import argparse
from types import SimpleNamespace

import pytest

from event_desk import cli
from event_desk import forecaster as fc
from event_desk.kalshi import KalshiClient, Market
from event_desk.ledger import Ledger
from event_desk.paper import decide, taker_fee
from event_desk.scoring import brier, promotion_verdict, scorecard


def raw_market(ticker, *, bid=40, ask=44, result="", status="active", volume=500):
    return {"ticker": ticker, "event_ticker": "EV", "title": f"Will {ticker} happen?",
            "yes_sub_title": "Yes", "rules_primary": "Resolves YES if it happens.",
            "status": status, "close_time": "2026-10-01T00:00:00Z", "yes_bid": bid,
            "yes_ask": ask, "last_price": 42, "volume": volume, "result": result}


class FakeResponse:
    def __init__(self, payload):
        self.payload, self.status_code = payload, 200

    def json(self):
        return self.payload

    def raise_for_status(self):
        pass


class FakeSession:
    """Serves /markets pages and /markets/{ticker} from an in-memory dict."""

    def __init__(self, markets):
        self.markets = markets

    def get(self, url, params=None, timeout=None):
        if url.endswith("/markets"):
            open_ = [m for m in self.markets.values() if not m["result"]]
            return FakeResponse({"markets": open_[: params["limit"]], "cursor": ""})
        return FakeResponse({"market": self.markets[url.rsplit("/", 1)[1]]})


class FakeForecaster:
    def __init__(self, probs):
        self.probs = probs

    def forecast(self, market, system_prompt, research=False):
        return fc.Forecast(self.probs[market.ticker], "test rationale", "fake-model")


def test_market_parses_cents_and_dollar_prices():
    cents = Market.from_api(raw_market("A", bid=40, ask=44))
    assert cents.yes_bid == pytest.approx(0.40) and cents.mid == pytest.approx(0.42)
    dollars = Market.from_api({**raw_market("B"), "yes_bid_dollars": "0.3100", "yes_ask_dollars": "0.3300"})
    assert dollars.mid == pytest.approx(0.32)
    assert Market.from_api(raw_market("C", result="yes")).settled


def test_taker_fee_rounds_up_to_cent():
    # 0.07 * 100 * 0.5 * 0.5 = 1.75
    assert taker_fee(100, 0.5) == pytest.approx(1.75)
    # 0.07 * 1 * 0.5 * 0.5 = 0.0175 -> 0.02
    assert taker_fee(1, 0.5) == pytest.approx(0.02)


def test_decide_buys_side_with_edge_after_fees_only():
    yes = decide(0.60, yes_bid=0.40, yes_ask=0.44)
    assert yes.side == "yes" and yes.price == pytest.approx(0.44) and yes.edge > 0.03
    no = decide(0.20, yes_bid=0.40, yes_ask=0.44)
    assert no.side == "no" and no.price == pytest.approx(0.60)
    assert decide(0.45, yes_bid=0.40, yes_ask=0.44) is None  # inside the spread


def test_promotion_gate_requires_volume_and_beating_market():
    from event_desk.ledger import ScoredForecast
    good = [ScoredForecast("T", "v1", 0.8, 0.6, 1, "yes", 10, 0.6, 0.2)] * 250
    ok, reasons = promotion_verdict(scorecard("v1", good))
    assert ok, reasons
    ok, reasons = promotion_verdict(scorecard("v1", good[:20]))
    assert not ok and "settled markets" in reasons[0]
    bad = [ScoredForecast("T", "v1", 0.4, 0.6, 1, None, 0, 0, 0)] * 250
    ok, reasons = promotion_verdict(scorecard("v1", bad))
    assert not ok and any("market midpoint" in r for r in reasons)


def test_end_to_end_forecast_settle_report(tmp_path, capsys):
    markets = {t: raw_market(t) for t in ("A", "B", "C")}
    kalshi = KalshiClient(session=FakeSession(markets))
    ledger = Ledger(tmp_path / "ledger.sqlite")
    args = argparse.Namespace(limit=10, series=None, event=None, prompt=["v1"], model="fake",
                              research=False, min_volume=0, stake=100.0, min_edge=0.03)
    cli.cmd_forecast(args, kalshi, ledger, forecaster=FakeForecaster({"A": 0.9, "B": 0.1, "C": 0.42}))
    # Re-running does not duplicate forecasts.
    cli.cmd_forecast(args, kalshi, ledger, forecaster=FakeForecaster({"A": 0.9, "B": 0.1, "C": 0.42}))
    assert ledger.conn.execute("SELECT COUNT(*) FROM forecasts").fetchone()[0] == 3
    assert ledger.conn.execute("SELECT COUNT(*) FROM paper_trades").fetchone()[0] == 2  # C has no edge

    markets["A"]["result"], markets["B"]["result"] = "yes", "no"
    cli.cmd_settle(None, kalshi, ledger)
    assert ledger.unsettled_tickers() == ["C"]

    rows = ledger.scored("v1")
    assert {r.ticker for r in rows} == {"A", "B"}
    card = scorecard("v1", rows)
    assert card.brier == pytest.approx((brier(0.9, 1) + brier(0.1, 0)) / 2)
    assert card.beats_market and card.pnl > 0

    cli.cmd_report(None, kalshi, ledger)
    out = capsys.readouterr().out
    assert "BEATS market" in out and "not yet" in out


def test_claude_forecaster_request_shape():
    """The forecaster sends blind market text, structured output, and refusal fallbacks."""
    calls = []

    class FakeMessages:
        def parse(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(stop_reason="end_turn",
                                   parsed_output=fc.ForecastOutput(p_yes=1.2, rationale="r"))

    client = SimpleNamespace(beta=SimpleNamespace(messages=FakeMessages()))
    f = fc.ClaudeForecaster(model="claude-opus-5", client=client)
    out = f.forecast(Market.from_api(raw_market("A")), "sys")
    assert out.p_yes == 0.99  # clamped
    kw = calls[0]
    assert kw["fallbacks"] == "default" and kw["betas"] == [fc.FALLBACK_BETA]
    assert kw["output_format"] is fc.ForecastOutput
    assert "0.4" not in kw["messages"][0]["content"]  # market price withheld


def test_claude_forecaster_skips_refusals():
    class FakeMessages:
        def parse(self, **kwargs):
            return SimpleNamespace(stop_reason="refusal", parsed_output=None)

    client = SimpleNamespace(beta=SimpleNamespace(messages=FakeMessages()))
    assert fc.ClaudeForecaster(client=client).forecast(Market.from_api(raw_market("A")), "s") is None


def test_latest_prompt_version_exists():
    assert fc.latest_prompt_version() == "v1"
    assert "calibrated" in fc.load_prompt("v1")
