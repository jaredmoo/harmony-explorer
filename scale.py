from interval import interval, Interval
from typing import Iterable


class Scale:
    def __init__(self, name, intervals: Iterable[str] | Iterable[Interval]):
        self.name = name
        self.intervals = tuple(map(interval, intervals))


class ScaleIndex:
    def __init__(self):
        self._by_name = dict()

    def add(self, scale: Scale):
        self._by_name[scale.name] = scale

    def add_many(self, scales: Iterable[Scale]):
        for s in scales:
            self.add(s)

    def names(self):
        return self._by_name.keys()

    def values(self):
        return self._by_name.values()

    def get_name(self, name: str):
        return self._by_name[name]


scale_index = ScaleIndex()
scale_index.add_many(
    [
        Scale(
            "lydian", ["1", "2", "3", "b5", "5", "6", "7", "8", "9", "10", "#11"]
        ),  # b5 is actually #4
        Scale("ionian", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]),
        Scale("mixolydian", ["1", "2", "3", "4", "5", "6", "b7", "8", "9", "10", "11"]),
        Scale("dorian", ["1", "2", "b3", "4", "5", "6", "b7", "8", "9", "b10", "11"]),
        Scale("aeolian", ["1", "2", "b3", "4", "5", "b6", "b7", "8", "9", "b10", "11"]),
        Scale(
            "phrygian", ["1", "b2", "b3", "4", "5", "b6", "b7", "8", "b9", "b10", "11"]
        ),
        Scale(
            "locrian",
            ["1", "b2", "b3", "4", "b5", "b6", "b7", "8", "b9", "b10", "b11", "b12"],
        ),
        Scale("pentatonic", ["1", "2", "4", "5", "6", "8", "9", "11"]),
        Scale("minor pentatonic", ["1", "b3", "4", "5", "b7", "8", "b10", "11"]),
        Scale(
            "harmonic minor",
            ["1", "2", "b3", "4", "5", "b6", "b7", "7", "8", "9", "b10", "11"],
        ),
    ]
)
