"""Main script."""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from src.dataclasses.datetimeparser import DateTimeParser, DateTimeParserDATETIME, DateTimeParserUNIX
from src.dataclasses.noise import NoiseSettings, BasicNoise, WithoutNoise
from src.dataclasses.resample import ResampleSettings, BasicResample, WithoutResample
from src.dataclasses.timerange import TimeRangeSettings, ExtendedTimeRangeByLooping
from src.io_utils import load_data, save_data
from src.noise import noise_dataframe
from src.resample import resample_dataframe
from src.timerange_bounds import adjust_timerange_of_dataframe

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def main(
    input_path: Path,
    output_path: Path,
    datetime_parser: DateTimeParser,
    resample_settings: ResampleSettings,
    noise_settings: NoiseSettings,
    timerange_settings: TimeRangeSettings,
):
    """Main function to load data, resample, add noise, and save the modified DataFrame."""
    df = load_data(input_path, datetime_parser)
    df = df.set_index(datetime_parser.index_column)

    df = adjust_timerange_of_dataframe(df=df, timerange_settings=timerange_settings)
    df = resample_dataframe(df=df, resample_settings=resample_settings)
    df = noise_dataframe(df=df, noise_settings=noise_settings)

    df = df.reset_index()
    save_data(df, output_path)

    # # --- Visualization for user feedback ---
    # plt.figure(figsize=(12, 6))
    # for col in df_modified.select_dtypes(include=["number"]).columns:
    #     if col != datetime_col:
    #         plt.plot(df_modified[datetime_col], df_modified[col], label=col)
    # plt.xlabel(datetime_col)
    # plt.ylabel("Values")
    # plt.title("Resampled and Noised Data")
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    # print("OK")


# --------------------------------------------------------------------
# For typical usage, you only need to modify the section below:
# Set input/output file paths and other parameters here as needed.
# --------------------------------------------------------------------

if __name__ == "__main__":
    input_folder = INPUT_DIR / "real_cud_data"
    for file in input_folder.glob("*.csv"):
        main(
            input_path=input_folder / file.name,
            output_path=OUTPUT_DIR / file.name,
            datetime_parser=DateTimeParserUNIX(index_column="timestamp"),
            resample_settings=BasicResample("3min"),
            noise_settings=WithoutNoise(),
            timerange_settings=ExtendedTimeRangeByLooping(
                datetime_from=pd.Timestamp("2025-04-09 00:00:00+02:00"), datetime_to=pd.Timestamp("2026-04-09 00:00:00+02:00")
            ),
        )
