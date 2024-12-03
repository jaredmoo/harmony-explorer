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

with open_data_write("scales.txt") as f:
    for n in note.roots:
        for s in scale_label.index.values():
            print(f"{n} {s.name}: {[n.add(i) for i in s.intervals]}", file=f)


def dump_chord_labels(chord_label_index: chord_label.ChordLabelIndex, file: str):
    x = list(chord_label_index.intervals())
    x.sort()
    with open_data_write(file) as f:
        f.truncate()
        for i in x:
            print(chord_label_index.get_intervals(i), file=f)


def dump_chords(
    chord_label_index: chord_label.ChordLabelIndex, root: note.Note, file: str
):
    x = list(chord_label_index.intervals())
    x.sort()
    with open_data_write(file) as f:
        f.truncate()
        for i in x:
            print(
                f"{n.name}{chord_label_index.get_intervals(i).symbol}",
                tuple(map(root.add, i)),
                file=f,
            )


dump_chord_labels(chord_label.index, "chord_labels_chromatic.txt")
for n in note.roots:
    dump_chords(chord_label.index, n, f"chords_{n.name}_chromatic.txt")
for s in scale_label.index.values():
    chord_labels_in_scale = chord_label.index.restrict(s)
    dump_chord_labels(chord_labels_in_scale, f"chord_labels_{s.name}.txt")
    for n in note.roots:
        dump_chords(chord_labels_in_scale, n, f"chords_{n.name}_{s.name}.txt")

with open_data_write("relationships.txt") as f:
    f.truncate()
    for r in relationships:
        print(r.type.name, " ", r.c1, " -> ", r.c2, file=f)
