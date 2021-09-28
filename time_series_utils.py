from typing import List, Tuple

from pandas import DataFrame, Series

from models import Event, TimeSeries, TradingType


def create_event(data: Series) -> Event:
    return Event(
        timestamp=data["timestamp"],
        lot_size=data["lot_size"],
        price=data["price"],
        platform=data["platform_id"],
        trading_type=TradingType.MONTHLY if data["trading_type"] == "monthly" else TradingType.DAILY
    )


def extract_time_series(data: DataFrame) -> TimeSeries:
    result = {}
    for session, values in data.groupby("session_id"):
        result[session] = [create_event(it[1]) for it in values.iterrows()]
    return result


def train_test_split(data: List[Event], test_size: float = 0.3) -> Tuple[List[Event], List[Event]]:
    data = sorted(data, key=lambda x: x.timestamp)  # just in case
    test_size = int(len(data) * test_size)
    return data[:-test_size], data[-test_size:]
