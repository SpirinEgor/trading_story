from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from pandas import Timestamp


class TradingType(Enum):
    MONTHLY = 1
    DAILY = 2


@dataclass
class Event:
    timestamp: Timestamp
    lot_size: int
    price: float
    trading_type: int
    platform: int


TimeSeries = Dict[int, List[Event]]
