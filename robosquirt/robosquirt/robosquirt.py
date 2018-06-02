# Servo Control
import time
import wiringpi


GPIO_PIN = 18

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #14 to be a PWM output
wiringpi.pinMode(GPIO_PIN, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01

while True:
    for pulse in range(50, 250, 1):
        wiringpi.pwmWrite(GPIO_PIN, pulse)
        time.sleep(delay_period)
    for pulse in range(250, 50, -1):
        wiringpi.pwmWrite(GPIO_PIN, pulse)
        time.sleep(delay_period)
