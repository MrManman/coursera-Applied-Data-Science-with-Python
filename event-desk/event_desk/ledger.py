"""SQLite experiment ledger: every forecast, paper trade, and settlement."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS forecasts (
    id             INTEGER PRIMARY KEY,
    created_at     TEXT NOT NULL,
    ticker         TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    model          TEXT NOT NULL,
    p_yes          REAL NOT NULL,
    market_mid     REAL,
    yes_bid        REAL,
    yes_ask        REAL,
    close_time     TEXT,
    rationale      TEXT
);
CREATE TABLE IF NOT EXISTS paper_trades (
    id          INTEGER PRIMARY KEY,
    forecast_id INTEGER NOT NULL REFERENCES forecasts(id),
    side        TEXT NOT NULL CHECK (side IN ('yes', 'no')),
    contracts   INTEGER NOT NULL,
    price       REAL NOT NULL,   -- cost per contract of the side bought, 0-1
    fee         REAL NOT NULL    -- total fee in dollars
);
CREATE TABLE IF NOT EXISTS settlements (
    ticker     TEXT PRIMARY KEY,
    result     TEXT NOT NULL CHECK (result IN ('yes', 'no')),
    settled_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS forecasts_ticker ON forecasts(ticker);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class ScoredForecast:
    ticker: str
    prompt_version: str
    p_yes: float
    market_mid: float | None
    outcome: int  # 1 if YES settled, else 0
    side: str | None
    contracts: int
    price: float
    fee: float

    @property
    def pnl(self) -> float:
        if self.side is None:
            return 0.0
        won = (self.side == "yes") == bool(self.outcome)
        payout = self.contracts * 1.0 if won else 0.0
        return payout - self.contracts * self.price - self.fee


class Ledger:
    def __init__(self, path: str | Path):
        self.conn = sqlite3.connect(str(path))
        self.conn.executescript(SCHEMA)

    def record_forecast(
        self,
        *,
        ticker: str,
        prompt_version: str,
        model: str,
        p_yes: float,
        market_mid: float | None,
        yes_bid: float | None,
        yes_ask: float | None,
        close_time: str,
        rationale: str,
    ) -> int:
        cur = self.conn.execute(
            "INSERT INTO forecasts (created_at, ticker, prompt_version, model, p_yes,"
            " market_mid, yes_bid, yes_ask, close_time, rationale)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (_now(), ticker, prompt_version, model, p_yes, market_mid, yes_bid, yes_ask,
             close_time, rationale),
        )
        self.conn.commit()
        return cur.lastrowid

    def record_trade(self, forecast_id: int, side: str, contracts: int, price: float, fee: float) -> None:
        self.conn.execute(
            "INSERT INTO paper_trades (forecast_id, side, contracts, price, fee) VALUES (?, ?, ?, ?, ?)",
            (forecast_id, side, contracts, price, fee),
        )
        self.conn.commit()

    def record_settlement(self, ticker: str, result: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO settlements (ticker, result, settled_at) VALUES (?, ?, ?)",
            (ticker, result, _now()),
        )
        self.conn.commit()

    def has_forecast(self, ticker: str, prompt_version: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM forecasts WHERE ticker = ? AND prompt_version = ? LIMIT 1",
            (ticker, prompt_version),
        ).fetchone()
        return row is not None

    def unsettled_tickers(self) -> list[str]:
        rows = self.conn.execute(
            "SELECT DISTINCT f.ticker FROM forecasts f"
            " LEFT JOIN settlements s ON s.ticker = f.ticker WHERE s.ticker IS NULL"
        ).fetchall()
        return [r[0] for r in rows]

    def prompt_versions(self) -> list[str]:
        rows = self.conn.execute("SELECT DISTINCT prompt_version FROM forecasts ORDER BY 1").fetchall()
        return [r[0] for r in rows]

    def scored(self, prompt_version: str | None = None) -> list[ScoredForecast]:
        """Settled forecasts. Only the first forecast per (ticker, version) counts."""
        sql = """
            SELECT f.ticker, f.prompt_version, f.p_yes, f.market_mid,
                   CASE s.result WHEN 'yes' THEN 1 ELSE 0 END,
                   t.side, COALESCE(t.contracts, 0), COALESCE(t.price, 0), COALESCE(t.fee, 0)
            FROM forecasts f
            JOIN settlements s ON s.ticker = f.ticker
            LEFT JOIN paper_trades t ON t.forecast_id = f.id
            WHERE f.id IN (SELECT MIN(id) FROM forecasts GROUP BY ticker, prompt_version)
        """
        params: tuple = ()
        if prompt_version is not None:
            sql += " AND f.prompt_version = ?"
            params = (prompt_version,)
        return [ScoredForecast(*row) for row in self.conn.execute(sql + " ORDER BY f.id", params)]

    def worst_misses(self, prompt_version: str, n: int = 15) -> list[dict]:
        """Settled forecasts with the largest squared error, for the improver."""
        rows = self.conn.execute(
            """
            SELECT f.ticker, f.p_yes, f.market_mid, s.result, f.rationale
            FROM forecasts f JOIN settlements s ON s.ticker = f.ticker
            WHERE f.prompt_version = ?
            ORDER BY (f.p_yes - CASE s.result WHEN 'yes' THEN 1.0 ELSE 0.0 END)
                   * (f.p_yes - CASE s.result WHEN 'yes' THEN 1.0 ELSE 0.0 END) DESC
            LIMIT ?
            """,
            (prompt_version, n),
        ).fetchall()
        keys = ("ticker", "p_yes", "market_mid", "result", "rationale")
        return [dict(zip(keys, r)) for r in rows]
