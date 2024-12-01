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
    Interval(10, "b7"),
    Interval(11, "7"),
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


class Scale:
    def __init__(self, name, intervals: list[str]):
        self.name = name
        self.intervals = tuple(intervals)


class ScaleIndex:
    def __init__(self):
        self._by_name = dict()

    def add(self, scale: Scale):
        self._by_name[scale.name] = scale

    def add_many(self, scales: list[Scale]):
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
            ["1", "b2", "b3", "4", "b5", "b6", "b7", "8", "b9", "b10", "b11", "#11"],
        ),  # #11 is actually b12
        Scale("pentatonic", ["1", "2", "4", "5", "6", "8", "9", "11"]),
        Scale("minor pentatonic", ["1", "b3", "4", "5", "b7", "8", "b10", "11"]),
        Scale(
            "harmonic minor",
            ["1", "2", "b3", "4", "5", "b6", "b7", "7", "8", "9", "b10", "11"],
        ),
    ]
)


class Chord:
    def __init__(self, intervals: tuple[str], symbol: str):
        self.intervals = intervals
        self.symbol = symbol

    def __repr__(self):
        return prettify(self.symbol) + " (" + " ".join(self.intervals) + ")"

    def extend_with(self, interval: str, symbol: str):
        return Chord(self.intervals + (interval,), self.symbol + symbol)

    def is_in(self, scale: Scale):
        for i in self.intervals:
            if i not in scale.intervals:
                return False
        return True


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

    def get_symbol(self, s: str):
        return self._by_symbol.get(s, None)

    def get_intervals(self, i: tuple[str]):
        return self._by_intervals.get(i, None)

    def dump(self, file: str):
        x = list(self._by_intervals.keys())
        x.sort()
        with io.open(file, "w", encoding="utf8") as f:
            f.truncate()
            for i in x:
                print(self._by_intervals[i], file=f)

    def restrict(self, scale: Scale):
        chords = [c for c in self.values() if c.is_in(scale)]
        restricted = ChordIndex()
        restricted.add_many(chords)
        return restricted


chord_index: ChordIndex = ChordIndex()
chord_index.add_many(
    [
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
        # sus
        Chord(("1", "2", "5", "6"), "6sus2"),
        Chord(("1", "4", "5", "6"), "6sus4"),
        ### 7 chords
        Chord(("1", "3", "5", "b7"), "7"),
        Chord(("1", "b3", "5", "b7"), "m7"),
        Chord(("1", "3", "5", "7"), "M7"),
        Chord(("1", "b3", "5", "7"), "mM7"),
        # power
        Chord(("1", "5", "b7"), "57"),
        Chord(("1", "5", "7"), "5M7"),
        # no5
        Chord(("1", "3", "b7"), "(no5)7"),
        Chord(("1", "b3", "b7"), "m(no5)7"),
        Chord(("1", "3", "7"), "(no5)M7"),
        Chord(("1", "b3", "7"), "m(no5)M7"),
        # dim
        Chord(("1", "b3", "b5", "6"), "dim7"),  # 6 is actually bb7
        Chord(("1", "b3", "b5", "b7"), "h7"),
        Chord(("1", "b3", "b5", "b7"), "hM7"),
        # sus
        Chord(("1", "2", "5", "b7"), "7sus2"),
        Chord(("1", "4", "5", "b7"), "7sus4"),
        Chord(("1", "2", "5", "7"), "M7sus2"),
        Chord(("1", "4", "5", "7"), "M7sus4"),
    ]
)

### Extensions
#
# What I would like to do, is to generate ALL extensions, but then:
# * Make the less common combinations less accessible via relationships.
#   For example, different relationships could have higher or lower ranking,
#   which could then guide you more towards more common chords or common
#   practices (e.g. omitting 5's, and )
# * Make the chord's internal intervals visible, especially b9's, which guide
#   you towards removing the 'avoid notes'.
#
# Common practices on extensions based on the chord's function:
#   * Piano with Johnny - Chord Substitution: 5 Levels from Beginner to Pro https://www.youtube.com/watch?v=IGBcnFSJb4c
#       * On a major chord, add 6, 7, or 9
#       * On a minor chord, add b7, 9, or 11
#       * On a dominant 7 chord, add 9, b9, #9, #11, b13, or 13.
#   * Using altered chord extensions https://www.reddit.com/r/musictheory/comments/fupzzd/comment/fme5c0q
#       * The alterations are all about voice leading. This is why you are more free to use alterations
#         on dominant chords, since those chords are leading to a clear target.
#
# Common practices on 9th chords:
#   * 5 can be omitted.
#
# Common practices on 11th chords:
#   * Woochia on 11th chords https://www.youtube.com/watch?v=gnLzPAEYcVE
#   * https://en.m.wikipedia.org/wiki/Eleventh_chord
# 3 can be omitted
#   * This reduces the character of a dominant chord
#   * This removes the b9 dissonance between 3 & 11.
# 5 can be omitted
#   * This removes the b9 dissonance between 5 & #11.
# 11th can be raised on a major chord
#   * This removes the b9 dissonance between 3 & 11.
# b9 can be omitted if not in a dominant chord
#   * This removes the b9 dissonance between 1 & b9.
# Also note, that when 3 & 5 are emitted, 7 & 9 & 11 form a simple triad,
# so this is exactly equivalent to a simple triad slash chord.
#
# Common practices on 13th chords:
#   * Woochia on 13th chords https://www.youtube.com/watch?v=DFkSSkWhZk0
#   * Why is there no straightforward way to play a 13th chord https://www.reddit.com/r/musictheory/comments/1161296/comment/j94k6ps
# Omit 5th and 9th, (and possibly 11th)
# Omit 7th and 11th => equivalent to 6/9

### 9 chords
# These are technically not the correct chord symbols, since '7add9' should just be written as '9'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    # See note above about not generating rare chords.
    chord_index.add_many([c.extend_with("9", "add9")])


### 11 chords
# These are technically not the correct chord symbols, since '7add9add11' should just be written as '11'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    # See note above about not generating rare chords.
    if "5" in c.intervals:
        continue

    if "3" not in c.intervals:
        chord_index.add_many([c.extend_with("11", "add11")])

    if "b3" not in c.intervals:
        chord_index.add_many([c.extend_with("#11", "add#11")])

chord_index.dump("chords_all.txt")
for s in scale_index.values():
    chord_index.restrict(s).dump("chords_" + s.name + ".txt")


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

        c2 = chord_index.get_intervals(tuple(intervals2))
        if c2 is not None:
            self.add(type, c, c2)

    def add_with_interval_changed(
        self, type: RelationshipType, c: Chord, i1: Interval, i2: Interval
    ):
        if i1 in c.intervals:
            intervals2 = tuple_replace(c.intervals, i1, i2)
            c2 = chord_index.get_intervals(intervals2)
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

    # extensions
    for i in ["b7", "7", "b9", "9", "#9", "11", "#11", "b13", "13"]:
        relationships.add_with_interval_omitted(
            RelationshipType("de-extend", "extend"), c, i
        )

    # interchange
    for i1, i2 in [
        ("b3", "3"),
        ("b7", "7"),
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
