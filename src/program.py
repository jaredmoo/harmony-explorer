import scale_label
import interval
import chord_label
import note
from src.relationship import relationships
import os

try:
    os.mkdir("data")
except FileExistsError:
    pass

with open("data/note_intervals.txt", "w", encoding="utf8") as f:
    for n in note.roots:
        for i in interval.index.values():
            n2 = n.add(i)
            print(f"{n} interval {i} = {n2}", file=f)

chord_label.index.dump("data/chord_labels_chromatic.txt")
for s in scale_label.index.values():
    chord_label.index.restrict(s).dump("data/chord_labels_" + s.name + ".txt")

with open("data/relationships.txt", "w", encoding="utf8") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
