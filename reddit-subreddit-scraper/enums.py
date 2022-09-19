from enum import Enum, auto


class Timeframe(Enum):
    HOUR = 3600000
    DAY = 86400000
    WEEK = 604800000
    MONTH = 2629800000
    YEAR = 31557600000
    ALL = auto()
