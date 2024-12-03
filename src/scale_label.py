import interval
from typing import Iterable


class ScaleLabel:
    def __init__(self, name, intervals: Iterable[str] | Iterable[interval.Interval]):
        self.name = name
        self.intervals = tuple(map(interval.index.get, intervals))


class ScaleLabelIndex:
    def __init__(self):
        self._by_name = dict()

    def add(self, scale: ScaleLabel):
        self._by_name[scale.name] = scale

    def add_many(self, scales: Iterable[ScaleLabel]):
        for s in scales:
            self.add(s)

    def names(self):
        return self._by_name.keys()

    def values(self):
        return self._by_name.values()

    def get_name(self, name: str):
        return self._by_name[name]


index = ScaleLabelIndex()
index.add_many(
    [
        ScaleLabel(
            "lydian", ["1", "2", "3", "b5", "5", "6", "7", "8", "9", "10", "#11"]
        ),  # b5 is actually #4
        ScaleLabel("ionian", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]),
        ScaleLabel(
            "mixolydian", ["1", "2", "3", "4", "5", "6", "b7", "8", "9", "10", "11"]
        ),
        ScaleLabel(
            "dorian", ["1", "2", "b3", "4", "5", "6", "b7", "8", "9", "b10", "11"]
        ),
        ScaleLabel(
            "aeolian", ["1", "2", "b3", "4", "5", "b6", "b7", "8", "9", "b10", "11"]
        ),
        ScaleLabel(
            "phrygian", ["1", "b2", "b3", "4", "5", "b6", "b7", "8", "b9", "b10", "11"]
        ),
        ScaleLabel(
            "locrian",
            ["1", "b2", "b3", "4", "b5", "b6", "b7", "8", "b9", "b10", "b11", "b12"],
        ),
        ScaleLabel("pentatonic", ["1", "2", "4", "5", "6", "8", "9", "11"]),
        ScaleLabel("minor pentatonic", ["1", "b3", "4", "5", "b7", "8", "b10", "11"]),
        ScaleLabel(
            "harmonic minor",
            ["1", "2", "b3", "4", "5", "b6", "b7", "7", "8", "9", "b10", "11"],
        ),
    ]
)
