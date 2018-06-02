import logging
import RPi.GPIO as GPIO
import time


def make_do():
    GPIO.setmode(GPIO.BCM)

    TRIG = 23
    ECHO = 24

    logging.info("Distance Measurement In Progress")

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    logging.info("Waiting For Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start, pulse_end = 0, 0
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    logging.info("Distance:", distance, "cm")

    GPIO.cleanup()


if __name__ == "__main__":
    import sys

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s -  %(levelname)s - %(name)s - %(message)s"
    )
    make_do()
