from dataclasses import dataclass
from interval import Interval, interval_index
from interval_set import IntervalSet
from typing import Iterable, Self


@dataclass
class ScaleLabel(IntervalSet):
    def __init__(self, name, intervals: Iterable[str | Interval]):
        super().__init__(intervals)
        self.name = name

    def extended(self) -> Self:
        extended_intervals = [
            i.up_octave() for i in self.intervals if i.major_scale_degree < 5
        ]
        return ScaleLabel(self.name, self.intervals + tuple(extended_intervals))

    def __repr__(self) -> str:
        return f"{self.name} {self.intervals}"


class ScaleLabelIndex:
    def __init__(self):
        self._by_name = dict()

    def add(self, scale: ScaleLabel):
        self._by_name[scale.name] = scale

    def add_many(self, scales: Iterable[ScaleLabel]):
        for s in scales:
            self.add(s)

    def names(self) -> str:
        return self._by_name.keys()

    def values(self) -> Iterable[ScaleLabel]:
        return self._by_name.values()

    def by_name(self, name: str) -> ScaleLabel:
        return self._by_name[name]


scale_label_index = ScaleLabelIndex()
scale_label_index.add_many(
    [
        ScaleLabel("lydian", ["1", "2", "3", "#4", "5", "6", "7"]),
        ScaleLabel("ionian", ["1", "2", "3", "4", "5", "6", "7"]),
        ScaleLabel("mixolydian", ["1", "2", "3", "4", "5", "6", "b7"]),
        ScaleLabel("dorian", ["1", "2", "b3", "4", "5", "6", "b7"]),
        ScaleLabel("aeolian", ["1", "2", "b3", "4", "5", "b6", "b7"]),
        ScaleLabel("phrygian", ["1", "b2", "b3", "4", "5", "b6", "b7"]),
        ScaleLabel("locrian", ["1", "b2", "b3", "4", "b5", "b6", "b7"]),
        ScaleLabel("pentatonic", ["1", "2", "4", "5", "6"]),
        ScaleLabel("minor pentatonic", ["1", "b3", "4", "5", "b7"]),
        ScaleLabel("harmonic minor", ["1", "2", "b3", "4", "5", "b6", "b7", "7"]),
    ]
)
