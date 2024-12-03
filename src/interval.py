from typing import Iterable
from prettify import prettify


class Interval:
    def __init__(self, major_scale_degree: int, rel_semitones: int):
        self.major_scale_degree = major_scale_degree
        self.rel_semitones = rel_semitones
        self.semitones = (major_scale_degree - 1) * 2 + rel_semitones
        self.symbol = (
            "b" if rel_semitones == -1 else "#" if rel_semitones == 1 else ""
        ) + str(major_scale_degree)
        self.pretty = prettify(self.symbol)

    def __repr__(self):
        return self.pretty

    def __lt__(self, other):
        if self.semitones != other.semitones:
            return self.semitones < other.semitones
        else:
            # semitones are equal
            return self.symbol < other.symbol


_values: list[Interval] = [
    Interval(1, 0),
    Interval(2, -1),
    Interval(2, 0),
    Interval(3, -1),
    Interval(3, 0),
    Interval(4, 0),
    Interval(5, -1),
    Interval(5, 0),
    Interval(5, 1),
    Interval(6, -1),
    Interval(6, 0),
    Interval(7, -1),
    Interval(7, 0),
    Interval(8, 0),
    Interval(9, -1),
    Interval(9, 0),
    Interval(9, 1),
    Interval(10, -1),
    Interval(10, 0),
    Interval(11, -1),
    Interval(11, 0),
    Interval(11, 1),
    Interval(12, -1),
    Interval(12, 0),
    Interval(13, -1),
    Interval(13, 0),
]


### Index
class IntervalIndex:
    def __init__(self, values: Iterable[Interval]):
        self._by_symbol: dict[str, Interval] = dict()
        for v in values:
            if v.symbol in self._by_symbol.keys():
                raise KeyError(v.symbol)
            self._by_symbol[v.symbol] = v

    def __repr__(self):
        return self.values().__repr__()

    def values(self):
        return self._by_symbol.values()

    def get(self, x) -> Interval:
        if isinstance(x, str):
            return self._by_symbol[x]
        elif isinstance(x, Interval):
            return x
        else:
            raise TypeError(type(x))


index = IntervalIndex(_values)
