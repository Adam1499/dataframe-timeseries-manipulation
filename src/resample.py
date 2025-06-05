"""Resampling module for time series data."""

import pandas as pd

from src.dataclasses.resample import ResampleSettings, BasicResample, WithoutResample


def resample_dataframe(df: pd.DataFrame, resample_settings: ResampleSettings) -> pd.DataFrame:
    """Resample the DataFrame to a specified frequency and interpolate missing values."""
    if isinstance(resample_settings, WithoutResample):
        return df

    elif isinstance(resample_settings, BasicResample):
        orig_freq = pd.infer_freq(pd.DatetimeIndex(df.index))
        if orig_freq is None:
            orig_freq = df.index[-1] - df.index[-2]
        new_last_time = df.index[-1] + pd.Timedelta(orig_freq)
        df.loc[new_last_time] = df.iloc[-1]
        df_resampled = df.resample(resample_settings.resample_frequency).mean()
        df_resampled = df_resampled.interpolate(method="linear")
        df_resampled = df_resampled.drop(df_resampled.index[-1])
        return df_resampled

    else:
        raise ValueError(f"Unknown resample_settings type: {type(resample_settings).__name__}")
