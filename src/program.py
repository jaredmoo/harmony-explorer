from chord import Chord
from chord_label import ChordLabel, ChordLabelIndex, chord_label_index
from interval import Interval, interval_index
from note import Note, root_notes, valid_notes_names
from prettify import prettify
from relationship import relationships
from scale_label import ScaleLabel, scale_label_index
from scale import Scale
import os

try:
    os.mkdir("data")
except FileExistsError:
    pass


def open_data_write(filename: str):
    return open(f"data/{filename}", "w", encoding="utf8")


# Write all notes and intervals between them
with open_data_write("note_intervals.txt") as f:
    for r in root_notes:
        for i in interval_index.values():
            n2 = r.add(i)
            print(f"{r} interval {i} = {n2}", file=f)

# Write all scales's notes
with open_data_write("scale_notes.txt") as f:
    for r in root_notes:
        for sl in scale_label_index.values():
            s = Scale(r, sl)
            print(s, file=f)

# Write each note which scales it (or its enharmonics) is in
with open_data_write("note_enharmonic_scales.txt") as f:
    for n in valid_notes_names:
        scales = [Scale(r, sl) for r in root_notes for sl in scale_label_index.values()]
        print(n, [s.name for s in scales if s.contains_note_or_enharmonic(n)], file=f)


def dump_chord_labels(cli: ChordLabelIndex, file: str):
    x = list(cli.intervals())
    x.sort()
    with open_data_write(file) as f:
        f.truncate()
        for i in x:
            print(cli.by_intervals(i), file=f)


def dump_chords(chord_label_index: ChordLabelIndex, root: Note, file: str):
    chord_labels = list(chord_label_index.values())
    chord_labels.sort()
    with open_data_write(file) as f:
        f.truncate()
        for cl in chord_labels:
            chord = Chord(root, cl)
            print(chord, file=f)


# Dump all chord labels and chordsl
dump_chord_labels(chord_label_index, "chord_labels_chromatic.txt")
for r in root_notes:
    dump_chords(chord_label_index, r, f"chords_{r.name}_chromatic.txt")

# Dump all chord labels within each scale label, and dump all chords within each scale
for sl in scale_label_index.values():
    chord_labels_in_scale = chord_label_index.restrict(sl)
    dump_chord_labels(chord_labels_in_scale, f"chord_labels_{sl.name}.txt")
    for r in root_notes:
        dump_chords(chord_labels_in_scale, r, f"chords_{r.name}_{sl.name}.txt")

# Dump all relationships
with open_data_write("relationships.txt") as f:
    f.truncate()
    for rel in relationships:
        print(rel.type.name, " ", rel.c1, " -> ", rel.c2, file=f)
