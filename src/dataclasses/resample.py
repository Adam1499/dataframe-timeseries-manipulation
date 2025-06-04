"""Resample settings for DataFrame operations."""

import pandas as pd

from dataclasses import dataclass


@dataclass
class ResampleSettings:
    """Base class for resample settings in a DataFrame."""

    pass


@dataclass
class BasicResample(ResampleSettings):
    """Class for basic resampling with a specified frequency."""

    resample_frequency: pd.Timedelta


@dataclass
class WithoutResample(ResampleSettings):
    """Class for no resampling, used to indicate that the DataFrame should not be resampled."""

    pass
