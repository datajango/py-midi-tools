import unittest
from src.midilib.midi_track import MidiTrack

class TestMidiTrack(unittest.TestCase):
    def test_init(self):
        tracxk = MidiTrack(1)
