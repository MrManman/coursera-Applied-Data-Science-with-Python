# Event Desk: paper-trading prototype

Forecasts Kalshi prediction markets with Claude, paper-trades the forecasts, and scores them against actual outcomes. **It never places real orders.** Its job is to answer one question before any money is at risk: *do the forecasts beat the market price after fees?*

## The loop

```
scan ──► forecast ──► (markets close) ──► settle ──► report ──► improve ──► forecast (champion vs challenger)
```

1. **forecast**: Claude estimates P(YES) for each open market. It does **not** see the market price, so each forecast is an independent check against the market. A paper trade is booked only when the forecast beats the ask (to buy YES) or the bid (to buy NO) by more than Kalshi's taker fee plus a margin (default 3¢ per contract, $100 cap per market).
2. **settle**: records YES/NO results for markets that have resolved.
3. **report**: for each prompt version, shows:
   - Brier score against the market midpoint on the same markets
   - log loss
   - calibration table
   - paper P&L
   - the **promotion gate**: 200+ settled markets, Brier score better than the market, and paper edge of at least 3% of turnover
4. **improve**: Claude reads the current prompt's worst misses and writes a challenger prompt (`prompts/v2.md`, …). Run both on the same markets. A challenger replaces the champion only if it scores better in `report`. That is the self-improvement loop, and nothing is promoted without settled results.

## Setup

```bash
cd event-desk
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # or `ant auth login`
```

Kalshi market data is public, so no Kalshi account is needed for paper trading.

## Usage

```bash
python -m event_desk scan --limit 50 --search temperature      # find series to follow
python -m event_desk forecast --series <SERIES_TICKER> --limit 20
python -m event_desk forecast --series <SERIES_TICKER> --research   # web-search news first (more tokens)
python -m event_desk settle          # run daily, e.g. from cron
python -m event_desk report
python -m event_desk improve         # after 30+ settled forecasts
python -m event_desk forecast --series <SERIES_TICKER> --prompt v1 --prompt v2
```

- Start with **one category** that settles daily and has public data, such as daily high-temperature markets or scheduled economic releases.
- Run `forecast` once or twice a day and `settle` daily.
- At about 10–20 markets a day, reaching 200 settled markets takes 2–3 weeks.

The model defaults to `claude-opus-5`. Set `--model` or `EVENT_DESK_MODEL` to change it; a cheaper model makes high-volume runs cheaper. Requests opt into server-side refusal fallback (`fallbacks: "default"`), and any market that still gets declined is skipped.

## Files

| Path | What |
|---|---|
| `event_desk/kalshi.py` | Read-only public market-data client |
| `event_desk/forecaster.py` | Claude forecaster, optional web research, prompt improver |
| `event_desk/paper.py` | Fee model and trade rule |
| `event_desk/scoring.py` | Brier, log loss, calibration, promotion gate |
| `event_desk/ledger.py` | SQLite ledger of forecasts, trades, and settlements |
| `prompts/v1.md` | Starting forecaster prompt |

Run the tests with `python -m pytest -q`.

## Caveats

- **Paper fills are optimistic.** They assume you get the quoted price with no slippage and no queue, and that nobody better informed is on the other side. Live results will be worse.
- **Fee model:** `ceil(0.07 × contracts × P × (1−P))`, Kalshi's general taker fee. Some series use different rates, so check the current fee schedule.
- **Tax treatment of event contracts is unsettled.** Talk to a CPA before going live.
- **Not yet run against live APIs.** The build environment blocked Kalshi and had no Anthropic key. The logic is covered by offline tests, and the Claude request format was checked against a local stub server.
