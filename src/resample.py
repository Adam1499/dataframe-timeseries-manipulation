"""Resampling module for time series data."""

import pandas as pd

from src.dto import ResampleSettings


def resample_dataframe(df: pd.DataFrame, resample_settings: ResampleSettings) -> pd.DataFrame:
    """Resample the DataFrame to a specified frequency and interpolate missing values."""
    orig_freq = pd.infer_freq(pd.DatetimeIndex(df.index))
    if orig_freq is None:
        orig_freq = df.index[-1] - df.index[-2]
    new_last_time = df.index[-1] + orig_freq
    df.loc[new_last_time] = df.iloc[-1]
    df_resampled = df.resample(resample_settings.resample_frequency).mean()
    df_resampled = df_resampled.interpolate(method="linear")
    df_resampled = df_resampled.drop(df_resampled.index[-1])
    return df_resampled
