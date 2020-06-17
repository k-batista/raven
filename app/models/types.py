from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Months(Enum):
    JAN = auto()
    FEV = auto()
    MAR = auto()
    ABR = auto()
    MAI = auto()
    JUN = auto()
    JUL = auto()
    AGO = auto()
    SET = auto()
    OUT = auto()
    NOV = auto()
    DEZ = auto()
