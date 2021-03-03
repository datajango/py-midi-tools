from src.midilib.bit_fiddle import get_number

class MidiHeader:
    def __init__(self):
        self.id = None
        self.length = None
        self.format = None # int
        self.num_tracks = None # int
        self.division = None  # int
        self.frames_per_second = None
        self.ticks_per_frame = None
        self.ticks_per_second = None
        self.ticks_per_quarter_note = None
        self.bpm = None

    def read(self, buf):
        self.id = buf[:4]

        if self.id != b'MThd':
            msg = 'Missing id of MThd was {}'.format(self.id)
            raise ValueError(msg)

        self.length, buf = get_number(buf[4:], 4)

        if self.length != 6:
            msg = 'MThd length not 6'
            raise ValueError(msg)

        self.midi_format_type, buf = get_number(buf, 2)

        #if midi_format_type != 0 and midi_format_type != 1:  # can not handle Type 2 right now
        #    msg = 'Can only handle Midi Format Type 0 and 1'
        #    raise ValueError(msg)

        self.num_tracks, buf = get_number(buf, 2)

        # unit of time for delta timing.
        # If the value is positive, then it represents the units per beat.
        # For example, +96 would mean 96 ticks per beat.
        # If the value is negative, delta times are in SMPTE compatible units.

        self.division, buf = get_number(buf, 2)
        print(self.division)
        if self.division & 0x8000:
            self.frames_per_second = -((self.division >> 8) | -128)
            self.ticks_per_frame = self.division & 0xFF

            if self.ticks_per_frame not in [24, 25, 29, 30]:
                msg = 'Error ticks_per_frame value is {}'.format(
                    self.ticks_per_frame)
                raise ValueError(msg)

            if self.ticks_per_frame == 29:
                ticks_per_frame = 30  # drop frame
            self.ticks_per_second = ticks_per_frame * self.frames_per_second
        else:
            self.ticks_per_quarter_note = self.division & 0x7FFF

        return buf

    def log(self):
        print('Header =============================')
        print('id:', self.id)
        print('midi_format_type:', self.midi_format_type)
        print('num_tracks:', self.num_tracks)
        print('division:', self.division)
        print('ticks_per_frame:', self.ticks_per_frame)
        print('ticks_per_second:', self.ticks_per_second)
        print('ticks_per_quarter_note:', self.ticks_per_quarter_note)
