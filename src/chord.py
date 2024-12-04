from chord_label import ChordLabel
from note import Note
from prettify import prettify


class Chord:
    def __init__(self, root: Note, chord_label: ChordLabel):
        self.root = root
        self.chord_label = chord_label
        self.notes = tuple(map(root.add, chord_label.intervals))
        self.name = str(root) + chord_label.name

    def __repr__(self):
        return f"{prettify(self.name)} {self.notes}"
