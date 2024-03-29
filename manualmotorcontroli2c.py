from tkinter import *
from smbus2 import SMBus
import os
import sys
import time
addr = 0x80
bus = SMBus(1)
time.sleep(1)
fired = False
def slidercontrol():
    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    master = Tk()
    angServo = Scale(master, from_=0, to=270)
    angServo.pack()
    horiMotor = Scale(master, from_=0, to=234, orient=HORIZONTAL)
    horiMotor.pack()
    fireBtn = Button(master, text='Fire', bd='5', command=firedCmd)
    fireBtn.pack()
    stopBtn = Button(master, text='Stop', bd='5', command=master.destroy)
    stopBtn.pack()
    loop = True
    prevAng = -10000
    prevHori = -10000
    while(loop):
        if prevAng != angServo.get():
            prevAng=angServo.get()
            send(2, prevAng)
        if prevHori!=horiMotor.get():
            prevHori=horiMotor.get()
            send(4,prevHori)
        # if fired:
        #     send(1, 0)
        # else:
        #     send(3, 0)
        master.update_idletasks()
        master.update()

#write to arduino
def send(addr, value):
    print(addr,value)
    bus.write_byte(addr, value)
    time.sleep(1)

def firedCmd():
    if fired:
        fired=False
    else:
        fired = True

slidercontrol()
