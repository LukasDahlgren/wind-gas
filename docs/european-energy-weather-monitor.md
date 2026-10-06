# Swedish Day-Ahead Electricity Price Monitor

*Research project brief — prototype scope*

## Goal

Explore whether weather and power-system conditions help forecast the next day's wholesale electricity price in one Swedish bidding area. The initial area is **SE3** (central Sweden, including Stockholm); the target is the **SE3 day-ahead price by delivery interval**. The interface should report observed/forecast prices and explain uncertainty. Any buy/sell recommendation remains disabled until an explicit instrument, horizon, and out-of-sample evaluation are chosen.

## Why this market

Swedish electricity prices are set separately in four bidding areas, SE1 through SE4. Weather can affect wind and hydropower production as well as electricity demand, but prices also depend on other generation, outages, imports/exports, fuel prices, and transmission constraints. A local weather signal is therefore a feature to evaluate, not a standalone trading rule. [Svenska kraftnät: Operations and Electricity Markets](https://www.svk.se/en/national-grid/operations-and-electricity-markets/)

SE3 is the default project area because it provides a clear single-area scope and represents central Sweden. It is a project choice, not a claim that SE3 is the easiest zone to forecast. Keep the bidding area configurable for comparisons later.

## Initial narrow scope

- **Market:** Swedish SE3 bidding area.
- **Target:** ENTSO-E day-ahead market price for each delivery interval, normalized to SEK/MWh for display.
- **Horizon:** next-day auction results by delivery interval.
- **Initial explanatory inputs:** day-ahead wind and solar generation forecasts, day-ahead load forecast, calendar/season features, and recent price history.
- **Later context:** temperature, hydrological conditions, available generation/outages, cross-border flows, neighbouring prices, and fuel/carbon prices.
- **Output:** historical prices and an evaluated next-day price outlook with issue time, data freshness, missing-data status, and uncertainty. No trade call before a product and evaluation standard are selected.

The ENTSO-E Transparency Platform and `entsoe-py` expose day-ahead prices and relevant load/generation series. Confirm area coverage, resolution, units, revisions, and license for each downloaded series. Sweden's day-ahead market data is also available through Nord Pool. [ENTSO-E Transparency Platform](https://www.entsoe.eu/data/transparency-platform/) · [Nord Pool day-ahead market](https://www.nordpoolgroup.com/en/the-power-market/Day-ahead-market/)

## First implementation milestones

1. **Load and inspect data.** Collect at least one full year of SE3 day-ahead prices and aligned load/wind/solar forecasts. Save retrieval and publication/issue timestamps.
2. **Establish baselines.** Compare calendar/seasonal and recent-price baselines with models that add weather-linked forecasts.
3. **Evaluate chronologically.** Use walk-forward or held-out later periods; prevent forecast revisions or post-delivery observations from leaking into inputs.
4. **Report honestly.** Show actual historical prices and forecasts only when backed by loaded data. Mark gaps and stale data; do not synthesize example values as observations.
5. **Decide on a tradable product later.** A price forecast alone does not define a buy recommendation. Map the target to a specific instrument, fees, roll behavior, and decision horizon before evaluating a strategy.

## Key pitfalls

- **Price spikes and negative prices:** assess errors and performance in both typical and extreme intervals.
- **Daylight saving:** use Europe/Stockholm local delivery times while retaining unambiguous timestamps and 23/25-hour days.
- **Lookahead and revisions:** archived forecast vintages may differ from today's corrected history; save forecasts as they are issued.
- **Market coupling:** SE3 prices reflect neighbouring areas and grid capacity, so local weather alone may not explain price movements.
- **Unit and currency:** retain source units/currency in metadata and document any conversion.
- **No recommendation from correlation alone:** demonstrate improvement over a baseline on unseen periods and define a real product before generating buy/sell calls.

## Current prototype status

The backend defaults to SE3 and can request day-ahead prices and existing ENTSO-E load/generation/forecast datasets. The frontend is an unconnected research dashboard: it displays no fabricated price data and makes no trade recommendation until live data and validated forecasting are implemented.
