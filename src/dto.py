"""Data Transfer Objects (DTOs) for handling DataFrame metadata and settings."""

from dataclasses import dataclass
import pandas as pd
from typing import Literal, Union


@dataclass
class DateTimeFormat:
    """Class to represent the format of datetime values in a DataFrame.

    Attributes:
        type (Literal["UNIX", "DATETIME"]): The type of datetime format.
        value (str): The value representing the format, e.g., "ms" for UNIX or a specific format string for DATETIME.
    """

    type: Literal["UNIX", "DATETIME"]
    value: str


@dataclass
class ResampleSettings:
    """Class to represent resampling settings for a DataFrame."""

    resample_frequency: Union[pd.Timedelta, Literal["NO_RESAMPLE"]]
