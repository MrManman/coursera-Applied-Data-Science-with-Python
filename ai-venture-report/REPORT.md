# AI Venture Plan: 5 Ideas for a $10M Profit Target from $500K

**Date:** 2026-09-24. **Target:** $10M net profit in 12 months on $500K, mostly automated, low compliance burden.

**Bottom line up front:** P($10M in 12 months) ≈ 4% (2–6%). P(profitable by month 12) ≈ 45%. The one idea with a realistic path is a paid-acquisition portfolio of AI consumer web apps (App Foundry). Concentrate capital there and gate everything else.

> Projections are planning estimates. Some sources are secondary blogs and some figures conflict, so verify key numbers before committing capital.

## 0. Who did the research

A CEO agent ran each research role as a separate pass with live web search (September 2026 sources). It could not spawn independent sub-agents.

| Role | Main conclusions |
|---|---|
| Market scout | Revenue ramps fast when distribution is bought: HeadshotPro ~$3.6M ARR run solo; Arcads $6M→$15M ARR in ~12 months; Polsia ~$10M run-rate, only ~$4.6M of it subscription ARR. Organic channels are closing: Google's March 2026 enforcement cut pSEO clicks by 50–80%, AI Overviews cut CTR by ~58–65%, and YouTube is terminating channels under its inauthentic-content policy. |
| Quant/markets | Kalshi and Polymarket have tens of billions in YTD volume but are bot-saturated: 14 of the top 20 Polymarket wallets are bots, and 0.51% of wallets made >$1K. Kalshi rebates are capped at $7K/week and changeable on 7 days' notice. Basis trades net mid-single digits a year. No path to $10M. |
| Unit economics | $10M profit needs ~$30–40M revenue in 12 months, which only paid acquisition with <30-day payback can deliver. Hard-paywall apps convert ~10.7% of downloads to paid versus 2.1% for freemium. Shopify apps: 81% stay under $1K MRR, 4.6% reach $10K MRR. |
| Infrastructure/tooling | Haiku 4.5 ~$1/$5 per million tokens (input/output); Sonnet-class ~$2–3/$10–15; batch jobs at half price. Reliable now: coding agents shipping small apps, creative generation and testing, funnel A/B tests, bandit budget allocation, eval-gated prompt tuning. Needs a human gate: big spending decisions, ToS/legal judgment, strategy. |
| Contrarian | Scrapped the performance-fee ad-ops agency. Changes to the other four ideas are listed per idea. |

**Candidates and screening**

- **Top 5 before contrarian review:** App Foundry; Creative Lab; Event Desk; Agent-Ready Catalog; performance-fee ad-ops agency.
- **Promoted in place of the scrapped agency:** Extract API.
- **Scrapped at screening:**
  - **Crypto basis fund:** 5–11% a year cannot reach 20x.
  - **Programmatic SEO:** Google's scaled-content-abuse enforcement.
  - **Faceless YouTube network:** YouTube's inauthentic-content policy and mass channel terminations.
  - **AI receptionist:** heavy setup, customers churn within ~60 days, commoditized at $49/mo, high support load.
- **Excluded by the constraints:** retail trading signals, health and legal services, lending, crypto tokens.

## 1. Shared agent stack

- **Models:** a Sonnet-class orchestrator; Haiku-class models for volume work.
- **Experiment ledger:** every change records a hypothesis, the metric, the sample size and a stopping rule.
- **Promotion rule:** a change ships only if it beats the incumbent on the eval set and in a live A/B test.
- **What agents may change:** prompts, copy, creative, prices and budgets inside caps. Changes to core code go through PRs with CI and human review.
- **Guardrails:** daily spend caps, a compliance-check agent, automatic refunds under $50, and a kill switch.
- **Run cost:** $8–20K/month.

## 2. Contrarian verdicts

| Idea | Verdict |
|---|---|
| App Foundry | MODIFY |
| Creative Lab | MODIFY |
| Event Desk | MODIFY (shrunk) |
| Agent-Ready Catalog | MODIFY |
| Performance-fee ad-ops agency | **SCRAP** |
| Extract API (promoted) | MODIFY |

## 3. Summary of the five ideas

ROI is 12-month profit divided by the capital allocated to that idea.

| # | Idea | Capital | Bear / Base / Bull profit (ROI) | P($10M in 12 mo) | P(profitable) |
|---|---|---|---|---|---|
| 1 | App Foundry | $250K | −$0.2M (−80%) / +$0.8M (+320%) / +$10M (+4,000%) | ~3% | ~35% |
| 2 | Creative Lab | $100K | −$80K (−80%) / +$0.5M (+500%) / +$5M (+5,000%) | ~0.5% | ~25% |
| 3 | Event Desk | $60K | −$30K (−50%) / +$30K (+50%) / +$250K (+420%) | <0.2% | ~40% |
| 4 | Agent-Ready Catalog | $40K | −$40K (−100%) / +$0.2M (+500%) / +$2.5M (+6,250%) | ~0.3% | ~20% |
| 5 | Extract API | $0 up front; $40K from reserve if it passes the day-60 review | −$40K / +$0.15M (+375%) / +$1.5M | ~0.2% | ~20% |

## 4. Ideas in detail

### Idea 1: App Foundry

**What it is:** agents build and run 10–30 single-purpose AI consumer web apps with Stripe web checkout, for example headshots, pet portraits, room redesign, voice or song gifts, resume polish and study cards.

- **Revenue:** $19–49 one-time purchases or $9.99–29.99/mo subscriptions.
- **Growth:** bought through Meta, TikTok and Google ads.
- **Portfolio logic:** most apps die; the 1–3 with 7-day ROAS above 1.3 get scaled.

**The self-improving loop**

- **Measures:** CPM, CTR, CPA, landing and paywall conversion, D0/D7 ROAS, refund and chargeback rate, D30 retention, output quality ratings, generation cost per order.
- **Changes:**
  - An idea agent mines ad libraries for new app ideas.
  - A coding agent ships a new app in 48–72 hours.
  - A creative agent produces 50–200 ad variants a week.
  - A bandit algorithm allocates budget across apps and ads.
  - A funnel agent tests paywalls and prices.
  - A quality agent tunes prompts and model routing.
- **Kill rule:** 14-day ROAS below 0.6 after $3K of spend.

**Automation and support:** ~90% automated. Instant refunds plus an LLM support agent; ~1% of tickets escalate; one human at 10–15 hours a week.

**Compliance:**

- ROSCA and state auto-renewal laws (clear consent, easy cancel).
- Ad platform policies.
- Uploaded photos deleted within 30 days.
- No biometric identification (BIPA).
- Excluded categories: health, finance, legal, NSFW, minors.

**Capital: $250K**

| Use | Amount |
|---|---|
| Ads | $150K |
| APIs and hosting | $35K |
| People | $35K |
| Chargeback/processor reserve | $30K |

| Case | Revenue | Profit | ROI |
|---|---|---|---|
| Bear | $0.4M | −$0.2M | −80% |
| Base | $4.0M | +$0.8M | +320% |
| Bull | $35M | +$10M | +4,000% |

The bull case assumes two apps each spending more than $1M/month on ads at ~1.4x 30-day ROAS and ~29% net margin.

**Probabilities:** P($10M) ~3%; P(profitable) ~35%. **Ceiling:** $50–100M+/yr as an app portfolio.

**Contrarian criticisms and responses**

1. **Ad-account bans.** Run 3+ business managers across Meta, TikTok and Google, pre-screen every creative, and keep at least 30% of spend off Meta by month 6.
2. **Payment processor freeze.** Keep chargebacks under 0.5%, use a clear billing descriptor, send renewal reminders, keep Paddle live as a backup processor, and hold a $30K reserve.
3. **Subscription-trap regulations.** One-click cancel and no dark patterns, as fixed rules the agents cannot A/B test around.
4. **ROAS decay and creative fatigue as spend scales.** Accepted as the core risk; handled by the kill rule and bandit allocation.
5. **Copycats.** Rejected as a reason to drop the idea; the edge is how fast the loop runs across a portfolio.
6. **Frontier labs bundle the same feature.** Choose workflow- or deliverable-specific jobs and review overlap monthly.

**30/60/90-day plan**

- **Day 30:** app template, experiment ledger and compliance agent built; 5 apps live; $30K spent.
- **Day 60:** 12+ apps launched and 8+ killed; 1 app at D7 ROAS ≥ 1.0 on $10K+ of spend; 100+ ad variants a week.
- **Day 90:** 1 app at 30-day ROAS ≥ 1.3 spending $3K+/day; portfolio contribution-margin positive.

**Kill criteria**

- No app at D30 ROAS ≥ 1.1 on $20K+ of spend by day 90.
- Chargebacks above 0.9% for 2 weeks: pause, and kill if it recurs.
- Cumulative losses reach $200K.
- Bans on 2 ad platforms within 60 days.

### Idea 2: Creative Lab

**What it is:** self-serve SaaS for subscription-app and DTC advertisers spending $20–500K/month on ads.

- Connects to Meta and TikTok through their official APIs.
- Generates ad variants from licensed avatars and the customer's own assets.
- Runs structured creative tests.
- Learns per-vertical benchmarks across all customer accounts.
- **Pricing:** $199–1,499/mo plus usage credits.
- App Foundry is its first user.

**The self-improving loop**

- **Measures:** thumb-stop rate, CTR, CPA and how fast ads fatigue, pooled into per-vertical benchmarks.
- **Changes:** hook and angle prompts, format and avatar recommendations, test-budget defaults, refresh timing. An eval set of historical ads checks how well it predicts winners.

**Automation and support:** ~85% automated. No custom creative work is ever sold. LLM support, plus a part-time human above 300 customers.

**Compliance:** Meta and TikTok API terms, avatar likeness rights, FTC endorsement guides, DPA/GDPR.

**Capital: $100K**

| Use | Amount |
|---|---|
| Build | $30K |
| Video-generation cost buffer | $25K |
| Customer acquisition | $35K |
| Reserve | $10K |

| Case | Revenue | Profit | ROI |
|---|---|---|---|
| Bear | $0.15M | −$80K | −80% |
| Base | $1.8M (exit ~$3.5M ARR) | +$0.5M | +500% |
| Bull | $12M (exit ~$25M ARR) | +$5M | +5,000% |

**Probabilities:** P($10M) ~0.5%; P(profitable) ~25%. **Ceiling:** $50–200M enterprise value.

**Contrarian criticisms and responses**

1. **Crowded market, including free tools built into Meta and TikTok.** Sell measured test outcomes rather than avatar generation, and start with subscription-app advertisers.
2. **Video-generation costs.** Usage credits, cheap draft renders, and a 70% gross-margin floor.
3. **API access revoked.** Apply for Meta app review early, use documented endpoints only, require customer confirmation before publishing, and keep a CSV export fallback.
4. **FTC risk from synthetic testimonials.** Block those templates.
5. **SaaS rarely profits in year 1.** Accepted; hence the small allocation.

**30/60/90-day plan**

- **Day 30:** internal version live; eval set of 2,000+ ads; Meta app review submitted.
- **Day 60:** public beta; 30 paying customers; gross margin ≥ 65%.
- **Day 90:** 120 paying customers; $40K MRR; churn under 8%; CAC payback under 4 months.

**Kill criteria (day 120):** under $20K MRR, churn above 12%, or API access denied. If any is true, fold it into App Foundry as an internal tool.

### Idea 3: Event Desk

**What it is:** proprietary trading of your own capital on Kalshi, a CFTC-regulated prediction-market exchange. No customers.

- **Long-tail market making:** quoting in thin markets that professional bots ignore.
- **News-based forecasts:** LLM probability estimates for economic, weather and scheduled-data markets.
- **Consistency trades:** buying and selling related contracts whose prices disagree.
- **Excluded:** sports contracts.

**The self-improving loop**

- **Measures:** forecast accuracy (Brier score) and calibration; net edge per strategy and category; losses to better-informed traders; incentive payout per dollar of capital.
- **Changes:** forecasting prompts and source weights, quote widths and inventory limits, which categories to trade.
- **Gate:** every change is paper-traded first and goes live only after 200+ settled markets show positive net edge after fees.

**Automation:** ~95%, with a weekly human risk review.

**Compliance:** low. Exchange rules, position limits, identity checks for the account entity, taxes, and no trading on inside information.

**Capital: $60K**: $50K of trading capital plus $10K for data and infrastructure.

| Case | Trading P&L | Profit | ROI |
|---|---|---|---|
| Bear | −$20K | −$30K | −50% |
| Base | +$40K | +$30K | +50% |
| Bull | +$260K | +$250K | +420% |

**Probabilities:** P($10M) <0.2%; P(profitable) ~40%. **Ceiling:** capacity-limited to ~$1–5M/yr.

**Contrarian criticisms and responses**

1. **Bot saturation.** Capital cut from $150K to $50K; trade long-tail markets only, after paper-trading proof.
2. **Exchange incentives can change on 7 days' notice.** Base cases assume zero incentive income.
3. **Losing to better-informed traders.** Pull quotes around scheduled data releases, cap inventory at 2% of capital per market, and stop a category automatically when those losses pile up.
4. **Can never reach $10M.** Accepted; kept for positive expected value and as a testbed for the agent loop.

**30/60/90-day plan**

- **Day 30:** data and forecasting pipeline built; paper trading across 5 categories.
- **Day 60:** $15K live in the 1–2 categories that showed edge.
- **Day 90:** scale to $50K if net edge is at least 3% of turnover over 200+ settled markets.

**Kill criteria:** 25% drawdown; no edge after 300 settled markets; a regulatory change that hurts the strategy.

**Prototype:** a paper-trading implementation lives in [`../event-desk/`](../event-desk/README.md).

### Idea 4: Agent-Ready Catalog

**What it is:** a Shopify app, later also WooCommerce and BigCommerce, for how merchants' products appear in AI shopping assistants such as ChatGPT shopping, Google AI Mode and Perplexity.

- Tracks each product's visibility in those assistants.
- Rewrites titles, attributes and structured data to improve it.
- Reports traffic and sales referred by AI assistants.
- **Why now:** AI-driven Shopify orders grew ~13x year on year in Q1 2026.
- **Pricing:** free tier, then $29–299/mo billed through Shopify.

**The self-improving loop**

- **Measures:** a per-product AI visibility score, AI-referred sessions and conversion, and the lift from each rewrite across all stores.
- **Changes:** promotes rewrite patterns that win across stores, retires the rest, and tunes the prompts used to sample the AI assistants.

**Automation and support:** ~90% automated. Every change can be undone in one click; LLM support; a human under 5 hours a week.

**Compliance:** low.

- Shopify app requirements and GDPR webhooks.
- Rewrites limited to facts already in the merchant's product data.
- Respect the terms of the AI assistants being sampled.

**Capital: $40K**

| Case | Revenue | Profit | ROI |
|---|---|---|---|
| Bear | $30K | −$40K | −100% |
| Base | $0.6M | +$0.2M | +500% |
| Bull | $5M | +$2.5M | +6,250% |

**Probabilities:** P($10M) ~0.3%; P(profitable) ~20%. **Ceiling:** could reach $100M+ ARR if AI assistants become a primary sales channel.

**Contrarian criticisms and responses**

1. **81% of Shopify apps stay under $1K MRR.** Capital capped, with hard gates.
2. **Shopify or OpenAI will build it natively.** Offer neutral measurement across all assistants, and go multi-platform by month 4.
3. **Attribution is noisy.** Each merchant keeps 20% of products unchanged as a control group.
4. **The AI-search optimization category is crowded.** Target small merchants with a self-serve product.

**30/60/90-day plan**

- **Day 30:** MVP built and submitted to the Shopify App Store.
- **Day 60:** 300 installs, 5% paying.
- **Day 90:** $10K MRR; 30% of merchants show visibility lift against their control products.

**Kill criteria:** under $5K MRR by day 120; Shopify ships an equivalent native feature; control tests show no lift.

### Idea 5: Extract API (promoted)

**What it is:** an API that turns logistics documents (bills of lading, invoices, packing lists, customs forms) into validated JSON with confidence scores.

- Accuracy benchmarks are published.
- **Pricing:** $0.03–0.15 per page.
- **Sales:** self-serve to developers.

**The self-improving loop**

- **Measures:** field-level accuracy on a labeled eval set that grows from customer corrections (through an opt-in feedback endpoint), cost per page by model route, and latency.
- **Changes:** prompts and schemas per document type, model routing (the cheapest model that meets the accuracy target), and validation rules. A change deploys only if it beats the incumbent on the evals.

**Automation and support:** ~90% automated, with documentation, LLM support and a status page.

**Compliance:** a data processing agreement, zero data retention by default, and a SOC 2 Type I audit once revenue justifies it.

**Capital:** $0 up front; $40K from the reserve if the day-60 review justifies it.

| Case | Revenue | Profit |
|---|---|---|
| Bear | $20K | −$40K |
| Base | $0.4M | +$0.15M (+375%) |
| Bull | $3M | +$1.5M |

**Probabilities:** P($10M) ~0.2%; P(profitable) ~20%. **Ceiling:** $20–50M ARR.

**Contrarian criticisms and responses**

1. **Frontier models already do this.** Sell validated accuracy on messy logistics scans.
2. **Funded competitors.** Compete in one vertical only, deeper and cheaper.
3. **Enterprise buyers need security reviews.** Self-serve only until $50K MRR; get SOC 2 once it pays for itself.
4. **Low odds of $10M.** Accepted; hence no up-front capital.

**30/60/90-day plan after funding**

- **Day 30:** 3 document types supported; 1,500 labeled pages.
- **Day 60:** 50 signups; 10 paying customers.
- **Day 90:** $8K MRR.

**Kill criteria:** under $5K MRR 90 days after funding, or accuracy not at least 3 points better than calling a frontier model directly.

### Scrapped: performance-fee ad-ops agency

- Needs admin access to clients' ad accounts, with liability when an account is banned.
- Clients dispute how much profit the agency actually caused.
- Every client needs custom service, which breaks the low-support constraint.
- B2B sales cycles are too slow for the 12-month target.
- Polsia already bundles ad-running with a revenue share.

Its useful parts live on inside App Foundry and Creative Lab.

## 5. Recommendation

| Idea | Allocation | P($10M) | P(profitable) | Base-case profit |
|---|---|---|---|---|
| App Foundry | $250K | ~3% | ~35% | +$0.8M |
| Creative Lab | $100K | ~0.5% | ~25% | +$0.5M |
| Event Desk | $60K | <0.2% | ~40% | +$30K |
| Agent-Ready Catalog | $40K | ~0.3% | ~20% | +$0.2M |
| Extract API | $0 (reserve option) | ~0.2% | ~20% | +$0.15M |
| Reserve | $50K | — | — | — |

**Reallocation gates**

- **Day 60:** capital from any idea that missed its gate returns to the reserve; Extract API may be funded.
- **Day 90:** if App Foundry has a winning app, it gets the reserve, all freed capital and its own reinvested profits. If not, stop its ad spend (expected loss ~$150–200K).

**Honest odds**

| Outcome | Estimate |
|---|---|
| $10M net profit within 12 months | ~4% (2–6%) |
| Profitable at all by month 12 | ~45% |
| Losing most of the $500K | ~30–35% |
| Reaching a $10M/yr profit run-rate within 24 months | ~10–15% |

Expected 12-month profit is roughly +$0.3–0.6M.

## Sources

- **Prediction markets:** Finance Magnates (bot playground); CryptoSlate (prop firms and AI agents on Polymarket/Kalshi); 1023jack (Polymarket bot profitability); Kalshi help center (Liquidity Incentive Program) and kalshi.com/incentives; Prediction Hunt (Kalshi fees 2026).
- **AI model pricing:** BenchLM and MetaCTO (Claude API pricing, September 2026).
- **AI startup comparables:** TechCrunch (2026-07-08, AI startup revenue growth); Fortune (2026-05-18, solo founders); note.com/x402inc and Mixergy (Polsia); Latka (Arcads); Trends.vc (synthetic UGC ads).
- **Content channels:** ScaleLab and ytgrowth (YouTube AI policy); MADX and seo-kreativ (pSEO and AI Overviews).
- **Subscription apps and ads:** RevenueCat State of Subscription Apps 2026; Adapty (Meta ads for subscription apps).
- **Shopify apps:** Week One Labs and Uptek (Shopify app benchmarks).
- **Crypto yields:** Medium (funding-rate arbitrage in 2026; Ethena stops farming the basis).
- **AI receptionists:** BossBot and Vellum.

Some sources are secondary blogs and some figures conflict (e.g., Creatify's ARR), so treat the projections as planning estimates.
