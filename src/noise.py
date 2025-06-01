import numpy as np
import pandas as pd


def add_gaussian_noise(df: pd.DataFrame, no_negative: bool, add_noise_to_zeros: bool, stddev=0.05, random_state=None):
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
