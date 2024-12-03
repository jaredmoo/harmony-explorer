from typing import Iterable
import interval
from collections import namedtuple
import chord_label


def _tuple_remove(t: tuple, a):
    l = list(t)
    l.remove(a)
    return tuple(l)


def _tuple_replace(t: tuple, a, b):
    l = list(t)
    i = l.index(a)
    l[i] = b
    return tuple(l)


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

    def add(
        self,
        type: RelationshipType,
        c1: chord_label.ChordLabel,
        c2: chord_label.ChordLabel,
    ):
        self._r.append(Relationship(type, c1, c2))
        self._r.append(Relationship(type.inverse(), c2, c1))

    def add_with_interval_omitted(
        self,
        type: RelationshipType,
        c: chord_label.ChordLabel,
        i: str | interval.Interval,
    ):
        self.add_with_intervals_omitted(type, c, [i])

    def add_with_intervals_omitted(
        self,
        type: RelationshipType,
        c: chord_label.ChordLabel,
        ii: Iterable[str | interval.Interval],
    ):
        ii2 = map(interval.index.get, ii)

        intervals2 = list(c.intervals)
        for i in ii2:
            if i not in c.intervals:
                return
            intervals2.remove(i)

        c2 = chord_label.index.get_intervals(tuple(intervals2))
        if c2 is not None:
            self.add(type, c, c2)

    def add_with_interval_changed(
        self,
        type: RelationshipType,
        c: chord_label.ChordLabel,
        i1: str | interval.Interval,
        i2: str | interval.Interval,
    ):
        i1 = interval.index.get(i1)
        i2 = interval.index.get(i2)
        if i1 in c.intervals:
            intervals2 = _tuple_replace(c.intervals, i1, i2)
            c2 = chord_label.index.get_intervals(intervals2)
            if c2 is not None:
                self.add(type, c, c2)


# todo relationships:
# interchange
#   major/minor to sus
#   minor to aug
# consonance/dissonance
#   add/remove note
#   remove internal b9
# slash
# substitution:
#   dominant augmented sub
#   dominant diminished sub
#   dominant tritone sub
#   functional sub (tonic/subdominant/dominant)
#   backdoor dominant sub
# invert

relationships = Relationships()
for c in chord_label.index.values():
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
