import  pandas as pd

from data.data_processor import(remove_duplicate_dates, validate_ohlc_relationship)


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