"""Main script."""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from src.dto import DateTimeFormat, ResampleSettings
from src.io_utils import load_data, save_data
from src.noise import add_moving_random_walk_noise
from src.resample import resample_dataframe

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def main(
    input_path: Path,
    output_path: Path,
    datetime_col: str,
    datetime_format: DateTimeFormat,
    resample_settings: ResampleSettings,
    no_negative: bool,
    add_noise_to_zeros: bool,
):
    """Main function to load data, resample, add noise, and save the modified DataFrame."""
    df = load_data(input_path, datetime_col, datetime_format)
    df = df.set_index(datetime_col)
    df_modified = resample_dataframe(df, resample_settings)
    df_modified = add_moving_random_walk_noise(df=df_modified, no_negative=no_negative, add_noise_to_zeros=add_noise_to_zeros)
    df_modified = df_modified.reset_index()
    save_data(df_modified, output_path)

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
            datetime_col="timestamp",
            datetime_format=DateTimeFormat(type="UNIX", value="ms"),
            resample_settings=ResampleSettings(resample_frequency=pd.Timedelta(seconds=900)),
            no_negative=True,
            add_noise_to_zeros=False,
        )
