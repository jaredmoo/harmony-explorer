
class Interval:
    def __init__(self, semitones: int, symbol: str, pretty_symbol: str, name: str):
        self.name = name
        self.symbol = symbol
        self.semitones = semitones

intervals: list[Interval] = [
    Interval(0, 'u',    '',     'Unison'),
    Interval(1, 'b2',   '♭2',   'Minor 2nd'),
    Interval(2, '2',    '2',    'Major 2'),
    Interval(3, 'b3',   '♭3',   'Minor 3rd'),
    Interval(4, '3',    '3',    'Major 3rd'),
    Interval(5, '4',    '4',    'Perfect 4th'),
    Interval(6, 'dim5', '°5',   'Diminished 5th'),
    Interval(7, '5',    '5',    'Perfect 5th'),
    Interval(8, '♭6',   'b6',   'Minor 6th'),
    Interval(9, '6',    '6',    'Major 6th',),
    Interval(10, '7',   '7',    'Minor 7th'),
    Interval(11, 'M7',  '△7',   'Major 7th'),
    Interval(12, '8',   '8',    'Octave'),
    Interval(13, 'b9',  '♭9',   'Minor 9th'),
    Interval(14, '9',   '9',    'Major 9th'),
    Interval(15, '#9',  '♯9',   'Augmented 9th'),
    Interval(16, '10',  '10',   'Major 10th'),
    Interval(17, '11',  '11',   'Perfect 11th'),
    Interval(18, '#11', '♯11',  'Augmented 11th'),
    Interval(19, '12',  '12',   'Perfect 12th'),
    Interval(20, 'b13', '♭13',  'Minor 13th'),
    Interval(21, '13',  '13',   'Major 13th'),
]
