import logging
import time
import threading

from analytics.session import WateringSessionManager

from .utils import OutputPin


ON = 1
OFF = 0


logger = logging.getLogger("robosquirt")


class Valve:
    """
    A class for controlling a solenoid valve.
    """

    # We track the state of the valve here.
    is_open = False
    # robosquirt.analytics.session.WateringSession objects will be placed here when valve is open.
    watering_session = None

    def __init__(self, pin, identifier=0):
        """
        :param pin: The Raspberry PI pin number the valve is on
        :param identifier: The unique identifier of the valve, not used for anything yet.
        """
        self.pin = OutputPin(pin)
        self.identifier = identifier
        # Prevent resource contention across threads, acquired when opening, closing or querying the valve.
        self.lock = threading.RLock()

    @property
    def status(self):
        return "open" if self.is_open else "closed"

    @property
    def real_status(self):
        """
        Actually poll the GPIO input for the state.
        """
        with self.lock:
            return "open" if self.pin.current_state == ON else "closed"

    def open(self):
        """
        Open the valve.
        """
        if self.is_open:  # pragma: no cover
            # Trying to open a valve that is already open may indicate a bug:
            logger.warning("Valve is already open.")
            return
        with self.lock:
            if self.pin.current_state == ON:  # pragma: no cover
                logging.error(("Requested the valve channel {} open, "
                               "component indicates valve is already open.").format(self.pin.channel))
                return
            self.watering_session = WateringSessionManager(self.identifier)
            self.pin.send_high()
            self.watering_session.start()
            self.is_open = True
            logger.info("Valve opened.")

    def close(self):
        """
        Close the valve.
        """
        if not self.is_open:  # pragma: no cover
            # Trying to close a valve that is already open may indicate a bug:
            logger.warning("Valve is already closed.")
            return
        with self.lock:
            if self.pin.current_state == OFF:  # pragma: no cover
                logging.error(("Requested valve on channel {} close, "
                               "component indicates valve is already closed.").format(self.pin.channel))
                return
            self.pin.send_low()
            self.watering_session.end()
            del self.watering_session
            self.is_open = False
            logger.info("Valve closed.")

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

    def handle_message(self, message):
        """
        Handle a message from a client of the Robosquirt server requesting some action be taken.

        :param message: A message from a client of the Robosquirt server. This will have already been validated.
        :return: A tuple of ``(<bool: did action succeed?>, and <None> or <Str: error if it failed>)``
        """
        if message["identifier"] != self.identifier:
            return False, "This message is for the wrong valve."
        action = message["action"]
        if action == "close":
            self.close()
        if action == "open":
            self.open()
        if action == "toggle":
            self.toggle()
        return True, None
