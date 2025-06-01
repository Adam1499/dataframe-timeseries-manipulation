import pandas as pd


def resample_dataframe(df: pd.DataFrame, output_frequency: str) -> pd.DataFrame:
    df_resampled = df.resample(output_frequency).mean()
    df_resampled = df_resampled.interpolate(method="linear")
    return df_resampled
