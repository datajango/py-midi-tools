def to_bytearay(input):
    b = bytearray.fromhex(input)
    return b

def to_str(input):
    lst = [ ]
    for c in input:
        lst.append("{}".format(chr(c)))
    return "".join(lst)

# def log_as_hex(buf):
#     for c in buf:
#         print('{}'.format(hex(c)), end =" ")
#     print()

def get_number(buf, length):
    sum = 0
    for i in range(length):
        sum = (sum << 8) + buf[i]
    return int(sum), buf[length:]

def put_number(num, length):
    # MIDI uses big-endian for everything
    lst = [ ]
    for i in range(length):
        n = 8 * (length - 1 - i)
        lst.append(chr((num >> n) & 0xFF))
    return "".join(lst)

def get_variable_length_number(buf):
    sum = 0
    i = 0
    while 1:
        x = buf[i]
        i = i + 1
        sum = (sum << 7) + (x & 0x7F)
        if not (x & 0x80):
            return sum, buf[i:]

def put_variable_length_number(x):
    lst = []
    while 1:
        y, x = x & 0x7F, x >> 7
        lst.append(chr(y + 0x80))
        if x == 0:
            break
    lst.reverse()
    lst[-1] = chr(ord(lst[-1]) & 0x7f)
    return "".join(lst)

# def tempo2bpm(tempo):
#     """Convert MIDI file tempo to BPM.

#     Returns BPM as an integer or float::

#         250000 => 240
#         500000 => 120
#         1000000 => 60
#     """
#     # One minute is 60 million microseconds.
#     return (60 * 1000000) / tempo