from dataclasses import dataclass
from interval import Interval
from prettify import prettify
from typing import Iterable, Self


def flatten(name: str):
    if name.endswith("#"):
        return name[:1]
    else:
        return name + "b"


def sharpen(name: str):
    if name.endswith("b"):
        return name[:1]
    else:
        return name + "#"


_semitone_note_names = {
    0: ["G##", "A", "Bbb"],
    1: ["A#", "Bb"],
    2: ["A##", "B", "Cb"],
    3: ["B#", "C", "Dbb"],
    4: ["C#", "Db"],
    5: ["C##", "D", "Ebb"],
    6: ["D#", "Eb"],
    7: ["D##", "E", "Fb"],
    8: ["E#", "F", "Gbb"],
    9: ["F#", "Gb"],
    10: ["F##", "G", "Abb"],
    11: ["G#", "Ab"],
}

# _note_name_semitones = {n: s for (s, nn) in _semitone_note_names for n in nn}
_note_name_enharmonics = {n: nn for nn in _semitone_note_names.values() for n in nn}

_rel_note_names = {
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    # "A#": ["A#", "B#", "C##", "D#", "E#", "F##", "G##"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    # "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    # "D#": ["D#", "E#", "F##", "G#", "A#", "B#", "C##"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    # "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "G#": ["G#", "A#", "B#", "C#", "D#", "E#", "F#"],
}

# Note names that we support as scale roots, for generating intervals from, etc
root_note_names = sorted(_rel_note_names.keys())

# All base note names, plus note names with 1 level of weirdness (B#, Cb, E#, Fb, and double flats / double sharps)
# that we consider to be reachable, but you wouldn't use them as a scale root
valid_notes_names = [x for xx in _semitone_note_names.values() for x in xx]

# Any other note names (including B##, Cbb, E##, Fbb, and triple flats / triple sharps)
# are considered abominations are are completel not allowed


@dataclass
class Note:
    name: str
    rel_octave: int = 0

    def __init__(self, name: str, rel_octave: int = 0):
        if name not in valid_notes_names:
            raise ValueError(f"Invalid note name {name}")

        self.name = name
        self.rel_octave = rel_octave

    def __repr__(self):
        return prettify(self.name) + (
            "↑" * self.rel_octave
            if self.rel_octave > 0
            else "↓" * (-1 * self.rel_octave) if self.rel_octave < 0 else ""
        )

    def add(self, i: Interval):
        # Don't support generating intervals from double flats or double sharps etc
        if self.name not in root_note_names:
            raise ValueError(
                f"{self.name} is a reachable note, but not supported as the base of an interval."
            )

        # determine relative octave
        (i, x_rel_octave) = i.normalize_octave()

        # determine name
        x_name = _rel_note_names[self.name][i.major_scale_degree - 1]

        # apply semitones
        if i.rel_semitones == -1:
            x_name = flatten(x_name)
        elif i.rel_semitones == 1:
            x_name = sharpen(x_name)

        # don't support generating abominations like E##, B##, Fbb, or Cbb
        if x_name not in valid_notes_names:
            raise ValueError(
                f"{str(self)} interval {i} would have resulted in unsupported note {prettify(x_name)}"
            )

        return Note(x_name, x_rel_octave)

    def enharmonic_note_names(self) -> Iterable[str]:
        return _note_name_enharmonics[self.name]

    def enharmonic_notes(self) -> Iterable[Self]:
        return [Note(n, self.rel_octave) for n in self.enharmonic_note_names()]


root_notes = [Note(n, 0) for n in root_note_names]
