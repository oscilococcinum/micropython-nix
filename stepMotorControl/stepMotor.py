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
DUTY = 50 #%

freq = 500 #Hz

dirOut = Pin(DIR, Pin.OUT)
enaOut = Pin(ENA, Pin.OUT)
pulOut = PWM(Pin(PUL), freq=freq, duty_u16=65536//(100//DUTY))
encoder_a = Pin(DT, Pin.IN, Pin.PULL_UP)
encoder_b = Pin(CLK, Pin.IN, Pin.PULL_UP)
encoder_sw = Pin(SW, Pin.IN, Pin.PULL_UP)

dirOut.value(0)
enaOut.value(1)
position = 0
mode = 0

def falling_a(pin):
    global position, freq
    if encoder_a.value() == 0 and encoder_b.value() == 1 and not mode:
        position += INC
    elif encoder_a.value() == 0 and encoder_b.value() == 1 and mode:
        freq += INC
    print(f'{position}, freq={freq}Hz')

def falling_b(pin):
    global position, freq
    if encoder_a.value() == 1 and encoder_b.value() == 0 and not mode:
        position -= INC
    elif encoder_a.value() == 0 and encoder_b.value() == 1 and mode:
        freq -= INC
    print(f'{position}, freq={freq}Hz')

def falling_sw(pin):
    global position, mode, freq
    if encoder_sw.value() == 0:
        mode = not mode
    if not mode:
        pulOut.freq(freq)
        print(f'Mode change to {mode}')

encoder_a.irq(trigger=Pin.IRQ_FALLING, handler=falling_a)
encoder_b.irq(trigger=Pin.IRQ_FALLING, handler=falling_b)
encoder_sw.irq(trigger=Pin.IRQ_FALLING, handler=falling_sw)

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
