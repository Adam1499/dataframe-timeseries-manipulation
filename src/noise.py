"""Add noise to a DataFrame."""

import numpy as np
import pandas as pd

from src.dataclasses.noise import NoiseSettings, BasicNoise, WithoutNoise


def noise_dataframe(df: pd.DataFrame, noise_settings: NoiseSettings) -> pd.DataFrame:
    """Add noise to the DataFrame based on the specified noise settings."""
    df_modified = _add_moving_random_walk_noise(df=df, noise_settings=noise_settings)
    return df_modified


def _add_moving_random_walk_noise(df: pd.DataFrame, noise_settings: NoiseSettings, stddev_rw=0.03, stddev_wn=0.02, random_state=None, window_size=60):
    """Add moving random walk noise to the DataFrame."""
    if isinstance(noise_settings, WithoutNoise):
        return df

    elif isinstance(noise_settings, BasicNoise):
        rng = np.random.default_rng(random_state)
        df_noisy = df.copy()
        for col in df.columns:
            scale_rw = stddev_rw * df_noisy[col].std()
            scale_wn = stddev_wn * df_noisy[col].std()
            length = len(df_noisy)
            noise_rw = rng.normal(0, scale_rw, size=length)
            rolling_rw = pd.Series(noise_rw).rolling(window=window_size, min_periods=1).sum().values
            white_noise = rng.normal(0, scale_wn, size=length)
            total_noise = np.asarray(rolling_rw, dtype=float) + white_noise
            if noise_settings.skip_noise_on_zeros:
                mask = df_noisy[col] != 0
                df_noisy.loc[mask, col] += total_noise[mask]
            else:
                df_noisy[col] += total_noise
            if noise_settings.prevent_negative_values:
                df_noisy[col] = np.clip(df_noisy[col], 0, None)
        return df_noisy

    else:
        raise ValueError(f"Unknown noise_settings type: {type(noise_settings).__name__}")
