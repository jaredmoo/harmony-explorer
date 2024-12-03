from prettify import prettify
import interval


def flatten(symbol: str):
    if symbol.endswith("#"):
        return symbol[:1]
    else:
        return symbol + "b"


def sharpen(symbol: str):
    if symbol.endswith("b"):
        return symbol[:1]
    else:
        return symbol + "#"


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
base_names = sorted(_rel_note_names.keys())

# All base note names, plus note names with 1 level of weirdness (B#, Cb, E#, Fb, and double flats / double sharps)
# that we consider to be reachable, but you wouldn't use them as a scale root
reachable_names = [
    "Abb",
    "Ab",
    "A",
    "A#",
    "A##",
    "Bbb",
    "Bb",
    "B",
    "B#",  # B## is abomination
    "Cb",
    "C",
    "C#",
    "C##",  # Cbb is abomination
    "Dbb",
    "Db",
    "D",
    "D#",
    "D##",
    "Ebb",
    "Eb",
    "E",
    "E#",  # E## is abomination
    "Fb",
    "F",
    "F#",
    "F##",  # F## is abomination
    "Gbb",
    "Gb",
    "G",
    "G#",
    "G##",
]

# Any other note names (including B##, Cbb, E##, Fbb, and triple flats / triple sharps)
# are considered abominations are are completel not allowed


class Note:
    def __init__(self, name: str, rel_octave: int = 0):
        if name not in reachable_names:
            raise ValueError(f"Invalid note name {name}")

        self.name = name
        self.rel_octave = rel_octave

    def __repr__(self):
        return prettify(self.name) + (
            "↑" * self.rel_octave
            if self.rel_octave > 0
            else "↓" * (-1 * self.rel_octave) if self.rel_octave < 0 else ""
        )

    def add(self, i: interval.Interval):
        # Don't support generating intervals from double flats or double sharps etc
        if self.name not in base_names:
            raise ValueError(
                f"{self.name} is a reachable note, but not supported as the base of an interval."
            )

        # determine relative octave
        x_rel_major_scale_degrees = i.major_scale_degree
        x_rel_octave = 0

        while x_rel_major_scale_degrees >= 8:
            x_rel_octave += 1
            x_rel_major_scale_degrees -= 7

        # determine name
        x_name = _rel_note_names[self.name][x_rel_major_scale_degrees - 1]

        # apply semitones
        if i.rel_semitones == -1:
            x_name = flatten(x_name)
        elif i.rel_semitones == 1:
            x_name = sharpen(x_name)

        # don't support generating abominations like E##, B##, Fbb, or Cbb
        if x_name not in reachable_names:
            raise ValueError(
                f"{str(self)} interval {i} would have resulted in unsupported note {prettify(x_name)}"
            )

        return Note(x_name, x_rel_octave)


roots = [Note(n, 0) for n in base_names]
