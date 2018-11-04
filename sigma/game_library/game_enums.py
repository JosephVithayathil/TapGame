"""Enums library"""
from enum import IntEnum


class CustomIntEnum(IntEnum):
    """Custome Int enum class to have cutom functions."""

    @classmethod
    def choices(cls):
        """Retuns list of options as enum in typle by name and code."""
        # return list(map(tuple, cls.__members__.items()))
        return [(int(code), name) for name, code in cls.__members__.items()]


class LevelEnum(CustomIntEnum):
    """Level enum."""

    LEVEL0 = 0
    LEVEL1 = 1
    LEVEL2 = 2
    LEVEl3 = 3
    LEVEl4 = 4
    LEVEl5 = 5
