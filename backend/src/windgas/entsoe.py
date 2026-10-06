"""ENTSO-E Transparency Platform data loading helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd
from dotenv import load_dotenv
from entsoe import EntsoePandasClient


@dataclass(frozen=True)
class LoadResult:
    """A loaded time series and basic coverage metadata."""

    name: str
    data: pd.Series | pd.DataFrame
    area: str
    start: datetime
    end: datetime

    @property
    def missing_intervals(self) -> int:
        """Number of rows containing at least one missing observation."""
        return int(self.data.isna().any(axis=1).sum()) if isinstance(self.data, pd.DataFrame) else int(self.data.isna().sum())


class EntsoeLoader:
    """Fetch ENTSO-E data for an area; defaults to the DE-LU bidding zone."""

    def __init__(self, api_token: str | None = None, area: str = "DE_LU") -> None:
        load_dotenv()
        token = api_token or os.getenv("ENTSOE_API_TOKEN")
        if not token:
            raise ValueError(
                "ENTSOE_API_TOKEN is required. Copy .env.example to .env and add your token."
            )
        self.client = EntsoePandasClient(api_key=token)
        self.area = area
        self.timezone = ZoneInfo("Europe/Berlin" if area == "DE_LU" else "Europe/Brussels")

    def load(self, dataset: str, start: date, end: date) -> LoadResult:
        """Load one supported dataset for [start, end) in the area's local timezone.

        Supported names: load, generation, wind_forecast, solar_forecast.
        ``end`` is exclusive and is converted using local midnight, retaining correct
        daylight-saving behavior for the bidding zone.
        """
        if end <= start:
            raise ValueError("end must be after start")
        query = self._query_for(dataset)
        start_dt = datetime.combine(start, time.min, self.timezone)
        end_dt = datetime.combine(end, time.min, self.timezone)
        data = query(start=start_dt, end=end_dt)
        if not isinstance(data.index, pd.DatetimeIndex):
            raise TypeError(f"ENTSO-E returned unexpected index for {dataset}")
        return LoadResult(dataset, data, self.area, start_dt, end_dt)

    def load_many(self, datasets: Iterable[str], start: date, end: date) -> dict[str, LoadResult]:
        """Load several datasets, returning results keyed by dataset name."""
        return {name: self.load(name, start, end) for name in datasets}

    def _query_for(self, dataset: str):
        queries = {
            "load": self.client.query_load,
            "generation": self.client.query_generation,
            "wind_forecast": self.client.query_wind_and_solar_forecast,
            "solar_forecast": self.client.query_wind_and_solar_forecast,
        }
        try:
            query = queries[dataset]
        except KeyError as exc:
            raise ValueError(f"Unsupported dataset {dataset!r}; choose from {', '.join(queries)}") from exc

        if dataset in {"wind_forecast", "solar_forecast"}:
            # The API returns both; select the relevant column(s) where available.
            def forecast_query(*, start: datetime, end: datetime):
                result = query(self.area, start=start, end=end)
                if isinstance(result, pd.DataFrame):
                    words = ("wind",) if dataset == "wind_forecast" else ("solar",)
                    cols = [column for column in result.columns if any(word in str(column).lower() for word in words)]
                    return result[cols] if cols else result
                return result
            return forecast_query

        if dataset == "generation":
            return lambda *, start, end: query(self.area, start=start, end=end, psr_type=None)
        return lambda *, start, end: query(self.area, start=start, end=end)


def save_result(result: LoadResult, directory: Path = Path("data")) -> Path:
    """Save a result as CSV with area and retrieval metadata in a sidecar file."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{result.area.lower()}_{result.name}_{result.start:%Y%m%d}_{result.end:%Y%m%d}.csv"
    result.data.to_csv(path, index_label="timestamp")
    metadata = pd.Series({
        "dataset": result.name,
        "area": result.area,
        "start": result.start.isoformat(),
        "end_exclusive": result.end.isoformat(),
        "retrieved_at_utc": datetime.now(ZoneInfo("UTC")).isoformat(),
        "missing_intervals": result.missing_intervals,
    })
    metadata.to_json(path.with_suffix(".json"), indent=2)
    return path
