from note import Note
from prettify import prettify
from scale_label import ScaleLabel


class Scale:
    def __init__(self, root: Note, scale_label: ScaleLabel):
        self.root = root
        self.scale_label = scale_label
        self.name = f"{root.name} {scale_label.name}"
        self.notes = tuple(map(root.add, scale_label.intervals))

    def __repr__(self):
        return f"{prettify(self.root.name)} {self.scale_label.name} {self.notes}"

    def contains_note_or_enharmonic(self, note: str | Note):
        note_name = note if isinstance(note, str) else note.name
        return any(note_name == n.name for n in self.notes) or any(
            note_name == e for n in self.notes for e in n.enharmonic_note_names()
        )

    def note_intervals(self):
        return zip(self.notes, self.scale_label.intervals)
