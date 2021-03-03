class EnumException(Exception):
    pass

class Enumeration:

    def __init__(self, enumList):
        lookup = { }
        reverseLookup = { }
        i = 0
        uniqueNames = [ ]
        uniqueValues = [ ]

        for item in enumList:

            if type(item) == tuple:
                name = item[0]
                value = item[1]
            else:
                raise EnumException("enum requires tuples")

            if type(name) != str:
                raise EnumException("enum name is not a string: {}".format(name))

            if type(value) != int:
                raise EnumException("enum name is not a integer: {}".format(value))

            if name in uniqueNames:
                raise EnumException("enum name is not unique: {}".format(name))

            if value in uniqueValues:
                raise EnumException("enum value is not unique for {} ".format(value))

            uniqueNames.append(name)
            uniqueValues.append(value)
            lookup[name] = value
            reverseLookup[value] = name
            i = i + 1

        self.lookup = lookup
        self.reverseLookup = reverseLookup

    def __add__(self, other):
        lst = [ ]
        for k in self.lookup.keys():
            lst.append((k, self.lookup[k]))
        for k in other.lookup.keys():
            lst.append((k, other.lookup[k]))
        return Enumeration(lst)

    def hasattr(self, attr):
        return attr in self.lookup

    def has_value(self, attr):
        return attr in self.reverseLookup

    def __getattr__(self, attr):
        if not attr in self.lookup:
            raise AttributeError
        return self.lookup[attr]

    def whatis(self, value):
        if value in self.reverseLookup:
            return self.reverseLookup[value]
        else:
            self.reverseLookup[value]='Unknown'
            return 'Unknown'

channelVoiceMessages = Enumeration([
    ("NOTE_OFF", 0x80),
    ("NOTE_ON", 0x90),
    ("POLYPHONIC_KEY_PRESSURE", 0xA0),
    ("CONTROLLER_CHANGE", 0xB0),
    ("PROGRAM_CHANGE", 0xC0),
    ("CHANNEL_KEY_PRESSURE", 0xD0),
    ("PITCH_BEND", 0xE0)
])

channelModeMessages = Enumeration([
    ("ALL_SOUND_OFF", 0x78),
    ("RESET_ALL_CONTROLLERS", 0x79),
    ("LOCAL_CONTROL", 0x7A),
    ("ALL_NOTES_OFF", 0x7B),
    ("OMNI_MODE_OFF", 0x7C),
    ("OMNI_MODE_ON", 0x7D),
    ("MONO_MODE_ON", 0x7E),
    ("POLY_MODE_ON", 0x7F)
])

metaEvents = Enumeration([
    ("SEQUENCE_NUMBER", 0x00),
    ("TEXT_EVENT", 0x01),
    ("COPYRIGHT_NOTICE", 0x02),
    ("SEQUENCE_TRACK_NAME", 0x03),
    ("INSTRUMENT_NAME", 0x04),
    ("LYRIC", 0x05),
    ("MARKER", 0x06),
    ("CUE_POINT", 0x07),
    ("MIDI_CHANNEL_PREFIX", 0x20),
    ("MIDI_PORT", 0x21),
    ("END_OF_TRACK", 0x2F),
    ("SET_TEMPO", 0x51),
    ("SMTPE_OFFSET", 0x54),
    ("TIME_SIGNATURE", 0x58),
    ("KEY_SIGNATURE", 0x59),
    ("SEQUENCER_SPECIFIC_META_EVENT", 0x7F)
])

channelVoiceMessages = Enumeration([
    ("NOTE_OFF", 0x80),
    ("NOTE_ON", 0x90),
    ("POLYPHONIC_KEY_PRESSURE", 0xA0),
    ("CONTROLLER_CHANGE", 0xB0),
    ("PROGRAM_CHANGE", 0xC0),
    ("CHANNEL_KEY_PRESSURE", 0xD0),
    ("PITCH_BEND", 0xE0)
])

channelModeMessages = Enumeration([
    ("ALL_SOUND_OFF", 0x78),
    ("RESET_ALL_CONTROLLERS", 0x79),
    ("LOCAL_CONTROL", 0x7A),
    ("ALL_NOTES_OFF", 0x7B),
    ("OMNI_MODE_OFF", 0x7C),
    ("OMNI_MODE_ON", 0x7D),
    ("MONO_MODE_ON", 0x7E),
    ("POLY_MODE_ON", 0x7F)
])

metaEvents = Enumeration([
    ("SEQUENCE_NUMBER", 0x00),
    ("TEXT_EVENT", 0x01),
    ("COPYRIGHT_NOTICE", 0x02),
    ("SEQUENCE_TRACK_NAME", 0x03),
    ("INSTRUMENT_NAME", 0x04),
    ("LYRIC", 0x05),
    ("MARKER", 0x06),
    ("CUE_POINT", 0x07),
    ("MIDI_CHANNEL_PREFIX", 0x20),
    ("MIDI_PORT", 0x21),
    ("END_OF_TRACK", 0x2F),
    ("SET_TEMPO", 0x51),
    ("SMTPE_OFFSET", 0x54),
    ("TIME_SIGNATURE", 0x58),
    ("KEY_SIGNATURE", 0x59),
    ("SEQUENCER_SPECIFIC_META_EVENT", 0x7F)
])

metaEvents = Enumeration([
    ("SEQUENCE_NUMBER", 0x00),
    ("TEXT_EVENT", 0x01),
    ("COPYRIGHT_NOTICE", 0x02),
    ("SEQUENCE_TRACK_NAME", 0x03),
    ("INSTRUMENT_NAME", 0x04),
    ("LYRIC", 0x05),
    ("MARKER", 0x06),
    ("CUE_POINT", 0x07),
    ("MIDI_CHANNEL_PREFIX", 0x20),
    ("MIDI_PORT", 0x21),
    ("END_OF_TRACK", 0x2F),
    ("SET_TEMPO", 0x51),
    ("SMTPE_OFFSET", 0x54),
    ("TIME_SIGNATURE", 0x58),
    ("KEY_SIGNATURE", 0x59),
    ("SEQUENCER_SPECIFIC_META_EVENT", 0x7F)
])
