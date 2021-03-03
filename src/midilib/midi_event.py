from src.midilib.bit_fiddle import *
from src.midilib.enumeration import *
from src.midilib.midi_header import *

class MidiEvent:

    def __init__(self, track):
        self.track = track
        self.time = None
        self.type = None
        self.channel = None
        self.pitch = None
        self.velocity = None
        self.data = None

    # def __cmp__(self, other):
    #     # assert self.time != None and other.time != None
    #     return cmp(self.time, other.time)

    def __repr__(self):
        r = ("<MidiEvent %s, t=%s, track=%s, channel=%s" %
             (self.type,
              repr(self.time),
              self.track.index,
              repr(self.channel)))
        for attrib in ["pitch", "data", "velocity"]:
            if getattr(self, attrib) != None:
                r = r + ", " + attrib + "=" + repr(getattr(self, attrib))
        return r + ">"

    def read(self, time, buf):
        global runningStatus
        self.time = time
        is_running_status = False

        # do we need to use running status?
        if not (buf[0] & 0x80):
            rs = bytearray(runningStatus)
            x = runningStatus
            y = x & 0xF0
            z = buf[0]
            is_running_status = True
            print('{}'.format(hex(x)))
        else:
            runningStatus = x = buf[0]
            y = x & 0xF0
            z = buf[1]

        #print('is_running_status={}, x={}, y={}, z={}'.format(is_running_status, hex(x),hex(y),hex(z)))

        command = x & 0x0F

        #print('is_running_status={}, command={}, x={}, y={}, z={}'.format(is_running_status, hex(command), hex(x),hex(y),hex(z)))

        if y == 0x80:
            # Note-off	2	key	velocity
            self.type = "NOTE_OFF"
            self.channel = (x & 0x0F) + 1
            channel = self.track.channels[self.channel - 1]
            self.pitch = buf[1]
            self.velocity = buf[2]

            channel.noteOff(self.pitch, self.time)

            print('time:{} {} type:{} channel:{} pitch:{} velocity:{}'.format(self.time, hex(x), self.type, hex(self.channel),
            hex(self.pitch), hex(self.velocity)))

            return buf[3:]

        elif y == 0x90:
            #0x90   Note-on	2	key	veolcity
            self.type = "NOTE_ON"
            self.channel = (x & 0x0F) + 1
            channel = self.track.channels[self.channel - 1]
            self.pitch = buf[1]
            self.velocity = buf[2]

            if self.velocity == 0:
                channel.noteOff(self.pitch, self.time)
            else:
                channel.noteOn(self.pitch, self.time, self.velocity)

            print('time:{} {} type:{} channel:{} pitch:{} velocity:{}'.format(self.time, hex(x), self.type, hex(self.channel),
            hex(self.pitch), hex(self.velocity)))

            return buf[3:]

        elif y == 0xA0:
            # Aftertouch	2	key	touch

            return buf[3:]

        elif y == 0xB0:
            # Continuous controller	2	controller #	controller value
            self.channel = (x & 0x0F) + 1
            channel = self.track.channels[self.channel - 1]
            self.type = channelModeMessages.whatis(z)
            if self.type == "LOCAL_CONTROL":
                self.data = (buf[2] == 0x7F)
            elif self.type == "MONO_MODE_ON":
                self.data = buf[2]
            elif self.type == "POLY_MODE_ON":
                self.data = buf[2]

            controller_number = buf[1]
            controller_value = buf[2]

            print('{} type:{} channel:{} controller_number:{} controller_value:{}'.format(hex(x), self.type, hex(self.channel), hex(controller_number), hex(controller_value)))
            return buf[3:]

        elif y == 0xC0:
            # Patch change	2	instrument #
            self.type = "PATCH_CHANGE"
            self.channel = (x & 0x0F) + 1
            channel = self.track.channels[self.channel - 1]

            print('{} type:{} channel:{} {} {}'.format(hex(x), self.type, hex(self.channel), hex(buf[1]), hex(buf[2])))

            return buf[3:]

        elif y == 0xD0:
            #Channel Pressure	1	pressure

            return buf[2:]

        elif y == 0xE0:
            #Pitch bend	2	lsb (7 bits)	msb (7 bits)

            return buf[3:]

        elif y == 0xF0:
            # (non-musical commands)
            if x == 0xF0 or x == 0xF7:
                self.type = {0xF0: "F0_SYSEX_EVENT", 0xF7: "F7_SYSEX_EVENT"}[x]
                length, buf = get_variable_length_number(buf[1:])
                self.data = buf[:length]
                print('{}:{}'.format(hex(x), self.data))
                return buf[length:]
            elif x == 0xFF:
                #if z == 0x03:
                #if not metaEvents.has_value(z):
                #    print("Unknown meta event: FF %02X" % z)
                    #sys.stdout.flush()
                    #raise "Unknown midi_lib event type"
                    # just ignore it?

                self.type = metaEvents.whatis(z)
                length, buf = get_variable_length_number(buf[2:])

                if self.type == 'TIME_SIGNATURE':
                    nn = int(buf[0]) # numerator of time signature
                    dd = int(buf[1]) # denominator of time signature
                    denominator = 2 ** dd
                    cc = buf[2] # number of MIDI clocks in a metronome click
                                # the number of MIDI clock ticks per click
                    bb = buf[3] # number of notated 32nd-notes in a MIDI quarter-note
                    #print('{} {} {} {} {}'.format(z, hex(z), self.type, hex(x), self.data))
                    print('TIME_SIGNATURE {}/{} {} {}'.format(nn,denominator,cc, bb))
                elif self.type == 'SEQUENCE_TRACK_NAME':
                    self.data = buf[:length]
                    text = self.data.decode("utf-8")
                    print('SEQUENCE_TRACK_NAME "{}"'.format(text))
                elif self.type == 'END_OF_TRACK':
                    print('END_OF_TRACK')
                else:
                    print('{} {} {}'.format(hex(x), hex(z), self.type))

                return buf[length:]
            else:
                print('ERROR')


        if channelVoiceMessages.has_value(y):
            self.channel = (x & 0x0F) + 1
            self.type = channelVoiceMessages.whatis(y)
            if (self.type == "PROGRAM_CHANGE" or
                    self.type == "CHANNEL_KEY_PRESSURE"):
                self.data = z
                return buf[2:]
            else:
                self.pitch = z
                self.velocity = buf[2]
                channel = self.track.channels[self.channel - 1]
                if (self.type == "NOTE_OFF" or
                        (self.velocity == 0 and self.type == "NOTE_ON")):
                    channel.noteOff(self.pitch, self.time)
                elif self.type == "NOTE_ON":
                    channel.noteOn(self.pitch, self.time, self.velocity)
                return buf[3:]
        #elif y == 0xB0 and channelModeMessages.has_value(z):
        elif y == 0xB0:
            self.channel = (x & 0x0F) + 1
            self.type = channelModeMessages.whatis(z)
            if self.type == "LOCAL_CONTROL":
                self.data = (buf[2] == 0x7F)
            elif self.type == "MONO_MODE_ON":
                self.data = buf[2]
            elif self.type == "POLY_MODE_ON":
                self.data = buf[2]
                pass # TODO figure out what todo here.
            return buf[3:]
        elif x == 0xF0 or x == 0xF7:
            self.type = {0xF0: "F0_SYSEX_EVENT",
                         0xF7: "F7_SYSEX_EVENT"}[x]
            length, buf = get_variable_length_number(buf[1:])
            self.data = buf[:length]
            return buf[length:]
        elif x == 0xFF:
            if not metaEvents.has_value(z):
                print("Unknown meta event: FF %02X" % z)
                #sys.stdout.flush()
                #raise "Unknown midi_lib event type"
                # just ignore it?

            self.type = metaEvents.whatis(z)

            length, buf = get_variable_length_number(buf[2:])
            self.data = buf[:length]
            for c in self.data:
                print('{}'.format(hex(c)))
            return buf[length:]
        else:
            msg = "Unknown event type {}".format(hex(x))
            print(msg)
            raise ValueError(msg)


    def write(self):
        sysex_event_dict = {"F0_SYSEX_EVENT": 0xF0,
                            "F7_SYSEX_EVENT": 0xF7}
        if channelVoiceMessages.hasattr(self.type):
            x = chr((self.channel - 1) +
                    getattr(channelVoiceMessages, self.type))
            if (self.type != "PROGRAM_CHANGE" and
                    self.type != "CHANNEL_KEY_PRESSURE"):
                data = chr(self.pitch) + chr(self.velocity)
            else:
                data = chr(self.data)
            return x + data
        elif channelModeMessages.hasattr(self.type):
            x = getattr(channelModeMessages, self.type)
            x = (chr(0xB0 + (self.channel - 1)) +
                 chr(x) +
                 chr(self.data))
            return x
        elif self.type in sysex_event_dict:
            buf = chr(sysex_event_dict[self.type])
            buf = buf + putVariableLengthNumber(len(self.data))
            return buf + self.data
        elif metaEvents.hasattr(self.type):
            buf = chr(0xFF) + chr(getattr(metaEvents, self.type))
            buf = buf + putVariableLengthNumber(len(self.data))
            return buf + self.data
        else:
            raise "unknown midi_lib event type: " + self.type


class DeltaTime(MidiEvent):

    type = "DeltaTime"

    def read(self, oldstr):
        self.time, newstr = get_variable_length_number(oldstr)
        return self.time, newstr

    def write(self):
        buf = putVariableLengthNumber(self.time)
        return buf