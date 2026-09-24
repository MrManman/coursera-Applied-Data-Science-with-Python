"""Paper-trading rule: buy only when the forecast beats the quote by more than fees plus a margin."""

from __future__ import annotations

import math
from dataclasses import dataclass

# Kalshi's general taker fee is ceil(0.07 * C * P * (1 - P)) rounded up to the
# cent. Some series use a different multiplier; check the current fee schedule
# before trusting paper P&L.
TAKER_FEE_RATE = 0.07


def taker_fee(contracts: int, price: float, rate: float = TAKER_FEE_RATE) -> float:
    return math.ceil(rate * contracts * price * (1 - price) * 100 - 1e-9) / 100


@dataclass(frozen=True)
class PaperTrade:
    side: str  # "yes" or "no"
    contracts: int
    price: float  # cost per contract of the side bought
    fee: float
    edge: float  # expected profit per contract after fees


def decide(
    p_yes: float,
    yes_bid: float | None,
    yes_ask: float | None,
    *,
    stake: float = 100.0,
    min_edge: float = 0.03,
) -> PaperTrade | None:
    """Return the trade to paper-book, or None.

    Buying YES costs the ask; buying NO costs 1 - bid. ``stake`` caps dollars
    per market (the 2%-of-capital limit on a $5K paper book by default).
    """
    candidates = []
    if yes_ask is not None and 0 < yes_ask < 1:
        candidates.append(("yes", yes_ask, p_yes))
    if yes_bid is not None and 0 < yes_bid < 1:
        candidates.append(("no", 1 - yes_bid, 1 - p_yes))

    best = None
    for side, price, p_win in candidates:
        contracts = int(stake // price)
        if contracts < 1:
            continue
        fee = taker_fee(contracts, price)
        edge = p_win - price - fee / contracts
        if edge >= min_edge and (best is None or edge > best.edge):
            best = PaperTrade(side, contracts, price, fee, edge)
    return best
