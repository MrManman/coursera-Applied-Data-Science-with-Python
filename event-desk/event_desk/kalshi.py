"""Read-only client for Kalshi's public market-data REST API.

No account or API key is needed for market data. This module never places
orders; Event Desk is paper-trading only.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Iterator

import requests

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"


def _price(raw: dict[str, Any], name: str) -> float | None:
    """Return a price in dollars (0-1).

    Kalshi has served prices both as integer cents (``yes_bid``) and as
    dollar strings (``yes_bid_dollars``); accept either.
    """
    dollars = raw.get(f"{name}_dollars")
    if dollars not in (None, ""):
        return float(dollars)
    cents = raw.get(name)
    if cents is None:
        return None
    return float(cents) / 100.0


@dataclass(frozen=True)
class Market:
    ticker: str
    event_ticker: str
    title: str
    subtitle: str
    rules: str
    status: str
    close_time: str
    yes_bid: float | None
    yes_ask: float | None
    last_price: float | None
    volume: int
    result: str  # "yes", "no", or "" while unresolved

    @property
    def mid(self) -> float | None:
        """Midpoint of the quoted spread; falls back to the last trade."""
        if self.yes_bid is not None and self.yes_ask is not None and self.yes_ask > 0:
            return (self.yes_bid + self.yes_ask) / 2
        return self.last_price

    @property
    def settled(self) -> bool:
        return self.result in ("yes", "no")

    @classmethod
    def from_api(cls, raw: dict[str, Any]) -> "Market":
        return cls(
            ticker=raw["ticker"],
            event_ticker=raw.get("event_ticker", ""),
            title=raw.get("title", ""),
            subtitle=raw.get("yes_sub_title") or raw.get("subtitle", ""),
            rules=raw.get("rules_primary", ""),
            status=raw.get("status", ""),
            close_time=raw.get("close_time", ""),
            yes_bid=_price(raw, "yes_bid"),
            yes_ask=_price(raw, "yes_ask"),
            last_price=_price(raw, "last_price"),
            volume=int(raw.get("volume") or 0),
            result=(raw.get("result") or "").lower(),
        )


class KalshiClient:
    def __init__(self, base_url: str = BASE_URL, session: requests.Session | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        for attempt in range(4):
            resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=20)
            if resp.status_code == 429 or resp.status_code >= 500:
                time.sleep(2**attempt)
                continue
            resp.raise_for_status()
            return resp.json()
        resp.raise_for_status()
        return resp.json()

    def iter_markets(self, limit: int = 200, **filters: Any) -> Iterator[Market]:
        """Yield markets matching ``filters`` (e.g. status="open", series_ticker=...)."""
        params = {k: v for k, v in filters.items() if v is not None}
        cursor = None
        remaining = limit
        while remaining > 0:
            page = self._get(
                "/markets", {**params, "limit": min(remaining, 1000), "cursor": cursor}
            )
            markets = page.get("markets", [])
            for raw in markets:
                yield Market.from_api(raw)
            remaining -= len(markets)
            cursor = page.get("cursor")
            if not cursor or not markets:
                return

    def get_market(self, ticker: str) -> Market:
        return Market.from_api(self._get(f"/markets/{ticker}")["market"])
