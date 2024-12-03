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


_relative_note_names = {
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
}


class Note:
    @classmethod
    def symbol(cls, name: str, octave: int):
        return name + str(octave)

    def __init__(self, name: str, octave: int, piano_key: int):
        self.name = name
        self.octave = octave
        self.symbol = Note.symbol(name, octave)
        self.piano_key = piano_key

    def __repr__(self):
        return prettify(self.id)

    def add(self, i: interval.Interval):
        x_relative_major_scale_degrees = i.major_scale_degree
        x_relative_octave = 0

        while x_relative_major_scale_degrees >= 8:
            x_relative_octave += 1
            x_relative_major_scale_degrees -= 7

        # determine higher note name
        x_name = _relative_note_names[self.name][x_relative_major_scale_degrees - 1]
        # determine higher note octave using name string comparison
        if _relative_note_names["C"].index(x_name[0]) < _relative_note_names["C"].index(
            self.name[0]
        ):
            # We went up to a next octave
            x_relative_octave += 1

        # apply semitones
        if i.rel_semitones == -1:
            x_name = flatten(x_name)
        elif i.rel_semitones == 1:
            x_name = sharpen(x.name)

        return Note(
            x_name, self.octave + x_relative_octave, self.piano_key + i.semitones
        )


class NoteIndex:
    def __init__(self):
        self._by_symbol = dict()

    def get_name_and_octave(self, name: str, octave: int):
        return self.get_id(Note.symbol(name, octave))

    def get_symbol(self, symbol):
        return self._by_symbol(symbol)

    def get_name_octave(self, name: str, octave: int):
        return self._by_symbol(Note.id(name, octave))

    def _add(self, name: str, octave: int, semitones: int):
        n = Note(name, octave, semitones)
        self._by_symbol[n.symbol] = n

    def values(self):
        return self._by_symbol.values()


index = NoteIndex()
for o in range(1, 6):
    pk = 12 * (o - 1)
    # A
    index._add("A", o - 1, 1 + pk)
    # Bb
    index._add("A#", o - 1, 2 + pk)
    index._add("Bb", o - 1, 2 + pk)
    # B
    index._add("A##", o - 1, 3 + pk)
    index._add("B", o - 1, 3 + pk)
    index._add("Cb", o - 1, 3 + pk)
    # C
    index._add("B#", o - 1, 4 + pk)
    index._add("C", o, 4 + pk)
    index._add("Dbb", o, 4 + pk)
    # C#
    index._add("C#", o, 5 + pk)
    index._add("Db", o, 5 + pk)
    # D
    index._add("C##", o, 6 + pk)
    index._add("D", o, 6 + pk)
    index._add("Ebb", o, 6 + pk)
    # D#
    index._add("D#", o, 7 + pk)
    index._add("Eb", o, 7 + pk)
    # E
    index._add("D##", o, 8 + pk)
    index._add("E", o, 8 + pk)
    index._add("Fb", o, 8 + pk)
    # F
    index._add("E#", o, 9 + pk)
    index._add("F", o, 9 + pk)
    index._add("Gbb", o, 9 + pk)
    # F#
    index._add("F#", o, 10 + pk)
    index._add("F", o, 10 + pk)
    index._add("Gbb", o, 10 + pk)
    # G
    index._add("F##", o, 11 + pk)
    index._add("G", o, 11 + pk)
    index._add("Abb", o, 11 + pk)
    # G#
    index._add("G#", o, 12 + pk)
    index._add("Ab", o, 12 + pk)
