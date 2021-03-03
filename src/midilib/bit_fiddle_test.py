import unittest
from src.midilib.bit_fiddle import *

class TestBitFiddle(unittest.TestCase):

  def test_get_number(self):
    bytes = "00 00 00 06"
    buf = to_bytearay(bytes)
    length, buf = get_number(buf, 4)
    self.assertEqual(type(length), int)
    self.assertEqual(length, 6)

    bytes = "00 00 01 00"
    buf = to_bytearay(bytes)
    length, buf = get_number(buf, 4)
    self.assertEqual(length, 256)

    bytes = "00 01 00 00"
    buf = to_bytearay(bytes)
    length, buf = get_number(buf, 4)
    self.assertEqual(length, 65536)

    bytes = "01 00 00 00"
    buf = to_bytearay(bytes)
    length, buf = get_number(buf, 4)
    self.assertEqual(length, 16777216)

  def test_put_number(self):
    bytes = "00 00 00 06"
    expected = to_str(to_bytearay(bytes))
    buf = put_number(6, 4)
    self.assertEqual(buf, expected)

  def test_get_variable_length_number(self):
    bytes = "00 ff 58 04 04 02 18 08"
    buf = to_bytearay(bytes)
    length, buf = get_variable_length_number(buf[3:])
    self.assertEqual(length, 4)

  def test_put_variable_length_number(self):
    bytes = "06"
    expected = to_str(to_bytearay(bytes))
    buf = put_variable_length_number(6)
    self.assertEqual(buf, expected)

if __name__ == '__main__':
  unittest.main()
