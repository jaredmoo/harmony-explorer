from interval import Interval, interval_index
from typing import Iterable, Self


class IntervalSet:
    def __init__(self, intervals: Iterable[str | Interval]):
        self.intervals = tuple(sorted(map(interval_index.get, intervals)))
        self.semitone_bitmap = 0
        for i in self.intervals:
            self.semitone_bitmap |= 1 << i.semitones

    def contains_enharmonics(self, other: Self) -> bool:
        return self.semitone_bitmap & other.semitone_bitmap == other.semitone_bitmap

    def __repr__(self) -> str:
        return "(" + ", ".join(map(repr, self.intervals)) + ")"

    def __lt__(self, other: Self) -> bool:
        return self.intervals < other.intervals

    def __eq__(self, other: Self) -> bool:
        return self.intervals == other.intervals

    def enharmonic_equals(self, other: Self) -> bool:
        return self.semiton_bitmap == other.semitone_bitmap
