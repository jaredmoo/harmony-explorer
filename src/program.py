from scale_label import scale_index
import chord_label
from src.relationship import relationships
import os

try:
    os.mkdir("data")
except FileExistsError:
    pass

chord_label.index.dump("data/chord_labels_chromatic.txt")
for s in scale_index.values():
    chord_label.index.restrict(s).dump("data/chord_labels_" + s.name + ".txt")

with open("data/relationships.txt", "w", encoding="utf8") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
