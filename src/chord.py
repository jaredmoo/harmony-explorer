from chord_label import ChordLabel, ChordLabelIndex
from note import Note
from prettify import prettify
from typing import Iterable


class Chord:
    def __init__(self, root: Note, chord_label: ChordLabel):
        self.root = root
        self.chord_label = chord_label
        self.notes = tuple(map(root.add, chord_label.intervals))
        self.name = str(root) + chord_label.name

    def __repr__(self):
        return f"{prettify(self.name)} {self.notes}"


class ChordIndex:
    def __init__(self, root: Note, chord_label_index: ChordLabelIndex):
        self.root = root
        self._by_name: dict[str, Chord] = dict()
        # self._by_notes = dict()
        for cl in chord_label_index.values():
            c = Chord(self.root, cl)
            self._by_name[c.name] = c
            # _by_notes[c.notes] = c # this is not going to work right now because eq & hash aren't implemented

    def values(self) -> Iterable[Chord]:
        return self._by_name.values()

    def by_name(self, name: str):
        return self._by_name[name]
