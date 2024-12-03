import scale_label
import interval
import chord_label
import note
from relationship import relationships
import os

try:
    os.mkdir("data")
except FileExistsError:
    pass


def open_data_write(filename: str):
    return open(f"data/{filename}", "w", encoding="utf8")


with open_data_write("note_intervals.txt") as f:
    for n in note.roots:
        for i in interval.index.values():
            n2 = n.add(i)
            print(f"{n} interval {i} = {n2}", file=f)


def dump_chord_label_index(chord_label_index: chord_label.ChordLabelIndex, file: str):
    x = list(chord_label_index.intervals())
    x.sort()
    with open_data_write(file) as f:
        f.truncate()
        for i in x:
            print(chord_label_index.get_intervals(i), file=f)


dump_chord_label_index(chord_label.index, "chord_labels_chromatic.txt")
for s in scale_label.index.values():
    dump_chord_label_index(chord_label.index.restrict(s), f"chord_labels_{s.name}.txt")

with open_data_write("relationships.txt") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
