import os
from contextlib import contextmanager
from datetime import datetime
from functools import partial
import logging
import pytz


os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"


try:
    import RPi.GPIO as GPIO
except ImportError:
    import robosquirt.mockGPIO as GPIO


class BasePin:

    gpio_functions = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel

    def _register(self):
        for fn_name in self.gpio_functions:
            fn = getattr(GPIO, fn_name)
            setattr(self, fn_name, partial(fn, self.channel))


class InputPin(BasePin):
    """
    Initialize a GPIO Pin, setting up the channel you are using as an input::

        my_pin = InputPin(18)
        input = my_pin.input()

        my_other_pin = InputPin(19, pull_up_down=GPIO.PUD_UP)
        channel = my_other_pin.wait_for_edge(GPIO.RISING, timeout=500000)


    """
    gpio_functions = ("input", "wait_for_edge", "add_event_detect", "event_detected", "remove_event_detect")

    def __init__(self, channel, pull_up_down=None):
        super().__init__(channel)
        self.channel = channel
        setup_kwargs = {"pull_up_down": pull_up_down} if pull_up_down is not None else {}
        GPIO.setup(self.channel, GPIO.IN, **setup_kwargs)
        self._register()


class OutputPin(BasePin):
    """
    Initialize a GPIO Pin, setting up the channel you are using as an output::

            my_pin = OutputPin(18)
            my_pin.output(1)
            print("This pin is HIGH." if my_pin.current_state == 1 else "This pin is LOW.")

    """
    gpio_functions = ("output", )

    def __init__(self, channel):
        super().__init__(channel)
        GPIO.setup(self.channel, GPIO.OUT)
        self._register()

    @property
    def current_state(self):
        """
        You can read the current state of a channel set up as an output using the input() function.
        """
        return GPIO.input(self.channel)

    def send_high(self):
        self.output(GPIO.HIGH)

    def send_low(self):
        self.output(GPIO.LOW)


@contextmanager
def gpio_session(numbering_system=GPIO.BCM):
    """
    Setup board numbering system, and cleanup everything when done.

    There are two ways of numbering the IO pins on a Raspberry Pi within RPi.GPIO. The first is using the BOARD
    numbering system. This refers to the pin numbers on the P1 header of the Raspberry Pi board. The second numbering
    system is the BCM numbers. This is a lower level way of working - it refers to the channel numbers on the Broadcom
    SOC.

    At the end any program, clean up any resources we might have used. When session exits, return all channels back to
    inputs with no pull up/down, you can avoid accidental damage to your RPi by shorting out the pins. Note that this
    will only clean up GPIO channels that your script has used. Note that GPIO.cleanup()
    also clears the pin numbering system in use.

    :param numbering_system: ``GPIO.BOARD`` or ``GPIO.BCM``
    """

    logging.debug("GPIO Session started.")
    GPIO.setmode(numbering_system)
    yield
    GPIO.cleanup()
    logging.debug("GPIO Session closed.")


def utc_now():
    return pytz.UTC.localize(datetime.utcnow())
