import unittest
from src.midilib.enumeration import Enumeration, EnumException

class TestEnumeration(unittest.TestCase):

    def test_init(self):

        foo = [
            ("OFF", 0x01),
            ("ON", 0x02),
        ]

        msgs = Enumeration(foo)

        self.assertEqual(msgs.OFF, 0x01)
        self.assertEqual(msgs.ON, 0x02)

        with self.assertRaises(AttributeError ):
            self.assertEqual(msgs.FOO, 0x02)

        self.assertEqual(msgs.hasattr('OFF'), True)
        self.assertEqual(msgs.hasattr('FOO'), False)

        self.assertEqual(msgs.has_value(0x01), True)
        self.assertEqual(msgs.has_value(0x03), False)

        self.assertEqual(msgs.whatis(0x01), 'OFF')
        self.assertEqual(msgs.whatis(0x03), 'Unknown')

    def test_add(self):

        foo = [
            ("OFF", 0x01),
            ("ON", 0x02),
        ]

        msgs = Enumeration(foo)

        morefoo = [
            ("ACTIVE", 0x03),
            ("INACTIVE", 0x04),
        ]

        more_msgs = Enumeration(morefoo)

        msgs += more_msgs

        self.assertEqual(msgs.OFF, 0x01)
        self.assertEqual(msgs.ON, 0x02)
        self.assertEqual(msgs.ACTIVE, 0x03)
        self.assertEqual(msgs.INACTIVE, 0x04)


    def test_catch_require_tuple_errors(self):

        foo = [
            ("OFF", 0x01),
            ["OFF", 0x02],
        ]

        with self.assertRaises(EnumException):
            msgs = Enumeration(foo)

    def test_catch_require_name_to_be_string(self):

        foo = [
            (1, 0x01)
        ]

        with self.assertRaises(EnumException):
            msgs = Enumeration(foo)

    def test_catch_require_value_to_be_int(self):

        foo = [
            ("ON", '1')
        ]

        with self.assertRaises(EnumException):
            msgs = Enumeration(foo)

    def test_catch_unique_names_errors(self):

        foo = [
            ("OFF", 0x01),
            ("OFF", 0x02),
        ]

        with self.assertRaises(EnumException):
            msgs = Enumeration(foo)

    def test_catch_unique_values_errors(self):

        foo = [
            ("OFF", 0x01),
            ("ON", 0x01),
        ]

        with self.assertRaises(EnumException):
            msgs = Enumeration(foo)

if __name__ == '__main__':
  unittest.main()