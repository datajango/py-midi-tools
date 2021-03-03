import unittest
from src.midilib.midi_file import MidiFile

class TestMidiFile(unittest.TestCase):
  def test_init(self):
    mf = MidiFile()
    self.assertEqual(mf.buf, None)

  def test_read(self):
    mf = MidiFile()
    mf.read('./assets/a.mid')
    self.assertEqual(type(mf.buf), bytearray)
    self.assertEqual(len(mf.buf), 240)

  def test_read_exception_is_file(self):
    mf = MidiFile()
    with self.assertRaises(ValueError):
      mf.read('./assets/xxx.mid')

  def test_read_exception_suffix(self):
    mf = MidiFile()
    with self.assertRaises(ValueError):
      mf.read('./assets/xxx')

if __name__ == '__main__':
  unittest.main()
