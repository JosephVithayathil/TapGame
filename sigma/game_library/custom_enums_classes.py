from enum import IntEnum

class CustomIntEnum(IntEnum):
    """Custome Int enum class to have cutom functions."""

    @classmethod
    def choices(cls):
        """Retuns list of options as enum in typle by name and code."""
        # return list(map(tuple, cls.__members__.items()))
        return [(int(code), name) for name, code in cls.__members__.items()]