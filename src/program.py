from scale_label import scale_index
import interval
import chord_label
import note
from src.relationship import relationships
import os

try:
    os.mkdir("data")
except FileExistsError:
    pass


with open("data/notes.txt", "w", encoding="utf8") as f:
    for n in note.index.values():
        print(n.symbol, "\t", n.piano_key, file=f)

with open("data/note_intervals.txt", "w", encoding="utf8") as f:
    for n in note.index.values():
        for i in interval.index.values():
            try:
                n2 = n.add(i)
                print(
                    f"{n} (piano key {n.piano_key}) interval {i} = {n2} (piano key {n2.piano_key})",
                    file=f,
                )
            except IndexError:
                pass

chord_label.index.dump("data/chord_labels_chromatic.txt")
for s in scale_index.values():
    chord_label.index.restrict(s).dump("data/chord_labels_" + s.name + ".txt")

with open("data/relationships.txt", "w", encoding="utf8") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
