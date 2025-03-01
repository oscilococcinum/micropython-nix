from machine import Pin, PWM

pwm2 = PWM(Pin(2), freq=25000, duty=512)  # create and configure in one go
freq_plus = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN)
freq_minus = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN)
duty_plus = Pin(16, mode=Pin.IN, pull=Pin.PULL_DOWN)
duty_minus = Pin(21, mode=Pin.IN, pull=Pin.PULL_DOWN)


while 1:
    print(f"freq: {pwm2.freq()}, duty: {pwm2.duty()}")
    if freq_plus.value() == 1 and pwm2.freq() < 40000:
        pwm2.freq(pwm2.freq() + 100)
    elif freq_minus.value() == 1 and pwm2.freq() > 100:
        pwm2.freq(pwm2.freq() - 100)
    elif duty_plus.value() == 1 and pwm2.duty() < 1023:
        pwm2.duty(pwm2.duty() + 1)
    elif duty_minus.value() == 1 and pwm2.duty() > 1:
        pwm2.duty(pwm2.duty() - 1)
