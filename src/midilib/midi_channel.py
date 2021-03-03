

"""
register_note() is a hook that can be overloaded from a script that
imports this module. Here is how you might do that, if you wanted to
store the notes as tuples in a list. Including the distinction
between track and channel offers more flexibility in assigning voices.
import midi_lib
notelist = [ ]
def register_note(t, c, p, v, t1, t2):
    notelist.append((t, c, p, v, t1, t2))
midi_lib.register_note = register_note
"""
def register_note(track_index, channel_index, pitch, velocity,
                  keyDownTime, keyUpTime):
    pass

class MidiChannel:
    """ A channel (together with a track) provides the continuity connecting
    a NOTE_ON event with its corresponding NOTE_OFF event. Together,
    those define the beginning and ending times for a Note."""

    def __init__(self, track, index):
        self.index = index
        self.track = track
        self.pitches = { }

    def __repr__(self):
        return "<MIDI channel %d>" % self.index

    def noteOn(self, pitch, time, velocity):
        self.pitches[pitch] = (time, velocity)

    def noteOff(self, pitch, time):
        if pitch in self.pitches:
            keyDownTime, velocity = self.pitches[pitch]
            register_note(self.track.index, self.index, pitch, velocity,
                          keyDownTime, time)
            del self.pitches[pitch]
        # The case where the pitch isn't in the dictionary is illegal,
        # I think, but we probably better just ignore it.
