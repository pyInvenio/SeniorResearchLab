from smbus import SMBus

addr = 0x8
bus = smbus.SMBus(1)

# How to write to the raspberry pi
def send(addr, value):
    # Value Coded message
    # first digit is the identifier used to chose what method will be selected
    # Current Method options: 1: Fire, 2: Vertical angle, 3: Stop Fire, 4: Shutdown
    # second digit is 0 by default
    # third digit is an argument for the vertical angle method
    # Ex. 90 => 090
    bus.write_byte(addr, "" + value)