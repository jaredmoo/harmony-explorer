from itertools import chain

prettify_translation = str.maketrans(
    'hMb#',
    'ø△♭♯')
def prettify(s):
    return s.translate(prettify_translation).replace('dim', '°')

class Interval:
    def __init__(self, semitones: int, symbol: str):
        self.semitones = semitones
        self.symbols = symbol
        self.pretty = prettify(symbol)
    
    def __repr__(self):
        return self.pretty

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
    def __init__(self, intervals: frozenset[str], symbol: str):
        self.intervals = intervals
        self.symbol = symbol
    
    def __repr__(self):
        return prettify(self.symbol) + ' (' + ' '.join(self.intervals) + ')'

    def extend_with(self, intervals: tuple[str], symbol: str):
        return Chord(chain(self.intervals, intervals), self.symbol + symbol)

class ChordIndex():
    def __init__(self):
        self._by_symbol = dict()
        self._by_intervals = dict()

    def __repr__(self):
        return self.values().__repr__()
    
    def add(self, chord: Chord):
        if chord.symbol in self._by_symbol.keys():
            raise KeyError(chord.symbol)
        self._by_symbol[chord.symbol] = chord
        self._by_intervals[chord.intervals] = chord

    def add_many(self, chords: list[Chord]):
        for c in chords:
            self.add(c)

    def values(self):
        return self._by_symbol.values()
    
    def find_symbol(self, s: str):
        return self._by_symbol[s]
    
    def find_intervals(self, i: tuple[str]):
        return self._by_intervals[i]

chord_index: ChordIndex = ChordIndex()


chord_index.add_many([
    # Power
    Chord(('1', '5'), '5'),

    ### Basic chords
    Chord(('1', '3'), '(no5)'),
    Chord(('1', 'b3'), 'm(no5)'),
    Chord(('1', '3', '5'), ''),
    Chord(('1', 'b3', '5'), 'm'),
    Chord(('1', '3', 'b6'), '+'), # b6 is actually #5
    Chord(('1', 'b3', 'b5'), 'd'),
    Chord(('1', '2', '5'), 'sus2'),
    Chord(('1', '4', '5'), 'sus4'),

    ### 6
    Chord(('1', '3', '5', '6'), '6'),
    Chord(('1', 'm3', '5', '6'), 'm6'),

    ### 7 chords
    Chord(('1', '3', '5', '7'), '7'),
    Chord(('1', 'b3', '5', '7'), 'm7'),
    Chord(('1', '3', '5', 'M7'), 'M7'),
    Chord(('1', 'b3', '5', 'M7'), 'mM7'),
    # no5
    Chord(('1', '3', '7'), '(no5)7'),
    Chord(('1', 'b3', '7'), 'm(no5)7'),
    Chord(('1', '3', 'M7'), '(no5)M7'),
    Chord(('1', 'b3', 'M7'), 'm(no5)M7'),
    # dim
    Chord(('1', 'b3', 'b5', '6'), 'dim7'), # 6 is actually bb7
    Chord(('1', 'b3', 'b5', '7'), 'h7'),
    Chord(('1', 'b3', 'b5', '7'), 'hM7'),
    # power
    Chord(('1', '5', '7'), '57'),
    Chord(('1', '5', 'M7'), '5M7'),
])

### 9 chords
# These are technically not the correct chord symbols, since '7add9' should just be written as '9'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    for s in ['b9', '9', '#9']:
        chord_index.add_many([
            c.extend_with((s), 'add' + s)
        ])

### 11 chords
# These are technically not the correct chord symbols, since '7add9add11' should just be written as '11'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    for s in ['11', '#11']:
        chord_index.add_many([
            c.extend_with((s), 'add' + s)
        ])

### 13 chords
# These are technically not the correct chord symbols, since '7add9add11add13' should just be written as '11'.
# Just trying to keep it simple at first.
for c in list(chord_index.values()):
    for s in ['13', 'b13']:
        chord_index.add_many([
            c.extend_with((s), 'add' + s)
        ])

class Relationship():
    def __init__():
        pass
