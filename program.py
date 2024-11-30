class Interval:
    def __init__(self, semitones: int, symbol: str):
        self.semitones = semitones
        self.symbols = symbol


intervals: list[Interval] = [
    Interval(0, '1'),
    Interval(1, 'b2'),
    Interval(2, '2'),
    Interval(3, 'b3'),
    Interval(4, '3'),
    Interval(5, '4'),
    Interval(6, 'b5'),
    Interval(7, '5'),
    Interval(8, 'b6'),
    Interval(9, '6'),
    Interval(10, '7'),
    Interval(11, 'M7'),
    Interval(12, '8'),
    Interval(13, 'b9'),
    Interval(14, '9'),
    Interval(15, '#9'),
    Interval(16, '10'),
    Interval(17, '11'),
    Interval(18, '#11'),
    Interval(19, '12'),
    Interval(20, 'b13'),
    Interval(21, '13'),
]

interval_index = dict()
for i in interval_index:
    interval_index[i.symbol] = i

class Chord:
    def __init__(self, intervals: list[str], symbol: list[str]):
        self.intervals = intervals
        self.symbol = symbol
    
    def extend_with(self, intervals, symbol: str):
        return Chord(self.intervals + intervals, self.symbol + symbol)

chord_index: dict[str,Chord] = dict()
def add_chords_to_index(cs: list[Chord]):
    for c in cs:
        if c.symbol in chord_index:
            raise KeyError(c.symbol)
        chord_index[c.symbol] = c

add_chords_to_index([
    # Power
    Chord(['1', '5'], '5'),

    ### Basic chords
    Chord(['1', '3'], '(no5)'),
    Chord(['1', 'b3'], 'm(no5)'),
    Chord(['1', '3', '5'], ''),
    Chord(['1', 'b3', '5'], 'm'),
    Chord(['1', '3', 'b6'], '+'), # b6 is actually #5
    Chord(['1', 'b3', 'b5'], 'd'),
    Chord(['1', '2', '5'], 'sus2'),
    Chord(['1', '4', '5'], 'sus4'),

    ### 6
    Chord(['1', '3', '5', '6'], '6'),
    Chord(['1', 'm3', '5', '6'], 'm6'),

    ### 7 chords
    Chord(['1', '3', '5', '7'], '7'),
    Chord(['1', 'b3', '5', '7'], 'm7'),
    Chord(['1', '3', '5', 'M7'], 'M7'),
    Chord(['1', 'b3', '5', 'M7'], 'mM7'),
    # no5
    Chord(['1', '3', '7'], '7(no5)'),
    Chord(['1', 'b3', '7'], 'm7(no5)'),
    Chord(['1', '3', 'M7'], 'M7(no5)'),
    Chord(['1', 'b3', 'M7'], 'mM7(no5)'),
    # dim
    Chord(['1', 'b3', 'b5', '6'], 'dim7'), # 6 is actually bb7
    Chord(['1', 'b3', 'b5', '7'], 'h7'),
    Chord(['1', 'b3', 'b5', '7'], 'hM7'),
])

### 9 chords
for s in ['b9', '9', '#9']:
    add_chords_to_index([
        # no 5, no 7
        Chord(['1', '3', s], '(no5)add' + s),
        Chord(['1', 'b3', s], 'm(no5)add' + s),
        # yes 5, no 7
        Chord(['1', '3', '5', s], 'add' + s),
        Chord(['1', 'b3', '5', s], 'm(add' + s),
        # no 5, yes 7
        Chord(['1', '3', '7', s], '(no5)' + s),
        Chord(['1', 'b3', '7', s], 'm(no5)' + s),
        Chord(['1', '3', 'M7', s], '(no5)M' + s),
        Chord(['1', 'b3', 'M7', s], '(no5)mM' + s),
        # yes 5, yes 7
        Chord(['1', '3', '5', '7', s], s),
        Chord(['1', 'b3', '5', '7', s], 'm' + s),
        Chord(['1', '3', '5', 'M7', s], 'M' + s),
        Chord(['1', 'b3', '5', 'M7', s], 'mM' + s),
        # dim
        Chord(['1', 'b3', 'b5', '6', s], 'd' + s), # 6 is actually bb7
        Chord(['1', 'b3', 'b5', '7', s], 'h' + s),
        Chord(['1', 'b3', 'b5', '7', s], 'hM' + s),
    ])

prettify_translation = str.maketrans(
    'dhMb#',
    '°ø△♭♯')
def prettify(s):
    return s.translate(prettify_translation)