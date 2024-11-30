class Interval:
    def __init__(self, semitones: int, symbol: str, pretty_symbol: str, name: str):
        self.semitones = semitones
        self.symbol = symbol
        self.pretty_symbol = pretty_symbol
        self.name = name


intervals: list[Interval] = [
    Interval(0, '1', '', 'Unison'),
    Interval(1, 'b2', '♭2', 'Minor 2nd'),
    Interval(2, '2', '2', 'Major 2'),
    Interval(3, 'b3', '♭3', 'Minor 3rd'),
    Interval(4, '3', '3', 'Major 3rd'),
    Interval(5, '4', '4', 'Perfect 4th'),
    Interval(6, 'dim5', '°5', 'Diminished 5th'),
    Interval(7, '5', '5', 'Perfect 5th'),
    Interval(8, 'b6', '♭6', 'Minor 6th'),
    Interval(9, '6', '6', 'Major 6th'),
    Interval(10, '7', '7', 'Minor 7th'),
    Interval(11, 'M7', '△7', 'Major 7th'),
    Interval(12, '8', '8', 'Octave'),
    Interval(13, 'b9', '♭9', 'Minor 9th'),
    Interval(14, '9', '9', 'Major 9th'),
    Interval(15, '#9', '♯9', 'Augmented 9th'),
    Interval(16, '10', '10', 'Major 10th'),
    Interval(17, '11', '11', 'Perfect 11th'),
    Interval(18, '#11', '♯11', 'Augmented 11th'),
    Interval(19, '12', '12', 'Perfect 12th'),
    Interval(20, 'b13', '♭13', 'Minor 13th'),
    Interval(21, '13', '13', 'Major 13th'),
]


class Chord:
    def __init__(self, symbol: str, pretty_symbol: str, interval_symbols: list[str]):
        self.symbol = symbol
        self.pretty_symbol = (pretty_symbol,)
        self.interval_symbols = (interval_symbols,)


chords: list[Chord] = [
    ### 2-note chords
    # Power chord
    Chord('5', '5', ['1', '5']),
    ### 3-note chords
    # Basic triads
    Chord('M', 'M', ['1', '3', '5']),
    Chord('m', 'm', ['1', 'b3', '5']),
    Chord('+', '+', ['1', '3', 'b6']), # b6 is actually #5
    Chord('dim', '°', ['1', 'b3', 'b5']),
    # Suspended chords
    Chord('sus2', 'sus2', ['1', '2', '5']),
    Chord('sus4', 'sus4', ['1', '4', '5']),
    # 6th chords
    Chord('m6', 'm6', ['1', 'm3', '5', '6']),
    Chord('6', '6', ['1', '3', '5', '6']),
    # 7th chords (no 5)
    Chord('7(no5)', '7(no5)', ['1', '3', '7']),
    Chord('M7(no5)', '△7(no5)', ['1', '3', 'M3']),
    Chord('m7(no5)', 'm7(no5)', ['1', 'b3', '7']),
    Chord('mM7(no5)', 'm△7(no5)', ['1', 'b3', 'M3']),

    ### 4-note chords
    # 7th chords
    Chord('7', '7', ['1', '3', '5', '7']),
    Chord('M7', '△7', ['1', '3', '5', 'M7']),
    Chord('m7', '7', ['1', 'b3', '5', '7']),
    Chord('mM7', 'm△7', ['1', 'b3', '5', 'M7']),
    Chord('dim7', '°', ['1', 'b3', 'b5', '6']), # 6 is actually bb7
    Chord('halfdim7', 'ø7', ['1', 'b3', 'b5', '7']),
    Chord('dimM7', '°△7', ['1', 'b3', 'b5', 'M7']),
]
