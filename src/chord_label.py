import interval
from prettify import prettify
from scale_label import ScaleLabel
from typing import Iterable
import io


class ChordLabel:
    def __init__(self, intervals: Iterable[str | interval.Interval], symbol: str):
        self.intervals = tuple(map(interval.index.get, intervals))
        self.symbol = symbol

    def __repr__(self):
        return prettify(self.symbol) + " (" + " ".join(map(str, self.intervals)) + ")"

    def extend_with(self, extension_interval: str | interval.Interval):
        extension_interval = interval.index.get(extension_interval)

        new_intervals = self.intervals + (extension_interval,)

        new_chord_symbol = self.symbol + "(add" + extension_interval.symbol + ")"
        if (
            interval.index.get("b7") in self.intervals
            or interval.index.get("7") in self.intervals
        ):
            if "9" in extension_interval.symbol:
                # We are extending a (M)7 to a (M)(b/#)9 chord
                new_chord_symbol = self.symbol.replace("7", extension_interval.symbol)
            elif (
                interval.index.get("9") in self.intervals
                and "11" in extension_interval.symbol
            ):
                # We are extending a 9 chord to a (#)11 chord
                new_chord_symbol = self.symbol.replace("9", extension_interval.symbol)
            elif "11" == extension_interval.symbol:
                # We are extending a b/#9 chord with an 11
                if interval.index.get("b9") in self.intervals:
                    new_chord_symbol = self.symbol.replace("b9", "11(b9)")
                elif interval.index.get("#9") in self.intervals:
                    new_chord_symbol = self.symbol.replace("#9", "11(#9)")
            elif "#11" == extension_interval.symbol and (
                interval.index.get("b9") in self.intervals
                or interval.index.get("9") in self.intervals
                or interval.index.get("#9") in self.intervals
            ):
                # We are extending a (b/#)9 chord with a #11
                new_chord_symbol = self.symbol + extension_interval.symbol

        return ChordLabel(new_intervals, new_chord_symbol)

    def is_in(self, scale: ScaleLabel):
        for i in self.intervals:
            if i not in scale.intervals:
                return False
        return True


_values: list[ChordLabel] = [
    ChordLabel(("1", "3", "5"), ""),
    ChordLabel(("1", "b3", "5"), "m"),
    # power
    ChordLabel(("1", "5"), "5"),
    # no5
    ChordLabel(("1", "3"), "(no5)"),
    ChordLabel(("1", "b3"), "m(no5)"),
    # dim
    ChordLabel(("1", "b3", "b5"), "dim"),
    # aug
    ChordLabel(("1", "3", "#5"), "+"),
    # sus
    ChordLabel(("1", "2", "5"), "sus2"),
    ChordLabel(("1", "4", "5"), "sus4"),
    ### 6
    ChordLabel(("1", "3", "5", "6"), "6"),
    ChordLabel(("1", "b3", "5", "6"), "m6"),
    # sus
    ChordLabel(("1", "2", "5", "6"), "6sus2"),
    ChordLabel(("1", "4", "5", "6"), "6sus4"),
    ### 7 chords
    ChordLabel(("1", "3", "5", "b7"), "7"),
    ChordLabel(("1", "b3", "5", "b7"), "m7"),
    ChordLabel(("1", "3", "5", "7"), "M7"),
    ChordLabel(("1", "b3", "5", "7"), "mM7"),
    # power
    ChordLabel(("1", "5", "b7"), "57"),
    ChordLabel(("1", "5", "7"), "5M7"),
    # no5
    ChordLabel(("1", "3", "b7"), "(no5)7"),
    ChordLabel(("1", "b3", "b7"), "m(no5)7"),
    ChordLabel(("1", "3", "7"), "(no5)M7"),
    ChordLabel(("1", "b3", "7"), "m(no5)M7"),
    # dim
    ChordLabel(("1", "b3", "b5", "6"), "dim7"),  # 6 is actually bb7
    ChordLabel(("1", "b3", "b5", "b7"), "h7"),
    ChordLabel(("1", "b3", "b5", "b7"), "hM7"),
    # aug
    ChordLabel(("1", "3", "#5", "b7"), "+7"),
    ChordLabel(("1", "3", "#5", "7"), "+M7"),
    # sus
    ChordLabel(("1", "2", "5", "b7"), "7sus2"),
    ChordLabel(("1", "4", "5", "b7"), "7sus4"),
    ChordLabel(("1", "2", "5", "7"), "M7sus2"),
    ChordLabel(("1", "4", "5", "7"), "M7sus4"),
]

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
for c in list(_values):
    # 9 is octave away from 2, so 9 & sus2 are redundant, and #9 & sus2 are a b9 away from each other.
    # b9 & 2 are a M7 away from each other, but it's too dissonant to include for now until we have
    # better relationships implemented.
    if interval.index.get("2") in c.intervals:
        continue

    # dim chords are already dissonant enough to not extend them.
    if interval.index.get("b5") in c.intervals:
        continue

    _values.append(c.extend_with("b9"))
    _values.append(c.extend_with("9"))
    _values.append(c.extend_with("#9"))


### 11 chords
# These are technically not the correct chord symbols, since '7add9add11' should just be written as '11'.
# Just trying to keep it simple at first.
for c in list(_values):
    # See note above about not generating rare chords (i.e. with internal b9's).
    if interval.index.get("5") in c.intervals:
        continue

    # 11 is octave away from 4, so 11 & sus4 are redundant, and #11 & sus4 are b9 away from each other.
    if interval.index.get("4") in c.intervals:
        continue

    # dim chords are already dissonant enough to not extend them.
    if interval.index.get("b5") in c.intervals:
        continue

    if interval.index.get("3") not in c.intervals:
        _values.append(c.extend_with("11"))

    if interval.index.get("b3") not in c.intervals:
        _values.append(c.extend_with("#11"))


### Index
class ChordLabelIndex:
    def __init__(self, values: Iterable[ChordLabel]):
        self._by_symbol: dict[str, ChordLabel] = dict()
        self._by_intervals: dict[Iterable[interval.Interval], ChordLabel] = dict()

        for v in values:
            if v.symbol in self._by_symbol.keys():
                raise KeyError(v.symbol)
            self._by_symbol[v.symbol] = v
            self._by_intervals[v.intervals] = v

    def __repr__(self):
        return self.values().__repr__()

    def symbols(self):
        return self._by_symbol.keys()

    def intervals(self):
        return self._by_intervals.keys()

    def values(self):
        return self._by_symbol.values()

    def get_symbol(self, s: str):
        return self._by_symbol.get(s, None)

    def get_intervals(self, i: tuple[interval.Interval, ...]):
        return self._by_intervals.get(i, None)

    def restrict(self, scale: ScaleLabel):
        return ChordLabelIndex([c for c in self.values() if c.is_in(scale)])


index = ChordLabelIndex(_values)
