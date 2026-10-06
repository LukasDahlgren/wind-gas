# Windgas

A small research project exploring whether wind conditions help explain pressure on gas-fired electricity generation. The initial market is DE-LU; see [the project brief](docs/european-energy-weather-monitor.md) for scope and caveats.

## Repository layout

```text
backend/   Python package, CLI, dependencies, and tests
frontend/  Web client workspace
data/      Local downloaded datasets (not committed)
docs/      Project brief and design notes
```

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cd ..
cp .env.example .env
```

Register on the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) and request REST API access. Add the generated token to `.env` as `ENTSOE_API_TOKEN`.

## Load data

Dates use the bidding area's local timezone; `--end` is exclusive. Output CSV and metadata JSON files are written under `data/`.

```bash
windgas load --start 2025-01-01 --end 2025-02-01
windgas generation --start 2025-01-01 --end 2025-02-01
windgas wind_forecast --start 2025-01-01 --end 2025-02-01
windgas solar_forecast --start 2025-01-01 --end 2025-02-01
```

Supported datasets: `load`, `generation`, `wind_forecast`, `solar_forecast`. Generation is returned by production type. Forecast queries return matching wind or solar columns when the API response provides them. Missing intervals remain missing and are reported in metadata; they are never filled with zero.

## Important limits

The API returns current published data and may expose revised historical values. It does not by itself prove what a forecaster could have known at a past cutoff. Save forecast snapshots promptly for forward evaluation. Validate bidding-zone coverage, product definitions, units, and licensing before relying on the series in analysis or publication.
