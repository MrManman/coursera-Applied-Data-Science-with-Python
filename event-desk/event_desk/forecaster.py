"""Claude-backed forecaster and the prompt improver that closes the self-improvement loop."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from pydantic import BaseModel, Field

from .kalshi import Market

DEFAULT_MODEL = os.environ.get("EVENT_DESK_MODEL", "claude-opus-5")
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

# Server-side refusal fallback: a declined request is re-run on Anthropic's
# recommended fallback model inside the same call.
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class ForecastOutput(BaseModel):
    p_yes: float = Field(description="Probability the market resolves YES, between 0.01 and 0.99.")
    rationale: str = Field(description="Two to four sentences: key evidence and the base rate used.")


class ImprovedPrompt(BaseModel):
    prompt: str = Field(description="The complete new system prompt.")
    changes: list[str] = Field(description="Each change made and which misses it addresses.")


@dataclass(frozen=True)
class Forecast:
    p_yes: float
    rationale: str
    model: str


def load_prompt(version: str) -> str:
    return (PROMPTS_DIR / f"{version}.md").read_text()


def latest_prompt_version() -> str:
    versions = sorted(
        (p.stem for p in PROMPTS_DIR.glob("v*.md")), key=lambda v: int(re.sub(r"\D", "", v) or 0)
    )
    if not versions:
        raise FileNotFoundError(f"no prompt versions in {PROMPTS_DIR}")
    return versions[-1]


def describe_market(market: Market, research_notes: str | None = None) -> str:
    """The user message for one market. Market prices are deliberately left out so
    forecasts are independent and can be scored against the market."""
    now = datetime.now(timezone.utc).isoformat(timespec="minutes")
    parts = [
        f"Current time (UTC): {now}",
        f"Market: {market.title}",
        f"YES outcome: {market.subtitle}" if market.subtitle else "",
        f"Closes: {market.close_time}",
        f"Resolution rules: {market.rules}" if market.rules else "",
    ]
    if research_notes:
        parts.append(f"Research notes gathered just now:\n{research_notes}")
    return "\n".join(p for p in parts if p)


def _text(message) -> str:
    return "".join(b.text for b in message.content if getattr(b, "type", None) == "text")


class ClaudeForecaster:
    def __init__(self, model: str = DEFAULT_MODEL, client: anthropic.Anthropic | None = None):
        self.model = model
        self.client = client or anthropic.Anthropic()

    def research(self, market: Market) -> str | None:
        """Gather current evidence with the web search server tool."""
        messages = [{
            "role": "user",
            "content": (
                "Collect the most recent evidence relevant to how this prediction market will "
                "resolve: official data, forecasts, schedules, and credible news. Report facts "
                "with dates and sources. Do not give a probability.\n\n" + describe_market(market)
            ),
        }]
        for _ in range(3):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 5}],
                messages=messages,
            )
            if response.stop_reason == "refusal":
                return None
            if response.stop_reason != "pause_turn":
                return _text(response) or None
            messages.append({"role": "assistant", "content": response.content})
        return None

    def forecast(self, market: Market, system_prompt: str, *, research: bool = False) -> Forecast | None:
        notes = self.research(market) if research else None
        response = self.client.beta.messages.parse(
            model=self.model,
            max_tokens=16000,
            system=system_prompt,
            messages=[{"role": "user", "content": describe_market(market, notes)}],
            output_format=ForecastOutput,
            betas=[FALLBACK_BETA],
            fallbacks="default",
        )
        if response.stop_reason == "refusal" or response.parsed_output is None:
            return None
        out = response.parsed_output
        return Forecast(min(max(out.p_yes, 0.01), 0.99), out.rationale, self.model)

    def propose_prompt(self, current_prompt: str, scorecard_text: str, misses: list[dict]) -> ImprovedPrompt | None:
        """Ask Claude for a challenger prompt that addresses the champion's worst misses."""
        miss_lines = "\n".join(
            f"- {m['ticker']}: forecast {m['p_yes']:.2f}, market "
            f"{'n/a' if m['market_mid'] is None else format(m['market_mid'], '.2f')}, "
            f"resolved {m['result'].upper()}. Rationale given: {m['rationale']}"
            for m in misses
        )
        response = self.client.beta.messages.parse(
            model=self.model,
            max_tokens=16000,
            system=(
                "You improve the system prompt of a prediction-market forecaster. Find the "
                "systematic errors behind the misses (overconfidence, ignoring base rates, "
                "misreading resolution rules, stale data) and revise the prompt to correct them. "
                "Keep what works. Do not add knowledge of specific past outcomes; the new prompt "
                "must generalize to unseen markets."
            ),
            messages=[{
                "role": "user",
                "content": (
                    f"Current prompt:\n<prompt>\n{current_prompt}\n</prompt>\n\n"
                    f"Scorecard:\n{scorecard_text}\n\nWorst misses:\n{miss_lines}"
                ),
            }],
            output_format=ImprovedPrompt,
            betas=[FALLBACK_BETA],
            fallbacks="default",
        )
        if response.stop_reason == "refusal":
            return None
        return response.parsed_output
