from prettify import prettify


class Interval:
    def __init__(self, semitones: int, symbol: str):
        self.semitones = semitones
        self.symbol = symbol
        self.pretty = prettify(symbol)

    def __repr__(self):
        return self.pretty

    def __lt__(self, other):
        if self.semitones != other.semitones:
            return self.semitones < other.semitones
        else:
            # semitones are equal
            return self.symbol < other.symbol


_intervals: list = [
    Interval(0, "1"),
    Interval(1, "b2"),
    Interval(2, "2"),
    Interval(3, "b3"),
    Interval(4, "3"),
    Interval(5, "4"),
    Interval(6, "b5"),
    Interval(7, "5"),
    Interval(8, "#5"),
    Interval(8, "b6"),
    Interval(9, "6"),
    Interval(10, "b7"),
    Interval(11, "7"),
    Interval(12, "8"),
    Interval(13, "b9"),
    Interval(14, "9"),
    Interval(15, "#9"),
    Interval(16, "10"),
    Interval(17, "11"),
    Interval(18, "#11"),
    Interval(19, "12"),
    Interval(20, "b13"),
    Interval(21, "13"),
]

_interval_index = dict()
for i in _intervals:
    _interval_index[i.symbol] = i


def interval(symbol: str):
    return _interval_index[symbol]
