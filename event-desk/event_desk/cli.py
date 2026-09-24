"""Event Desk command line: scan, forecast, settle, report, improve."""

from __future__ import annotations

import argparse
import sys

from . import forecaster as fc
from .kalshi import KalshiClient
from .ledger import Ledger
from .paper import decide
from .scoring import promotion_verdict, scorecard


def cmd_scan(args, kalshi: KalshiClient, ledger: Ledger) -> None:
    for m in kalshi.iter_markets(limit=args.limit, status="open", series_ticker=args.series,
                                 event_ticker=args.event):
        if args.search and args.search.lower() not in (m.title + " " + m.subtitle).lower():
            continue
        mid = "  n/a" if m.mid is None else f"{m.mid:5.2f}"
        print(f"{m.ticker:40} mid {mid}  vol {m.volume:>8}  closes {m.close_time}  {m.title} {m.subtitle}")


def cmd_forecast(args, kalshi: KalshiClient, ledger: Ledger, forecaster=None) -> None:
    forecaster = forecaster or fc.ClaudeForecaster(model=args.model)
    versions = args.prompt or [fc.latest_prompt_version()]
    markets = [
        m for m in kalshi.iter_markets(limit=args.limit, status="open", series_ticker=args.series,
                                       event_ticker=args.event)
        if m.volume >= args.min_volume
    ]
    print(f"{len(markets)} open markets; prompt versions: {', '.join(versions)}")
    for version in versions:
        system_prompt = fc.load_prompt(version)
        for m in markets:
            if ledger.has_forecast(m.ticker, version):
                continue
            f = forecaster.forecast(m, system_prompt, research=args.research)
            if f is None:
                print(f"  {m.ticker}: skipped (declined or unparsable)")
                continue
            fid = ledger.record_forecast(
                ticker=m.ticker, prompt_version=version, model=f.model, p_yes=f.p_yes,
                market_mid=m.mid, yes_bid=m.yes_bid, yes_ask=m.yes_ask,
                close_time=m.close_time, rationale=f.rationale,
            )
            trade = decide(f.p_yes, m.yes_bid, m.yes_ask, stake=args.stake, min_edge=args.min_edge)
            note = ""
            if trade:
                ledger.record_trade(fid, trade.side, trade.contracts, trade.price, trade.fee)
                note = f"  PAPER BUY {trade.contracts} {trade.side.upper()} @ {trade.price:.2f} (edge {trade.edge:+.3f})"
            mid = "n/a" if m.mid is None else f"{m.mid:.2f}"
            print(f"  [{version}] {m.ticker}: model {f.p_yes:.2f} vs market {mid}{note}")


def cmd_settle(args, kalshi: KalshiClient, ledger: Ledger) -> None:
    settled = 0
    for ticker in ledger.unsettled_tickers():
        m = kalshi.get_market(ticker)
        if m.settled:
            ledger.record_settlement(ticker, m.result)
            settled += 1
    print(f"recorded {settled} new settlements")


def format_card(card) -> str:
    if card.n == 0:
        return f"{card.prompt_version}: no settled forecasts yet"
    market = "n/a" if card.market_brier is None else f"{card.market_brier:.4f}"
    lines = [
        f"{card.prompt_version}: {card.n} settled",
        f"  Brier {card.brier:.4f} vs market {market} ({'BEATS' if card.beats_market else 'does not beat'} market)",
        f"  log loss {card.log_loss:.4f}",
        f"  paper trades {card.trades}, P&L ${card.pnl:,.2f} on ${card.turnover:,.2f} turnover"
        f" ({card.edge_on_turnover:+.1%})",
        "  calibration (bucket, n, mean forecast, hit rate):",
    ]
    lines += [f"    {b:>8}  {n:4}  {p:.2f}  {h:.2f}" for b, n, p, h in card.calibration]
    return "\n".join(lines)


def cmd_report(args, kalshi: KalshiClient, ledger: Ledger) -> None:
    versions = ledger.prompt_versions()
    if not versions:
        print("no forecasts recorded yet")
        return
    for version in versions:
        card = scorecard(version, ledger.scored(version))
        ok, reasons = promotion_verdict(card)
        print(format_card(card))
        print("  GATE: " + ("PASS - eligible for live capital" if ok else "not yet: " + "; ".join(reasons)))
        print()


def cmd_improve(args, kalshi: KalshiClient, ledger: Ledger, forecaster=None) -> None:
    champion = args.prompt[0] if args.prompt else fc.latest_prompt_version()
    card = scorecard(champion, ledger.scored(champion))
    if card.n < args.min_settled:
        sys.exit(f"{champion} has {card.n} settled forecasts; need {args.min_settled} before proposing a challenger")
    forecaster = forecaster or fc.ClaudeForecaster(model=args.model)
    proposal = forecaster.propose_prompt(fc.load_prompt(champion), format_card(card),
                                         ledger.worst_misses(champion))
    if proposal is None:
        sys.exit("improver declined or returned nothing")
    new_version = f"v{int(fc.latest_prompt_version().lstrip('v')) + 1}"
    path = fc.PROMPTS_DIR / f"{new_version}.md"
    path.write_text(proposal.prompt.strip() + "\n")
    print(f"wrote challenger {path}")
    for change in proposal.changes:
        print(f"  - {change}")
    print(f"Next: run `forecast --prompt {champion} --prompt {new_version}` so both score the same markets.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="event-desk", description="Kalshi paper-trading forecaster")
    p.add_argument("--db", default="event_desk.sqlite", help="ledger path")
    sub = p.add_subparsers(dest="command", required=True)

    def market_filters(sp):
        sp.add_argument("--series", help="series ticker, e.g. a daily high-temperature series")
        sp.add_argument("--event", help="event ticker")
        sp.add_argument("--limit", type=int, default=50, help="max markets to fetch")

    sp = sub.add_parser("scan", help="list open markets")
    market_filters(sp)
    sp.add_argument("--search", help="substring filter on title")

    sp = sub.add_parser("forecast", help="forecast open markets and paper-trade")
    market_filters(sp)
    sp.add_argument("--prompt", action="append", help="prompt version(s); default latest")
    sp.add_argument("--model", default=fc.DEFAULT_MODEL)
    sp.add_argument("--research", action="store_true", help="gather news with web search first")
    sp.add_argument("--min-volume", type=int, default=0)
    sp.add_argument("--stake", type=float, default=100.0, help="max paper dollars per market")
    sp.add_argument("--min-edge", type=float, default=0.03, help="min edge per contract after fees")

    sub.add_parser("settle", help="record results for resolved markets")
    sub.add_parser("report", help="scorecard and promotion gate per prompt version")

    sp = sub.add_parser("improve", help="propose a challenger prompt from the worst misses")
    sp.add_argument("--prompt", action="append", help="champion version; default latest")
    sp.add_argument("--model", default=fc.DEFAULT_MODEL)
    sp.add_argument("--min-settled", type=int, default=30)
    return p


COMMANDS = {"scan": cmd_scan, "forecast": cmd_forecast, "settle": cmd_settle,
            "report": cmd_report, "improve": cmd_improve}


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    COMMANDS[args.command](args, KalshiClient(), Ledger(args.db))


if __name__ == "__main__":
    main()
