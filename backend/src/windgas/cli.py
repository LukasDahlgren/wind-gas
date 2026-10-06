"""Command-line interface for downloading ENTSO-E data."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from windgas.entsoe import EntsoeLoader, save_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Load ENTSO-E transparency data")
    parser.add_argument("dataset", choices=["load", "generation", "wind_forecast", "solar_forecast"])
    parser.add_argument("--start", type=date.fromisoformat, required=True, help="Start date, YYYY-MM-DD")
    parser.add_argument("--end", type=date.fromisoformat, required=True, help="Exclusive end date, YYYY-MM-DD")
    parser.add_argument("--area", default="DE_LU", help="ENTSO-E bidding zone code (default: DE_LU)")
    parser.add_argument("--output", type=Path, default=Path("data"), help="Output directory (default: data)")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = EntsoeLoader(area=args.area).load(args.dataset, args.start, args.end)
    path = save_result(result, args.output)
    print(f"Saved {len(result.data)} rows to {path} ({result.missing_intervals} rows with missing data)")


if __name__ == "__main__":
    main()
