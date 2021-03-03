import unittest
from src.midilib.midi_header import MidiHeader

class TestMidiHeader(unittest.TestCase):
    def test_init(self):
        mf = MidiHeader()

    def test_read(self):
        mf = MidiHeader()
        #mf.read(self, buf)