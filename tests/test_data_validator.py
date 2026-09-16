import pandas as pd

from data.data_validator import validate_market_data


def test_validd_market_data():

    data = pd.DataFrame({
        "Date": pd.date_range(
            start="2025-01-01",
            periods= 5
        ),
        "Open": [100,101,102,103,104],
        "High": [105,106,107,108,109],
        "Low": [95,96,97,98,99],
        "Close":[103,104,105,106,107],
        "Volume":[1000,1100,1200,1300,1400],
    })

    assert validate_market_data(data) is True

def test_missing_close_column():

    data = pd.DataFrame({
        "Date": pd.date_range(
            start="2025-01-01",
            periods=5
        ),
        "Open": [100, 101, 102, 103, 104],
        "High": [105, 106, 107, 108, 109],
        "Low": [95, 96, 97, 98, 99],
        "Volume": [1000, 1100, 1200, 1300, 1400],
    })

    assert validate_market_data(data) is False

def test_missing_values():

    data = pd.DataFrame({
        "Date": pd.date_range(
            start="2025-01-01",
            periods=5
        ),
        "Open": [100, 101, None, 103, 104],
        "High": [105, 106, 107, 108, 109],
        "Low": [95, 96, 97, 98, 99],
        "Close": [103, 104, 105, 106, 107],
        "Volume": [1000, 1100, 1200, 1300, 1400],
    })

    assert validate_market_data(data) is False

def test_duplicate_dates():

    data = pd.DataFrame({
        "Date": [
            "2025-01-01",
            "2025-01-02",
            "2025-01-02",
            "2025-01-04",
            "2025-01-05",
        ],
        "Open": [100, 101, 102, 103, 104],
        "High": [105, 106, 107, 108, 109],
        "Low": [95, 96, 97, 98, 99],
        "Close": [103, 104, 105, 106, 107],
        "Volume": [1000, 1100, 1200, 1300, 1400],
    })

    assert validate_market_data(data) is False

def test_negative_price():

    data = pd.DataFrame({
        "Date": pd.date_range(
            start="2025-01-01",
            periods=5
        ),
        "Open": [100, 101, -102, 103, 104],
        "High": [105, 106, 107, 108, 109],
        "Low": [95, 96, 97, 98, 99],
        "Close": [103, 104, 105, 106, 107],
        "Volume": [1000, 1100, 1200, 1300, 1400],
    })

    assert validate_market_data(data) is False

def test_negative_volume():

    data = pd.DataFrame({
        "Date": pd.date_range(
            start="2025-01-01",
            periods=5
        ),
        "Open": [100, 101, 102, 103, 104],
        "High": [105, 106, 107, 108, 109],
        "Low": [95, 96, 97, 98, 99],
        "Close": [103, 104, 105, 106, 107],
        "Volume": [1000, -1100, 1200, 1300, 1400],
    })

    assert validate_market_data(data) is False

