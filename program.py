class Interval:
    def __init__(self, semitones: int, symbol: str, pretty_symbol:str=None):
        self.semitones = semitones
        self.symbols = symbol
        self.pretty_symbol = pretty_symbol or symbol


intervals: list[Interval] = [
    Interval(0, '1'),
    Interval(1, 'b2', '♭2'),
    Interval(2, '2'),
    Interval(3, 'b3', '♭3'),
    Interval(4, '3'),
    Interval(5, '4'),
    Interval(6, 'b5', '°5'),
    Interval(7, '5'),
    Interval(8, 'b6', '♭6'),
    Interval(9, '6'),
    Interval(10, '7'),
    Interval(11, 'M7', '△7'),
    Interval(12, '8'),
    Interval(13, 'b9', '♭9'),
    Interval(14, '9'),
    Interval(15, '#9', '♯9'),
    Interval(16, '10'),
    Interval(17, '11'),
    Interval(18, '#11', '♯11'),
    Interval(19, '12'),
    Interval(20, 'b13', '♭13'),
    Interval(21, '13'),
]

interval_index = dict()
for i in interval_index:
    interval_index[i.symbol] = i

class Chord:
    def __init__(self, intervals: list[str], symbol: list[str], pretty_symbol: str=None):
        self.intervals = intervals
        self.symbol = symbol
        self.pretty_symbol = pretty_symbol or symbol
    
    def extend_with(self, intervals, symbol: str, pretty_symbol: str=None):
        return Chord(self.intervals + intervals, self.symbol + symbol, self.pretty_symbol + (pretty_symbol or symbol))

chord_index: dict[str,Chord] = dict()
def add_chords_to_index(cs: list[Chord]):
    for c in cs:
        if c.symbol in chord_index:
            raise KeyError(c.symbol)
        chord_index[c.symbol] = c

add_chords_to_index([
    # Power
    Chord(['1', '5'], '5'),
    
    # no 5
    Chord(['1', '3'], '(no5)'),
    Chord(['1', 'b3'], 'm(no5)'),

    # Basic triads
    Chord(['1', '3', '5'], ''),
    Chord(['1', 'b3', '5'], 'm'),
    Chord(['1', '3', 'b6'], '+'), # b6 is actually #5
    Chord(['1', 'b3', 'b5'], 'dim', '°'),

    # Suspended
    Chord(['1', '2', '5'], 'sus2'),
    Chord(['1', '4', '5'], 'sus4'),

    # 6
    Chord(['1', '3', '5', '6'], '6'),
    Chord(['1', 'm3', '5', '6'], 'm6'),

    # dim 7 
    Chord(['1', 'b3', 'b5', '6'], 'dim7', '°7'), # 6 is actually bb7
    Chord(['1', 'b3', 'b5', '7'], 'h7', 'ø7')
])

# Build 7 chords
for c in ['(no5)', 'm(no5)', '', 'm', '+', '6', 'm6']:
    add_chords_to_index([
        chord_index[c].extend_with(['7'], '7'),
        chord_index[c].extend_with(['M7'], 'M7', '△7')
    ])

# Build 9 chords
for c in ['(no5)', 'm(no5)', '', 'm', '+', '6', 'm7']:
    add_chords_to_index([
        chord_index[c].extend_with(['7', '9'], '9'),
        chord_index[c].extend_with(['M7', '9'], 'M9', '△9'),
        chord_index[c].extend_with(['7', 'b9'], 'b9', '♭9'),
        chord_index[c].extend_with(['M7', 'b9'], 'Mb9', '△♭9'),
        chord_index[c].extend_with(['7', '#9'], '#9', '♯9'),
        chord_index[c].extend_with(['M7', '#9'], 'M#9', '△♯9'),
    ])
