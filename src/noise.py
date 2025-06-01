import numpy as np
import pandas as pd


def add_gaussian_noise(df: pd.DataFrame, no_negative: bool, add_noise_to_zeros: bool, stddev=0.1, random_state=None):
    rng = np.random.default_rng(random_state)
    df_noisy = df.copy()
    for col in df.columns:
        scale = stddev * df_noisy[col].std()
        noise = rng.normal(0, scale, size=len(df_noisy))
        if not add_noise_to_zeros:
            mask = df_noisy[col] != 0
            df_noisy.loc[mask, col] += noise[mask]
        else:
            df_noisy[col] += noise
        if no_negative:
            df_noisy[col] = np.clip(df_noisy[col], 0, None)
    return df_noisy


def add_moving_random_walk_noise(
    df: pd.DataFrame,
    no_negative: bool,
    add_noise_to_zeros: bool,
    stddev_rw=0.03,
    stddev_wn=0.02,
    random_state=None,
    window_size=60
):
    rng = np.random.default_rng(random_state)
    df_noisy = df.copy()
    for col in df.columns:
        scale_rw = stddev_rw * df_noisy[col].std()
        scale_wn = stddev_wn * df_noisy[col].std()
        length = len(df_noisy)
        noise_rw = rng.normal(0, scale_rw, size=length)
        rolling_rw = pd.Series(noise_rw).rolling(window=window_size, min_periods=1).sum().values
        white_noise = rng.normal(0, scale_wn, size=length)
        total_noise = rolling_rw + white_noise
        if not add_noise_to_zeros:
            mask = df_noisy[col] != 0
            df_noisy.loc[mask, col] += total_noise[mask]
        else:
            df_noisy[col] += total_noise
        if no_negative:
            df_noisy[col] = np.clip(df_noisy[col], 0, None)
    return df_noisy
