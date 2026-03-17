from machine import Pin
import time

class Esp32:
    def __init__(self) -> None:
        self.increment = 10
        self.position = 0
        self.leftOut = Pin(26, Pin.OUT)
        self.rightOut = Pin(25, Pin.OUT)
        self.encoder_a = Pin(32, Pin.IN, Pin.PULL_UP)
        self.encoder_b = Pin(33, Pin.IN, Pin.PULL_UP)
        self.encoder_sw = Pin(19, Pin.IN, Pin.PULL_UP)

        self.leftOut.value(0)
        self.rightOut.value(0)
        self.encoder_a.irq(trigger=Pin.IRQ_FALLING, handler=self.falling_a)
        self.encoder_b.irq(trigger=Pin.IRQ_FALLING, handler=self.falling_b)
        self.encoder_sw.irq(trigger=Pin.IRQ_FALLING, handler=self.falling_sw)


    def falling_a(self, pin: Pin):
        if self.encoder_a.value() == 0 and self.encoder_b.value() == 1:
            self.position += self.increment
        print(f'{self.position}')

    def falling_b(self, pin: Pin):
        if self.encoder_a.value() == 1 and self.encoder_b.value() == 0:
            self.position -= self.increment
        print(f'{self.position}')

    def falling_sw(self, pin: Pin):
        global position
        self.position = 0
        print(f'{self.position}')

esp32 = Esp32()
while True:
    while esp32.position != 0:
        time.sleep(0.2)
        if esp32.position > 0:
            esp32.rightOut.value(0)
            esp32.leftOut.value(1)
            esp32.position -= 1
        elif esp32.position < 0:
            esp32.leftOut.value(0)
            esp32.rightOut.value(1)
            esp32.position += 1
        print(esp32.position)
    esp32.leftOut.value(0)
    esp32.rightOut.value(0)
