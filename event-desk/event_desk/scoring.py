"""Scorecards and the promotion gate for prompt versions."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .ledger import ScoredForecast

# A challenger goes live only after this many settled markets (see the plan's
# "200+ resolved markets" gate).
MIN_SETTLED_FOR_PROMOTION = 200


def brier(p: float, outcome: int) -> float:
    return (p - outcome) ** 2


def log_loss(p: float, outcome: int, eps: float = 1e-4) -> float:
    p = min(max(p, eps), 1 - eps)
    return -math.log(p if outcome else 1 - p)


@dataclass(frozen=True)
class Scorecard:
    prompt_version: str
    n: int
    brier: float
    market_brier: float | None  # same markets, using the market midpoint as the forecast
    log_loss: float
    trades: int
    pnl: float
    turnover: float
    calibration: list[tuple[str, int, float, float]]  # (bucket, n, mean forecast, hit rate)

    @property
    def beats_market(self) -> bool:
        return self.market_brier is not None and self.brier < self.market_brier

    @property
    def edge_on_turnover(self) -> float:
        return self.pnl / self.turnover if self.turnover else 0.0


def scorecard(prompt_version: str, rows: list[ScoredForecast]) -> Scorecard:
    n = len(rows)
    if n == 0:
        return Scorecard(prompt_version, 0, float("nan"), None, float("nan"), 0, 0.0, 0.0, [])

    priced = [r for r in rows if r.market_mid is not None]
    market_brier = (
        sum(brier(r.market_mid, r.outcome) for r in priced) / len(priced) if priced else None
    )
    # Compare like with like: model Brier on the same priced subset when available.
    base = priced or rows
    model_brier = sum(brier(r.p_yes, r.outcome) for r in base) / len(base)

    traded = [r for r in rows if r.side is not None]
    buckets = []
    for lo in range(0, 100, 10):
        hi = lo + 10
        in_bucket = [r for r in rows if lo / 100 <= r.p_yes < hi / 100 or (hi == 100 and r.p_yes == 1)]
        if in_bucket:
            buckets.append((
                f"{lo}-{hi}%",
                len(in_bucket),
                sum(r.p_yes for r in in_bucket) / len(in_bucket),
                sum(r.outcome for r in in_bucket) / len(in_bucket),
            ))

    return Scorecard(
        prompt_version=prompt_version,
        n=n,
        brier=model_brier,
        market_brier=market_brier,
        log_loss=sum(log_loss(r.p_yes, r.outcome) for r in rows) / n,
        trades=len(traded),
        pnl=sum(r.pnl for r in traded),
        turnover=sum(r.contracts * r.price for r in traded),
        calibration=buckets,
    )


def promotion_verdict(card: Scorecard, min_edge_on_turnover: float = 0.03) -> tuple[bool, list[str]]:
    """Whether a prompt version has earned live capital. Returns (ok, reasons it is not)."""
    reasons = []
    if card.n < MIN_SETTLED_FOR_PROMOTION:
        reasons.append(f"only {card.n}/{MIN_SETTLED_FOR_PROMOTION} settled markets")
    if not card.beats_market:
        reasons.append("Brier score does not beat the market midpoint")
    if card.edge_on_turnover < min_edge_on_turnover:
        reasons.append(
            f"paper edge {card.edge_on_turnover:.1%} of turnover is below {min_edge_on_turnover:.0%}"
        )
    return (not reasons, reasons)
