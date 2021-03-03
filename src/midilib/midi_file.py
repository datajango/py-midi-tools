from pathlib import Path
from src.midilib.bit_fiddle import *
from src.midilib.enumeration import *
from src.midilib.midi_header import *
from src.midilib.midi_event import *
from src.midilib.midi_channel import *
from src.midilib.midi_track import *

class MidiFile:

    def __init__(self) -> None:
        self.buf = None
        self.filename = None
        self.header = None
        self.tracks = []
        self.error = False
        self.buf = None

    def read(self, filename):
        file = Path(filename)
        self.filename = file.resolve()

        if not self.filename.suffix == '.mid':
            msg = 'Unfortunatley {} is not a MIDI file'.format(self.filename)
            raise ValueError(msg)

        if not file.is_file():
            msg = 'Unfortunatley {} is not a file'.format(self.filename)
            raise ValueError(msg)

        f = open(filename, 'rb')
        self.buf = bytearray(f.read())
        f.close()


    def process(self):
        self.read_mthd_chunk()
        self.read_tracks()

    def read_mthd_chunk(self):
        if self.buf[:4] != b'MThd':
            msg = 'Missing MThd {}'.format(self.buf[:4])
            raise ValueError(msg)

        self.header = MidiHeader()
        self.buf = self.header.read(self.buf)
        self.header.log()

    def read_tracks(self):
        for i in range(self.header.num_tracks):
            trk = MidiTrack(i)
            self.buf = trk.read(self.buf)
            #trk.log()
            self.tracks.append(trk)
