from dataclasses import dataclass
from interval import Interval, interval_index
from typing import Iterable


@dataclass
class ScaleLabel:
    def __init__(self, name, intervals: Iterable[str | Interval]):
        self.name = name
        self.intervals = tuple(map(interval_index.get, intervals))

    def intervals_relative_to(self, new_root: str | Interval) -> Iterable[Interval]:
        new_root = interval_index.get(new_root)
        (new_root, _) = new_root.normalize_octave()
        result = list()
        for i in self.intervals:
            while i < new_root:
                i = i.up_octave()

            result.append(i - new_root)
        return result


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
        ScaleLabel(
            "lydian", ["1", "2", "3", "#4", "5", "6", "7", "8", "9", "10", "#11"]
        ),
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
            "locrian", ["1", "b2", "b3", "4", "b5", "b6", "b7", "8", "b9", "b10", "b11"]
        ),
        ScaleLabel("pentatonic", ["1", "2", "4", "5", "6", "8", "9", "11"]),
        ScaleLabel("minor pentatonic", ["1", "b3", "4", "5", "b7", "8", "b10", "11"]),
        ScaleLabel(
            "harmonic minor",
            ["1", "2", "b3", "4", "5", "b6", "b7", "7", "8", "9", "b10", "11"],
        ),
    ]
)
