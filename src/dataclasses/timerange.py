from dataclasses import dataclass
from datetime import datetime
import pandas as pd


@dataclass
class TimeRangeSettings:
    pass


@dataclass
class NoTimeRangeAdjustment(TimeRangeSettings):
    pass


@dataclass
class ExtendedTimeRangeByLooping(TimeRangeSettings):
    datetime_from: datetime | pd.Timestamp
    datetime_to: datetime | pd.Timestamp
