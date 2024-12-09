from interval import Interval, interval_index
from typing import Iterable, NewType, Self

Bitmap = NewType("Bitmap", int)


class SemitoneSet:
    def __init__(self, semitones: Iterable[int]):
        self.bitmap = 0
        for i in semitones:
            self.bitmap |= 1 << i

    def transpose(self, i: int):
        copy = SemitoneSet([])
        copy.bitmap = self.bitmap << i
        return copy

    def normalize_octave(self):
        copy = SemitoneSet([])
        copy.bitmap = (self.bitmap & 0xFFF) | (self.bitmap >> 12)
        return copy

    def contains_set(self, b2):
        return self.bitmap & b2.bitmap == b2.bitmap

    def contains_semitone(self, i):
        return self.bitmap & (1 << i) != 0


class IntervalSet:
    def __init__(self, intervals: Iterable[str | Interval]):
        self.intervals = tuple(sorted(map(interval_index.get, intervals)))
        self.semitone_bitmap = SemitoneSet([i.semitones for i in self.intervals])

    def contains_enharmonics(self, other: int | Self) -> bool:
        other_bitmap = other.semitones if isinstance(other, Interval) else other
        return self.semitone_bitmap.contains_set(other_bitmap)

    def relative_to(self, new_root: str | Interval) -> Iterable[Interval]:
        new_root = interval_index.get(new_root).normalize_octave()

        result = list()
        for i in self.intervals:
            while i < new_root:
                i = i.up_octave()

            result.append(i - new_root)

        return IntervalSet(result)

    def normalize_octave(self) -> Self:
        return IntervalSet([i.normalize_octave() for i in self.intervals])

    def __repr__(self) -> str:
        return "(" + ", ".join(map(repr, self.intervals)) + ")"

    def __lt__(self, other: Self) -> bool:
        return self.intervals < other.intervals

    def __eq__(self, other: Self) -> bool:
        return self.intervals == other.intervals
