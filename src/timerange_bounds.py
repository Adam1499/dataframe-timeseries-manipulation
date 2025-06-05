import pandas as pd

from src.dataclasses.timerange import TimeRangeSettings, ExtendedTimeRangeByLooping, NoTimeRangeAdjustment


def adjust_timerange_of_dataframe(df: pd.DataFrame, timerange_settings: TimeRangeSettings) -> pd.DataFrame:
    if isinstance(timerange_settings, NoTimeRangeAdjustment):
        return df

    if isinstance(timerange_settings, ExtendedTimeRangeByLooping):
        # TODO: This is only hotfix solution.
        if timerange_settings.datetime_to <= df.index[-1]:
            df_extended = df.copy()
        else:
            delta = df.index[-1] - df.index[0]
            freq = df.index[1] - df.index[0]
            dfs = [df.copy()]
            last_index = df.index[-1]
            while timerange_settings.datetime_to > last_index:
                new_index = dfs[-1].index + delta + freq
                df_copy = df.copy()
                df_copy.index = new_index
                dfs.append(df_copy)
                last_index = df_copy.index[-1]
            df_extended = pd.concat(dfs)

        df_extended = df_extended[(df_extended.index <= timerange_settings.datetime_to) & (df_extended.index >= timerange_settings.datetime_from)]

        return df_extended
