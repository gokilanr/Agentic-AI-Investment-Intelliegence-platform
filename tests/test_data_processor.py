import  pandas as pd
import pytest 

from data.data_processor import (
    remove_duplicate_dates,
    validate_ohlc_relationship,
    calculate_daily_return,
    calculate_log_return,
    calculate_moving_averages
)

def test_valid_ohlc_relationship():
    data =pd.DataFrame({
        "Open":[100],
        "High":[110],
        "Low" :[95],
        "Close":[105]
    })

    assert validate_ohlc_relationship(data) is True

def test_invalid_high():

    data = pd.DataFrame({
        "Open" : [100],
        "High" : [90],
        "Low" : [80],
        "Close" : [85]
    })

    assert validate_ohlc_relationship(data) is False


def test_invalid_low():

    data = pd.DataFrame({
        "Open" : [100],
        "High" : [110],
        "Low" : [105],
        "Close" : [102]
    })

    assert validate_ohlc_relationship(data) is False


def test_no_duplicate_dates():
    data = pd.DataFrame({
        "Date": pd.to_datetime([
            "2025-01-01",
            "2025-01-02",
            "2025-01-03",
        ]),
        "Close": [100, 105, 110],
    })

    result = remove_duplicate_dates(data)

    assert len(result) == 3

def test_duplicate_dates_are_removed():
    data = pd.DataFrame({
        "Date": pd.to_datetime([
            "2025-01-01",
            "2025-01-02",
            "2025-01-02",
            "2025-01-03",
        ]),
        "Close": [100, 105, 106, 110],
    })

    result = remove_duplicate_dates(data)

    assert len(result) == 3
    assert result["Date"].duplicated().sum() == 0

def test_calculate_daily_return():
    data = pd.DataFrame({
        "Close": [100, 110, 99],
    })

    result = calculate_daily_return(data)

    assert pd.isna(result.loc[0, "Daily_Return"])
    assert result.loc[1, "Daily_Return"] == pytest.approx(0.10)
    assert result.loc[2, "Daily_Return"] == pytest.approx(-0.10)

def test_calculate_log_return():
    data = pd.DataFrame({
        "Close": [100, 110, 99],
    })

    result = calculate_log_return(data)

    assert pd.isna(result.loc[0, "Log_Return"])
    assert result.loc[1, "Log_Return"] == pytest.approx(
        0.09531018
    )
    assert result.loc[2, "Log_Return"] == pytest.approx(
        -0.10536052
    )

def test_calculate_moving_averages():
    data = pd.DataFrame({
        "Close": list(range(1, 51))
    })

    result = calculate_moving_averages(data)

    #sma20
    assert result["SMA_20"].iloc[:19].isna().all()
    assert result["SMA_20"].iloc[19] == pytest.approx(10.5)

    #sma50
    assert result["SMA_50"].iloc[:49].isna().all()
    assert result["SMA_50"].iloc[49] == pytest.approx(25.5)
