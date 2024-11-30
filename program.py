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
        Chord(("1", "b3", "b5"), "dim"),
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
        self.add_with_intervals_omitted(type, c, [i])

    def add_with_intervals_omitted(
        self, type: RelationshipType, c: Chord, ii: list[Interval]
    ):
        intervals2 = list(c.intervals)
        for i in ii:
            if i not in c.intervals:
                return
            intervals2.remove(i)

        c2 = chord_index.find_intervals(tuple(intervals2))
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
        RelationshipType("neutralize", "make major"), c, "3"
    )
    relationships.add_with_interval_omitted(
        RelationshipType("neutralize", "make minor"), c, "b3"
    )

    # sparser/denser
    relationships.add_with_interval_omitted(
        RelationshipType("sparser", "denser"), c, "5"
    )

    # Common practices on 11th chords:
    # 3 can be omitted
    #   * This reduces the character of a dominant chord
    #   * This removes the b9 dissonance between 3 & 11.
    # 5 can be omitted
    #   * This removes the b9 dissonance between 5 & #11.
    # 11th can be raised on a major chord
    #   * This removes the b9 dissonance between 3 & 11.
    # b9 can be omitted if not in a dominant chord
    #   * This removes the b9 dissonance between 1 & b9.
    #
    # Omitting only '5' is already covered by 'sparser' relationship above.
    for x in ("b3", "3"):
        for y in ("11", "#11"):
            # TODO: Add comments to these relationships
            relationships.add_with_intervals_omitted(
                RelationshipType("sparser", "denser"), c, [x]
            )
            relationships.add_with_intervals_omitted(
                RelationshipType("sparser", "denser"), c, [x, "5"]
            )
            relationships.add_with_intervals_omitted(
                RelationshipType("sparser", "denser"), c, [x, "b9"]
            )

    # Common practices on 13th chords:
    # Omit 5th and 9th, (and possibly 11th)
    # Omit 7th and 11th => equivalent to 6/9

    # extensions
    for i in ["7", "M7", "b9", "9", "#9", "11", "#11", "b13", "13"]:
        relationships.add_with_interval_omitted(
            RelationshipType("de-extend", "extend"), c, i
        )

    # interchange
    for i1, i2 in [
        ("b3", "3"),
        ("7", "M7"),
        ("b9", "9"),
        ("b9", "#9"),
        ("9", "#9"),
        ("11", "#11"),
        ("b13", "13"),
    ]:
        relationships.add_with_interval_changed(
            RelationshipType("interchange", "interchange"), c, i1, i2
        )

with open("relationships.txt", "w", encoding="utf8") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
