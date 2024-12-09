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


# Write intervals
with open_data_write("intervals.txt") as f:
    for i in interval_index.values:
        print(f"{i} ({i.semitones} total semitones)", file=f)

# Write differences between intervals
with open_data_write("interval_diffs.txt") as f:
    for x in range(len(interval_index.values)):
        i1 = interval_index.values[x]
        for y in range(x, len(interval_index.values)):
            i2 = interval_index.values[y]
            print(
                f"{i1} to {i2} is a {i2 - i1}",
                file=f,
            )


# Write all notes and intervals between them
with open_data_write("note_intervals.txt") as f:
    for r in root_notes:
        for i in interval_index.values:
            n2 = r.add(i)
            print(f"{r} interval {i} = {n2}", file=f)

# Write all scales's notes
with open_data_write("scale_notes.txt") as f:
    for r in root_notes:
        for sl in scale_label_index.values():
            sl = sl.extended()
            s = Scale(r, sl)
            print(s, file=f)

# Write each note which scales it (or its enharmonics) is in
with open_data_write("note_enharmonic_scales.txt") as f:
    for n in valid_notes_names:
        scales = [
            Scale(r, sl.extended())
            for r in root_notes
            for sl in scale_label_index.values()
        ]
        print(n, [s.name for s in scales if s.contains_note_or_enharmonic(n)], file=f)


def dump_chord_labels(cli: ChordLabelIndex, file: str):
    x = list(cli.intervals())
    x.sort()
    with open_data_write(file) as f:
        f.truncate()
        for i in x:
            print(cli.by_intervals(i), file=f)


def dump_chords(sl: ScaleLabel, scale_root_note: Note, file: str):
    chord_labels = list(chord_label_index.values())
    chord_labels.sort()
    with open_data_write(file) as f:
        f.truncate()
        s = Scale(scale_root_note, sl)
        # For each note & interval in this scale that could be the root of the chord
        for chord_root_note, chord_root_interval in s.note_intervals():
            # For each potential chord
            for chord_label in chord_labels:
                # Translate the chord's intervals so that it's rooted on the chosen chord root note
                chord_semitones_transposed = chord_label.semitone_bitmap.transpose(
                    chord_root_interval.semitones
                )

                if sl.contains_enharmonics(
                    chord_semitones_transposed.normalize_octave()
                ):
                    # The chord label (translated to be rooted on this chord root note) is in the scale
                    # Print this chord, but with the note names coming from the scale
                    chord_notes = tuple(
                        [
                            n
                            for (n, i) in s.note_intervals()
                            if chord_semitones_transposed.contains_semitone(i.semitones)
                        ]
                        + [
                            n.up_octave()
                            for (n, i) in s.note_intervals()
                            if chord_semitones_transposed.down_octave().contains_semitone(
                                i.semitones
                            )
                        ]
                    )
                    print(
                        f"{chord_root_note}{prettify(chord_label.name)} {chord_notes}",
                        file=f,
                    )


# Dump all chord labels and chord
# dump_chord_labels(chord_label_index, "chord_labels_chromatic.txt")
# for r in root_notes:
#     dump_chords(
#         scale_label_index.by_name("chromatic"), r, f"chords_{r.name}_chromatic.txt"
#     )

# Dump all chord labels within each scale label, and dump all chords within each scale
for sl in scale_label_index.values():
    # chord_labels_in_scale = chord_label_index.restrict(sl)
    # dump_chord_labels(chord_labels_in_scale, f"chord_labels_{sl.name}.txt")
    for r in root_notes:
        dump_chords(sl, r, f"chords_{r.name}_{sl.name}.txt")

# Dump all relationships
with open_data_write("relationships.txt") as f:
    f.truncate()
    for rel in relationships:
        print(rel.type.name, " ", rel.c1, " -> ", rel.c2, file=f)

with open_data_write("scale_label_relative_intervals.txt") as f:
    for sl in scale_label_index.values():
        for i in sl.intervals:
            print(
                f"In {sl.name} starting from {i}, the same notes have intervals {sl.relative_to(i)}",
                file=f,
            )
