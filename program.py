from collections import namedtuple
import io

prettify_translation = str.maketrans("hMb#", "ø△♭♯")


def prettify(s):
    return s.translate(prettify_translation).replace("dim", "°")


class Interval:
    def __init__(self, semitones: int, symbol: str):
        self.semitones = semitones
        self.symbols = symbol
        self.pretty = prettify(symbol)

    def __repr__(self):
        return self.pretty


intervals: list[Interval] = [
    Interval(0, "1"),
    Interval(1, "b2"),
    Interval(2, "2"),
    Interval(3, "b3"),
    Interval(4, "3"),
    Interval(5, "4"),
    Interval(6, "b5"),
    Interval(7, "5"),
    Interval(8, "b6"),
    Interval(9, "6"),
    Interval(10, "7"),
    Interval(11, "M7"),
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

interval_index = dict()
for i in interval_index:
    interval_index[i.symbol] = i


class Chord:
    def __init__(self, intervals: tuple[str], symbol: str):
        self.intervals = intervals
        self.symbol = symbol

    def __repr__(self):
        return prettify(self.symbol) + " (" + " ".join(self.intervals) + ")"

    def extend_with(self, interval: str, symbol: str):
        return Chord(self.intervals + (interval,), self.symbol + symbol)


class ChordIndex:
    def __init__(self):
        self._by_symbol = dict()
        self._by_intervals = dict()

    def __repr__(self):
        return self.values().__repr__()

    def add(self, chord: Chord):
        if chord.symbol in self._by_symbol.keys():
            raise KeyError(chord.symbol)
        self._by_symbol[chord.symbol] = chord
        self._by_intervals[chord.intervals] = chord

    def add_many(self, chords: list[Chord]):
        for c in chords:
            self.add(c)

    def values(self):
        return self._by_symbol.values()

    def find_symbol(self, s: str):
        return self._by_symbol.get(s, None)

    def find_intervals(self, i: tuple[str]):
        return self._by_intervals.get(i, None)

    def dump(self, file: str):
        x = list(self._by_intervals.keys())
        x.sort()
        with io.open(file, "w", encoding="utf8") as f:
            f.truncate()
            for i in x:
                print(self._by_intervals[i], file=f)


chord_index: ChordIndex = ChordIndex()


chord_index.add_many(
    [
        # basic
        Chord(("1", "3", "5"), ""),
        Chord(("1", "b3", "5"), "m"),
        # power
        Chord(("1", "5"), "5"),
        # no5
        Chord(("1", "3"), "(no5)"),
        Chord(("1", "b3"), "m(no5)"),
        # dim/aug
        Chord(("1", "b3", "b5"), "d"),
        Chord(("1", "3", "b6"), "+"),  # b6 is actually #5
        # sus
        Chord(("1", "2", "5"), "sus2"),
        Chord(("1", "4", "5"), "sus4"),
        ### 6
        Chord(("1", "3", "5", "6"), "6"),
        Chord(("1", "m3", "5", "6"), "m6"),
        ### 7 chords
        Chord(("1", "3", "5", "7"), "7"),
        Chord(("1", "b3", "5", "7"), "m7"),
        Chord(("1", "3", "5", "M7"), "M7"),
        Chord(("1", "b3", "5", "M7"), "mM7"),
        # power
        Chord(("1", "5", "7"), "57"),
        Chord(("1", "5", "M7"), "5M7"),
        # no5
        Chord(("1", "3", "7"), "(no5)7"),
        Chord(("1", "b3", "7"), "m(no5)7"),
        Chord(("1", "3", "M7"), "(no5)M7"),
        Chord(("1", "b3", "M7"), "m(no5)M7"),
        # dim
        Chord(("1", "b3", "b5", "6"), "dim7"),  # 6 is actually bb7
        Chord(("1", "b3", "b5", "7"), "h7"),
        Chord(("1", "b3", "b5", "7"), "hM7"),
    ]
)

### 9 chords
# These are technically not the correct chord symbols, since '7add9' should just be written as '9'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    for s in ["b9", "9", "#9"]:
        chord_index.add_many([c.extend_with(s, "add" + s)])

### 11 chords
# These are technically not the correct chord symbols, since '7add9add11' should just be written as '11'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    for s in ["11", "#11"]:
        chord_index.add_many([c.extend_with(s, "add" + s)])

### 13 chords
# These are technically not the correct chord symbols, since '7add9add11add13' should just be written as '11'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    for s in ["13", "b13"]:
        chord_index.add_many([c.extend_with(s, "add" + s)])

chord_index.dump("chords.txt")


class RelationshipType:
    def __init__(self, name: str, inverse_name: str):
        self.name = name
        self.inverse_name = inverse_name

    def inverse(self):
        return RelationshipType(self.inverse_name, self.name)


Relationship = namedtuple("Relationship", ["type", "c1", "c2"])


class Relationships(list):
    def __init__(self):
        self._r = list()

    def __iter__(self):
        return self._r.__iter__()

    def add(self, type: RelationshipType, c1: Chord, c2: Chord):
        self._r.append(Relationship(type, c1, c2))
        self._r.append(Relationship(type.inverse(), c2, c1))

    def add_with_interval_omitted(self, type: RelationshipType, c: Chord, i: Interval):
        if i in c.intervals:
            intervals2 = tuple_remove(c.intervals, i)
            c2 = chord_index.find_intervals(intervals2)
            if c2 is not None:
                self.add(type, c, c2)

    def add_with_interval_changed(
        self, type: RelationshipType, c: Chord, i1: Interval, i2: Interval
    ):
        if i1 in c.intervals:
            intervals2 = tuple_replace(c.intervals, i1, i2)
            c2 = chord_index.find_intervals(intervals2)
            if c2 is not None:
                self.add(type, c, c2)


def tuple_remove(t: tuple, a):
    l = list(t)
    l.remove(a)
    return tuple(l)


def tuple_replace(t: tuple, a, b):
    l = list(t)
    i = l.index(a)
    l[i] = b
    return tuple(l)


relationships = Relationships()
for c in chord_index.values():
    relationships.add_with_interval_omitted(
        RelationshipType("remove 3", "add 3"), c, "3"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove 3", "add b3"), c, "b3"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove 5", "add 5"), c, "5"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove 7", "add 7"), c, "7"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove M7", "add M7"), c, "M7"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove b9", "add b9"), c, "b9"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove 9", "add 9"), c, "9"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove #9", "add #9"), c, "#9"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove 11", "add 11"), c, "11"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove #11", "add #11"), c, "#11"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove b13", "add b13"), c, "b13"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("remove 13", "add 13"), c, "13"
    )
    relationships.add_with_interval_changed(
        RelationshipType("minor to major", "major to minor"), c, "b3", "3"
    )
    relationships.add_with_interval_changed(
        RelationshipType("7 to M7", "M7 to 7"), c, "7", "M7"
    )

with open("relationships.txt", "w", encoding="utf8") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
