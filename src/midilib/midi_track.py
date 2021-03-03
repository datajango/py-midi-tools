from src.midilib.bit_fiddle import get_number
from src.midilib.enumeration import *
from src.midilib.midi_event import MidiEvent, DeltaTime
from src.midilib.midi_channel import MidiChannel

class MidiTrack:

    def __init__(self, index) -> None:
        self.id = None
        self.index = index
        self.length = None
        self.events = []
        self.channels = []
        self.length = 0
        for i in range(16):
            self.channels.append(MidiChannel(self, i+1))

    def read(self, buf):
        self.id = buf[:4]

        #log_as_hex(buf[:4])

        if self.id != b'MTrk':
            msg = 'Missing id of MTrk was {}'.format(self.id)
            raise ValueError(msg)

        self.length, buf = get_number(buf[4:], 4)

        #log_as_hex(buf[:6])

        track_buf = buf[:self.length]
        remainder = buf[self.length:]

        time = 0
        while track_buf:
            delta_t = DeltaTime(self)
            dt, track_buf = delta_t.read(track_buf)
            time = time + dt
            self.events.append(delta_t)
            e = MidiEvent(self)
            track_buf = e.read(time, track_buf)

            # for c in track_buf[0:4]:
            #     print('{}'.format(hex(c)))

            self.events.append(e)

        return remainder

    def log(self):
        print('Track =============================')
        print('id:', self.id)
        print('index:', self.index)