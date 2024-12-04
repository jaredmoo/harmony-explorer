from note import Note
from prettify import prettify
from scale_label import ScaleLabel


class Scale:
    def __init__(self, root: Note, scale_label: ScaleLabel):
        self.root = root
        self.scale_label = scale_label
        self.name = root.name + scale_label.name
        self.notes = tuple(map(root.add, scale_label.intervals))

    def __repr__(self):
        return f"{prettify(self.name)} {self.notes}"
