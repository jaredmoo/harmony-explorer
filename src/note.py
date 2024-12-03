from interval import interval


def flatten(symbol: str):
    if symbol.startswith("#"):
        return symbol[1:]
    else:
        return "b" + symbol


def sharpen(symbol: str):
    if symbol.startswith("b"):
        return symbol[1:]
    else:
        return "#" + symbol


_relative_note_names = {
    "A": ["B", "C#", "D", "E", "F#", "G#"],
    "B": ["C#", "D#", "E", "F#", "G#", "A#"],
    "C": ["D", "E", "F", "G", "A", "B"],
    "D": ["E" "F#", "G", "A", "B", "C#"],
    "E": ["F#", "G#", "A", "B", "C#", "D#"],
    "F": ["G", "A", "Bb", "C", "D", "E"],
    "G": ["A", "B", "C", "D", "E", "F#"],
}
