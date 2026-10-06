from datetime import date

import pandas as pd
import pytest

from windgas.entsoe import EntsoeLoader


def test_missing_token_is_clear(monkeypatch):
    monkeypatch.delenv("ENTSOE_API_TOKEN", raising=False)
    with pytest.raises(ValueError, match="ENTSOE_API_TOKEN"):
        EntsoeLoader()


def test_end_must_follow_start():
    loader = EntsoeLoader.__new__(EntsoeLoader)
    with pytest.raises(ValueError, match="end must be after start"):
        loader.load("load", date(2026, 1, 2), date(2026, 1, 2))


def test_forecast_column_selection():
    loader = EntsoeLoader.__new__(EntsoeLoader)
    loader.area = "DE_LU"
    class Client:
        def query_wind_and_solar_forecast(self, area, *, start, end):
            return pd.DataFrame({"Wind Onshore": [1.0], "Solar": [2.0]})
    loader.client = Client()
    query = loader._query_for("wind_forecast")
    result = query(start=None, end=None)
    assert list(result.columns) == ["Wind Onshore"]
