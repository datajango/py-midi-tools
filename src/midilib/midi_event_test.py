import unittest
from src.midilib.midi_track import MidiTrack
from src.midilib.midi_event import MidiEvent

class TestEvent(unittest.TestCase):
    def test_init(self):
        track = MidiTrack(0)
        event = MidiEvent(track)