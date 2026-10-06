# European Energy Weather Monitor

*Project starter — tentative title, idea-level scope*

## Goal

Build a small monitor that answers: **Do tomorrow’s wind conditions suggest unusually high or low demand for gas-fired electricity generation?** Start with one market, establish whether the signal is useful, and expand toward a European outlook over the following week.

## Core hypothesis

When wind generation falls, gas-fired plants may need to supply more electricity. When wind rises, they may supply less. The effect depends on electricity demand, solar output, other available generators, imports, and fuel economics.

The relationship has a physical basis and observed relevance: the IEA reports that weak European wind generation boosted gas-fired generation in the first half of 2025. That supports investigating the idea; it does not establish a stable forecasting rule. [IEA electricity supply analysis](https://www.iea.org/reports/electricity-mid-year-update-2025/supply-renewables-grow-the-most-followed-by-gas-and-nuclear)

## Why it matters

Weather connects renewable electricity supply with demand for a traded fuel. A useful monitor could highlight calm periods, explain changes in gas-fired generation, and eventually track weather shocks across electricity and gas markets.

**Keep the target precise:** gas-fired electricity generation is an initial proxy for power-sector gas use. It is not total natural-gas demand, which also includes heating and industry. Converting electricity output into gas consumption would require additional assumptions about plant efficiency.

## Initial narrow scope

- **Market:** provisionally Germany’s DE-LU bidding zone; confirm data coverage before committing.
- **Horizon:** next day, using one fixed daily publication cutoff.
- **Data frequency:** hourly where available, summarized into a daily outlook.
- **Main signal:** forecast wind generation relative to normal conditions for that season.
- **Context:** expected electricity demand and solar generation; actual gas-fired generation for subsequent evaluation.
- **Output:** an indicative higher / typical / lower pressure assessment, a short explanation, and a recent-history chart.

Use published wind-generation forecasts first. Building a model that converts weather into wind-farm output can wait. Leave trading strategies, gas-price forecasts, exact gas-volume estimates, and a Europe-wide dashboard outside the MVP.

## Data needed

| Category | Purpose | Priority |
|---|---|---|
| Actual wind and gas-fired generation | Explore the relationship and evaluate outcomes | MVP |
| Day-ahead wind-generation forecasts | Produce the forward-looking signal | MVP |
| Actual and forecast electricity load | Distinguish wind effects from demand changes | MVP |
| Actual and forecast solar generation | Account for another variable electricity source | MVP |
| Publication time, forecast issue time, delivery time, retrieval time, revisions | Reconstruct what was knowable at each cutoff | MVP |
| Temperature and broader weather forecasts | Add cold-weather demand and longer horizons | Later |
| Other generation, outages, imports/exports, fuel and electricity prices | Explain exceptions and improve the outlook | Later, or earlier if initial findings require them |

Start by auditing the [ENTSO-E Transparency Platform](https://www.entsoe.eu/data/transparency-platform/) for generation and load data. Its [data categories](https://eepublicdownloads.entsoe.eu/clean-documents/mc-documents/transparency-platform/150101_Transparency%20Platform%20Data%20Categories.pdf) include day-ahead wind/solar forecasts and actual generation. Verify access, historical coverage, forecast versions, reporting gaps, and reuse terms for the chosen zone before designing around them.

## First implementation milestones

1. **Audit the data.** Confirm matching market boundaries and timestamps. Aim for at least one full year of historical actuals, preferably more. Begin saving daily forecast snapshots immediately.
2. **Explore the mechanism.** Compare low- and high-wind periods with gas-fired output, accounting for demand, solar, season, and hour. Identify cases where wind displaced another source instead.
3. **Create a simple baseline and signal.** Compare a basic outlook using calendar patterns and demand with one that also uses wind forecasts. Keep the pressure labels transparent; avoid complex modelling initially.
4. **Evaluate chronologically.** Use earlier periods to develop the approach and later periods to test it. Check whether wind adds useful information, including during sustained low-wind episodes.
5. **Publish a daily report.** Show the forecast, pressure assessment, explanation, issue time, data freshness, and previous outlook versus observed gas-fired generation.

## Key pitfalls

- **Lookahead and timing:** use only information actually available at the chosen cutoff. Today’s corrected historical forecast may differ from the version available then. If archived versions cannot be verified, use historical actuals for exploration and saved snapshots for forward evaluation.
- **Correlation versus cause:** demand, season, prices, and outages affect both dispatch and the apparent wind relationship. Describe evidence cautiously.
- **Changing substitution:** extra wind can displace coal, imports, hydro, or curtailed output rather than gas. A fixed wind-to-gas relationship may fail.
- **Data consistency:** align bidding zones, units, intervals, time zones, and daylight-saving changes. Missing values are not zero; incomplete days should be flagged.
- **Structural change:** new renewable capacity, plant closures, and changing fuel economics can make older patterns less relevant.
- **Market interpretation:** a physical demand signal alone does not demonstrate a price forecast or trading advantage; forecasts may already be reflected in prices.

## Clear MVP definition

**One reproducible daily report for one market, covering tomorrow’s expected pressure on gas-fired generation.** It contains wind, load, and solar forecasts; an explained pressure label; timestamps and missing-data flags; a historical context chart; and subsequent comparison with actual gas-fired output.

The MVP is complete when the report updates reliably and its assessment can be evaluated against a baseline using information available at the time. A weak or inconsistent wind signal is a valid research finding, not a reason to hide the results.

## Expansion path

After the MVP: add temperature and cold-plus-low-wind episodes; extend to several days; compare markets and simultaneous regional calm periods; monitor forecast revisions; then investigate gas consumption, storage effects, or market-price responses with their own data and validation.
