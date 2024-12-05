from dataclasses import dataclass
from prettify import prettify
from typing import Iterable, Self


def _mod_div_octave(major_scale_degree: int) -> tuple[int, int]:
    if major_scale_degree < 1:
        raise ValueError(major_scale_degree)

    return ((major_scale_degree - 1) % 7 + 1, (major_scale_degree - 1) // 7)


def _total_semitones(major_scale_degree: int) -> int:
    (major_scale_degree, octave) = _mod_div_octave(major_scale_degree)
    return _major_scale_degree_semitones[major_scale_degree] + int(12 * octave)


_major_scale_degree_semitones = {
    1: 0,
    2: 2,
    3: 4,
    4: 5,
    5: 7,
    6: 9,
    7: 11,
}


@dataclass
class Interval:
    major_scale_degree: int
    rel_semitones: int

    def __init__(self, major_scale_degree: int, rel_semitones: int):
        # if major_scale_degree < 1 or major_scale_degree > 11:
        #    raise ValueError(
        #        f"Major scale degree {major_scale_degree} is not currently supported."
        #    )

        self.major_scale_degree = major_scale_degree
        self.rel_semitones = rel_semitones
        self.semitones = _total_semitones(major_scale_degree) + rel_semitones

        self.name = (
            "b" if rel_semitones == -1 else "#" if rel_semitones == 1 else ""
        ) + str(major_scale_degree)
        self.pretty = prettify(self.name)

    def __eq__(self, other: Self) -> bool:
        return (
            self.major_scale_degree == other.major_scale_degree
            and self.rel_semitones == other.rel_semitones
        )

    def __hash__(self):
        return hash((self.major_scale_degree, self.rel_semitones))

    def __repr__(self):
        return self.pretty

    def __lt__(self, other):
        if self.semitones != other.semitones:
            return self.semitones < other.semitones
        else:
            # semitones are equal
            return self.name < other.name

    def __sub__(self, other: Self) -> Self:
        # walk from 'other' up to 'self'
        rel_major_scale_degrees = 0
        rel_semitones = 0

        # Suppose we start from other = (2, 0), self = (7, 0)
        # current = (2, 0) -> diff = (1, 0)
        # current = (3, 0) -> diff = (2, 0)
        # current = (4, 0) -> diff = (3, -1)
        # current = (5, 0) -> diff = (4, 0)
        # current = (6, 0) -> diff = (5, 0)
        # current = (7, 0) -> diff = (6, 0)
        for curr_major_scale_degree in range(
            other.major_scale_degree, self.major_scale_degree + 1
        ):
            if curr_major_scale_degree in (4, 8, 11, 15):
                rel_semitones -= 1
            rel_major_scale_degrees += 1
            if rel_major_scale_degrees in (4, 8, 11, 15):
                rel_semitones += 1

        rel_semitones += self.rel_semitones
        rel_semitones -= other.rel_semitones

        return Interval(
            rel_major_scale_degrees,
            rel_semitones,
        )

    def up_octave(self) -> Self:
        return Interval(self.major_scale_degree + 7, self.rel_semitones)

    def down_octave(self) -> Self:
        return Interval(self.major_scale_degree - 7, self.rel_semitones)

    def normalize_octave(self) -> Self:
        return self.normalize_octave_ex()[0]

    def normalize_octave_ex(self) -> tuple[Self, int]:
        x_major_scale_degrees = self.major_scale_degree
        x_rel_octave = 0

        while x_major_scale_degrees >= 8:
            x_rel_octave += 1
            x_major_scale_degrees -= 7
        while x_major_scale_degrees < 0:
            x_rel_octave -= 1
            x_major_scale_degrees += 7

        return (Interval(x_major_scale_degrees, self.rel_semitones), x_rel_octave)


_values: list[Interval] = [
    Interval(1, 0),
    Interval(2, -1),
    Interval(2, 0),
    Interval(3, -1),
    Interval(3, 0),
    Interval(4, 0),
    Interval(4, 1),
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
]


### Index
class IntervalIndex:
    def __init__(self, values: Iterable[Interval]):
        self.values = list(values)
        self._by_name: dict[str, Interval] = dict()
        for v in values:
            if v.name in self._by_name.keys():
                raise KeyError(v.name)
            self._by_name[v.name] = v

    def __repr__(self):
        return self.values().__repr__()

    def get(self, x) -> Interval:
        if isinstance(x, str):
            return self._by_name[x]
        elif isinstance(x, Interval):
            return x
        else:
            raise TypeError(type(x))


interval_index = IntervalIndex(_values)
