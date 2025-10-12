from machine import Pin, PWM
import time

LED = 2
PUL = 25
DIR = 26
ENA = 27
DT = 32
CLK = 33
SW = 19
INC = 3

dirOut = Pin(DIR, Pin.OUT)
enaOut = Pin(ENA, Pin.OUT)
pulOut = PWM(Pin(PUL), freq=500 , duty_u16=65536//2)
encoder_a = Pin(DT, Pin.IN, Pin.PULL_UP)
encoder_b = Pin(CLK, Pin.IN, Pin.PULL_UP)
encoder_sw = Pin(SW, Pin.IN, Pin.PULL_UP)

dirOut.value(0)
enaOut.value(1)
position = 0
oldPosition = 0

def falling_a(pin):
    global position
    if encoder_a.value() == 0 and encoder_b.value() == 1:
        position += INC
    print(position)

def falling_b(pin):
    global position
    if encoder_a.value() == 1 and encoder_b.value() == 0:
        position -= INC
    print(position)

def rising_sw(pin):
    global oldPosition, position
    if encoder_sw.value() == 0:
        enaOut.value(1)
        position = 0
        print(f'sw = {encoder_sw.value()}')

encoder_a.irq(trigger=Pin.IRQ_FALLING, handler=falling_a)
encoder_b.irq(trigger=Pin.IRQ_FALLING, handler=falling_b)
encoder_sw.irq(trigger=Pin.IRQ_RISING, handler=rising_sw)

while True:
    while position != 0 and encoder_sw.value():
        time.sleep(0.05)
        if position > 0:
            dirOut.value(1)
            enaOut.value(0)
            position -= 1
        elif position < 0:
            dirOut.value(0)
            enaOut.value(0)
            position += 1
        print(position)
    enaOut.value(1)
