import logging

import RPi.GPIO as GPIO
import time

PIN = 18



def test():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    #This function turns the valve on and off in 10 sec. intervals.
    try:
        for idx in range(5):
            GPIO.output(PIN, 1)
            logging.info("GPIO HIGH (on)")
            time.sleep(3)
            GPIO.output(PIN, 0)
            logging.info("GPIO HIGH (off)")
    except KeyboardInterrupt:
        GPIO.cleanup()
    logging.info("All done!")


if __name__ == "__main__":
    import sys

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s -  %(levelname)s - %(name)s - %(message)s"
    )
    test()
