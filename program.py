from interval import interval, Interval
from prettify import prettify
from collections import namedtuple
import io


class Scale:
    @classmethod
    def from_symbols(cls, name, interval_symbols: list[str]):
        return Scale(name, tuple(map(interval, interval_symbols)))

    def __init__(self, name, intervals: tuple[str]):
        self.name = name
        self.intervals = intervals


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


class ChordSuffix:
    @classmethod
    def from_symbols(cls, interval_symbols: tuple[str], symbol: str):
        return ChordSuffix(tuple(map(interval, interval_symbols)), symbol)

    def __init__(self, intervals: tuple[Interval], symbol: str):
        self.intervals = intervals
        self.symbol = symbol

    def __repr__(self):
        return prettify(self.symbol) + " (" + " ".join(map(str, self.intervals)) + ")"

    def extend_with_symbol(self, extension_interval_symbol: str):
        new_intervals = self.intervals + (interval(extension_interval_symbol),)

        new_chord_symbol = self.symbol + "add" + extension_interval_symbol
        if interval("b7") in self.intervals or interval("7") in self.intervals:
            if "9" in extension_interval_symbol:
                # We are extending a (b)7 to a (b/#)9 chord
                new_chord_symbol = self.symbol.replace("7", extension_interval_symbol)
            elif interval("9") in self.intervals and "11" in extension_interval_symbol:
                # We are extending a 9 chord to an 11 chord
                new_chord_symbol = self.symbol.replace("9", extension_interval_symbol)

        return ChordSuffix(new_intervals, new_chord_symbol)

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

    def add(self, chord: ChordSuffix):
        if chord.symbol in self._by_symbol.keys():
            raise KeyError(chord.symbol)
        self._by_symbol[chord.symbol] = chord
        self._by_intervals[chord.intervals] = chord

    def add_many(self, chords: list[ChordSuffix]):
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
        ChordSuffix.from_symbols(("1", "3", "5"), ""),
        ChordSuffix.from_symbols(("1", "b3", "5"), "m"),
        # power
        ChordSuffix.from_symbols(("1", "5"), "5"),
        # no5
        ChordSuffix.from_symbols(("1", "3"), "(no5)"),
        ChordSuffix.from_symbols(("1", "b3"), "m(no5)"),
        # dim/aug
        ChordSuffix.from_symbols(("1", "b3", "b5"), "dim"),
        ChordSuffix.from_symbols(("1", "3", "b6"), "+"),
        # sus
        ChordSuffix.from_symbols(("1", "2", "5"), "sus2"),
        ChordSuffix.from_symbols(("1", "4", "5"), "sus4"),
        ### 6
        ChordSuffix.from_symbols(("1", "3", "5", "6"), "6"),
        ChordSuffix.from_symbols(("1", "b3", "5", "6"), "m6"),
        # sus
        ChordSuffix.from_symbols(("1", "2", "5", "6"), "6sus2"),
        ChordSuffix.from_symbols(("1", "4", "5", "6"), "6sus4"),
        ### 7 chords
        ChordSuffix.from_symbols(("1", "3", "5", "b7"), "7"),
        ChordSuffix.from_symbols(("1", "b3", "5", "b7"), "m7"),
        ChordSuffix.from_symbols(("1", "3", "5", "7"), "M7"),
        ChordSuffix.from_symbols(("1", "b3", "5", "7"), "mM7"),
        # power
        ChordSuffix.from_symbols(("1", "5", "b7"), "57"),
        ChordSuffix.from_symbols(("1", "5", "7"), "5M7"),
        # no5
        ChordSuffix.from_symbols(("1", "3", "b7"), "(no5)7"),
        ChordSuffix.from_symbols(("1", "b3", "b7"), "m(no5)7"),
        ChordSuffix.from_symbols(("1", "3", "7"), "(no5)M7"),
        ChordSuffix.from_symbols(("1", "b3", "7"), "m(no5)M7"),
        # dim
        ChordSuffix.from_symbols(("1", "b3", "b5", "6"), "dim7"),  # 6 is actually bb7
        ChordSuffix.from_symbols(("1", "b3", "b5", "b7"), "h7"),
        ChordSuffix.from_symbols(("1", "b3", "b5", "b7"), "hM7"),
        # sus
        ChordSuffix.from_symbols(("1", "2", "5", "b7"), "7sus2"),
        ChordSuffix.from_symbols(("1", "4", "5", "b7"), "7sus4"),
        ChordSuffix.from_symbols(("1", "2", "5", "7"), "M7sus2"),
        ChordSuffix.from_symbols(("1", "4", "5", "7"), "M7sus4"),
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
    # 9 is octave away from 2, so 9 & sus2 are redundant, and #9 & sus2 are a b9 away from each other.
    # b9 & 2 are a M7 away from each other, but it's too dissonant to include for now until we have
    # better relationships implemented.
    if interval("2") in c.intervals:
        continue

    # dim chords are already dissonant enough to not extend them.
    if interval("b5") in c.intervals:
        continue

    chord_index.add_many([c.extend_with_symbol("b9")])
    chord_index.add_many([c.extend_with_symbol("9")])
    chord_index.add_many([c.extend_with_symbol("#9")])


### 11 chords
# These are technically not the correct chord symbols, since '7add9add11' should just be written as '11'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    # See note above about not generating rare chords (i.e. with internal b9's).
    if interval("5") in c.intervals:
        continue

    # 11 is octave away from 4, so 11 & sus4 are redundant, and #11 & sus4 are b9 away from each other.
    if interval("4") in c.intervals:
        continue

    # dim chords are already dissonant enough to not extend them.
    if interval("b5") in c.intervals:
        continue

    if interval("3") not in c.intervals:
        chord_index.add_many([c.extend_with_symbol("11")])

    if interval("b3") not in c.intervals:
        chord_index.add_many([c.extend_with_symbol("#11")])

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

    def add(self, type: RelationshipType, c1: ChordSuffix, c2: ChordSuffix):
        self._r.append(Relationship(type, c1, c2))
        self._r.append(Relationship(type.inverse(), c2, c1))

    def add_with_interval_omitted(
        self, type: RelationshipType, c: ChordSuffix, i: Interval
    ):
        self.add_with_intervals_omitted(type, c, [i])

    def add_with_intervals_omitted(
        self, type: RelationshipType, c: ChordSuffix, ii: list[Interval]
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
        self, type: RelationshipType, c: ChordSuffix, i1: Interval, i2: Interval
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
