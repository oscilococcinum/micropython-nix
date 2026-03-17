from machine import Pin, PWM
import time

class esp32:
    def __init__(self) -> None:
        self.position = 0
        self.mode = 0
        self.increment = 1
        self.pinDir = Pin(26, Pin.OUT)
        self.motorMotion = Pin(27, Pin.OUT)
        self.pinPWMOut = PWM(Pin(25), freq=500, duty_u16=65536//(100//50))
        self.encoder_a = Pin(32, Pin.IN, Pin.PULL_UP)
        self.encoder_b = Pin(33, Pin.IN, Pin.PULL_UP)
        self.encoder_sw = Pin(19, Pin.IN, Pin.PULL_UP)

        self.pinDir.value(0)
        self.motorMotion.value(1)
        self.encoder_a.irq(trigger=Pin.IRQ_FALLING, handler=self.motionClockwise)
        self.encoder_b.irq(trigger=Pin.IRQ_FALLING, handler=self.motionCounterClockwise)
        self.encoder_sw.irq(trigger=Pin.IRQ_FALLING, handler=self.switchPush)

    def setPWMDuty(self, duty: int) -> None:
        self.pinPWMOut.duty_u16(65536//(100//duty))

    def motionClockwise(self, pin: Pin) -> None:
        freq = self.pinPWMOut.freq
        if self.encoder_a.value() == 0 and self.encoder_b.value() == 1 and not self.mode:
            self.position += self.increment
        elif self.encoder_a.value() == 0 and self.encoder_b.value() == 1 and self.mode:
            freq(freq() + self.increment)
        print(f'{self.position}, freq={freq()}Hz')

    def motionCounterClockwise(self, pin: Pin) -> None:
        freq = self.pinPWMOut.freq
        if self.encoder_a.value() == 1 and self.encoder_b.value() == 0 and not self.mode:
            self.position -= self.increment
        elif self.encoder_a.value() == 0 and self.encoder_b.value() == 1 and self.mode:
            freq(freq() - self.increment)
        print(f'{self.position}, freq={freq()}Hz')

    def switchPush(self, pin: Pin):
        if self.encoder_sw.value() == 0:
            self.mode = not self.mode
        print(f'Mode change to {self.mode}')


esp = esp32()
while True:
    while esp.position != 0 and esp.encoder_sw.value():
        time.sleep(0.05)
        if esp.position > 0:
            esp.pinDir.value(1)
            esp.motorMotion.value(0)
            esp.position -= 1
        elif esp.position < 0:
            esp.pinDir.value(0)
            esp.motorMotion.value(0)
            esp.position += 1
        print(esp.position)
    esp.motorMotion.value(1)
