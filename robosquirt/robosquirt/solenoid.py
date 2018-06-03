import logging
import time

from .utils import OutputPin


ON = 1
OFF = 0


class Valve:
    """
    A class for controlling a solenoid valve.
    """

    # We track the state of the valve here.
    is_open = False

    def __init__(self, pin):
        """
        :param pin: The Raspberry PI pin number the valve is on
        """
        self.pin = OutputPin(pin)

    @property
    def status(self):
        return "open" if self.is_open else "closed"

    @property
    def real_status(self):
        """
        Actually poll the GPIO input for the state.
        """
        return "open" if self.pin.current_state == ON else "closed"

    def open(self):
        """
        Open the valve.
        """
        if self.pin.current_state == ON:  # pragma: no cover
            logging.error(("Requested the valve channel {} open, "
                           "component indicates valve is already open.").format(self.pin.channel))
            return
        if self.is_open:  # pragma: no cover
            # Trying to open a valve that is already open may indicate a bug:
            logging.warning("Valve is already open.")
            return
        self.pin.send_high()
        self.is_open = True
        logging.debug("Valve opened.")

    def close(self):
        """
        Close the valve.
        """
        if self.pin.current_state == OFF:  # pragma: no cover
            logging.error(("Requested valve on channel {}, close"
                           "component indicates valve is already closed.").format(self.pin.channel))
            return
        if not self.is_open:  # pragma: no cover
            # Trying to close a valve that is already open may indicate a bug:
            logging.warning("Valve is already closed.")
            return
        self.pin.send_low()
        self.is_open = False
        logging.debug("Valve closed.")

    def toggle(self):
        """
        Open the valve if closed, close the valve if open
        """
        if self.is_open:
            self.close()
        else:
            self.open()

    def test(self, seconds_on=3):
        """
        Open the valve for ``seconds_on`` seconds, then close it again.

        :param seconds_on: Number of seconds valve should remain open for test.
        """
        self.open()
        time.sleep(seconds_on)
        self.close()
