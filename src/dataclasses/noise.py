"""Noise settings for DataFrame operations."""

from dataclasses import dataclass


@dataclass
class NoiseSettings:
    """Base class for noise settings in a DataFrame."""

    pass


@dataclass
class BasicNoise(NoiseSettings):
    """Class for basic noise settings with parameters for noise addition."""

    prevent_negative_values: bool
    skip_noise_on_zeros: bool


@dataclass
class WithoutNoise(NoiseSettings):
    """Class for no noise, used to indicate that the DataFrame should not have noise added."""

    pass
