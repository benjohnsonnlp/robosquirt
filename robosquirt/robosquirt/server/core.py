import logging
import pprint
import signal
import threading
import voluptuous
import zmq

from robosquirt.analytics.models import create_tables_if_needed
from robosquirt.solenoid import Valve
from robosquirt.utils import gpio_session


logger = logging.getLogger(__name__)

#: We will listen for these OS signals and shutdown the Robosquirt process gracefully when received.
INTERRUPT_SIGNAL_NAME_MAP = {
    signal.SIGINT: "SIGINT",
    signal.SIGHUP: "SIGHUP",
    signal.SIGTERM: "SIGTERM"

}


class Main:
    """
    The main Robosquirt process: coordinates valve control, watering policy, and the ØMQ-based server.
    """

    def __init__(self, valve_pin):
        self.objects = {
            "valve": Valve(valve_pin)
        }
        for sig_type in INTERRUPT_SIGNAL_NAME_MAP.keys():
            signal.signal(sig_type, self.os_signal_handler)
        self.should_stop = False
        self.server = Server(self.objects["valve"])

    def cleanup(self):
        """
        Signal the ØMQ server thread to stop, make sure the valve is closed.
        """
        self.server.stop()
        self.objects["valve"].close()

    def os_signal_handler(self, signum, frame):
        """
        Handles signals from the OS (specifically sigterm, sigint, and sighup).

        :param signum: The signal that's being handled.
        :param frame: The current stack frame.
        :return:
        """
        signal_name = INTERRUPT_SIGNAL_NAME_MAP.get(signum, "unknown")
        logger.info("{} OS signal received. Shutting down all...".format(signal_name))
        self.should_stop = True
        self.cleanup()

    def run(self):
        try:
            self.server.start()
            while not self.should_stop:
                # FIXME: All the watering policy logic checks would go here.
                pass
        except Exception as exc:
            # Whenever something unexpected happens, cleanup everything and re-raise.
            logger.error("An error occurred: {}".format(exc))
            self.cleanup()
            raise


class Server(threading.Thread):
    """
    A ØMQ-based TCP server, runs in a separate thread and shares a ``solenoid.Valve`` object with the main thread
    which it can manipulate directly (the Valve class is thread-safe).
    """

    #: This will be used to validate messages from clients.
    schema = voluptuous.Schema({
        voluptuous.Required("entity"): "valve",
        voluptuous.Required("identifier"): int,
        voluptuous.Required("action", default=None): voluptuous.Any(None, "open", "close", "toggle")
    })

    def __init__(self, obj, port=8001):
        super().__init__()
        self._stop_event = threading.Event()

        self.port = port
        self.obj = obj
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:{port}".format(port=self.port))

    def handle(self, message):
        try:
            clean_data = self.schema(message)
        except voluptuous.MultipleInvalid as exc:
            return {
                "entity": "valve",
                "identifier": message.get("identifier" or -1),
                "succeeded": False,
                "error": "Invalid message: {}".format(exc)
            }
        if clean_data["identifier"] != 0:
            return {
                "entity": "valve",
                "identifier": message.get("identifier" or -1),
                "succeeded": False,
                "error": "There is no valve with the identifier {}".format(clean_data["identifier"])
            }
        if clean_data["action"] is None:  # Status is being requested.
            del clean_data["action"]
            clean_data.update({
                "state": self.obj.status,
            })
        else:
            succeeded, err = self.obj.handle_message(clean_data)
            clean_data.update({
                "succeeded": succeeded,
                "error": err
            })
        return clean_data

    def run(self):
        logger.info("Robosquirt server started and listening on port {}...".format(self.port))
        while not self._stop_event.is_set():
            try:
                message = self.socket.recv_json(zmq.NOBLOCK)
            except zmq.ZMQError:  # No messages received.
                pass
            else:
                logger.debug("Received request: %s" % pprint.pformat(message))
                response = self.handle(message)
                #  Send reply back to client
                self.socket.send_json(response)

    def stop(self):
        """
        Calling this sets the stop event flag, which will tell the thread to exit.
        """
        logger.info("Stopping robosquirt server...")
        self._stop_event.set()


def main():
    create_tables_if_needed()
    with gpio_session():
        main_proc = Main(18)
        main_proc.run()
