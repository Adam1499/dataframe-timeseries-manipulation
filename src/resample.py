import pandas as pd


def resample_dataframe(df: pd.DataFrame, output_frequency: str) -> pd.DataFrame:
    orig_freq = pd.infer_freq(df.index)
    if orig_freq is None:
        orig_freq = df.index[-1] - df.index[-2]
    new_last_time = df.index[-1] + orig_freq
    df.loc[new_last_time] = df.iloc[-1]
    df_resampled = df.resample(output_frequency).mean()
    df_resampled = df_resampled.interpolate(method="linear")
    df_resampled = df_resampled.drop(df_resampled.index[-1])
    return df_resampled
