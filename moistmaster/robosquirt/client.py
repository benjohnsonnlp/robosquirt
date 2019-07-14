import logging
import zmq

logger = logging.getLogger(__name__)


class RobosquirtClient:
    """
    Communicate with a robosquirt process over a ZMQ message bus.
    """

    def __init__(self, port=8001, timeout_ms=3000):
        self.context = zmq.Context()
        self.timeout_ms = timeout_ms
        self.port = port
        self._setup_connection()
        self.socket = None
        self.poller = None

    def _setup_connection(self):
        """
        Open a socket connection to the robosquirt server and setup a poller, which allows us to monitor
        sockers for data, and provides for a timeout.
        """
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://127.0.0.1:{port}'.format(port=self.port))
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        logger.debug("Connecting to Robosquirt server on port {}...".format(self.port))

    def _teardown_connection(self):
        """
        When we experience a connection failure, we want to close the socket and try again later.
        """
        self.socket.close()
        self.socket = None
        self.poller = None

    def _send_and_recieve(self, message_obj):
        if not self.socket:
            self._setup_connection()
        self.socket.send_json(message_obj)
        socks = dict(self.poller.poll(self.timeout_ms))
        if self.socket in socks:
            return self.socket.recv_json()
        else:  # Socket didn't respond after ``self.timeout_ms`` milliseconds.
            logger.warning("Unable to connect to Robosquirt server after {} milliseconds, closing socket.".format(
                self.timeout_ms
            ))
            self._teardown_connection()
            return {}

    def _do_action(self, action, identifier):
        return self._send_and_recieve({"entity": "valve",
                                       "identifier": identifier,
                                       "action": action
                                       })

    def open(self, identifier=0):
        return self._do_action("open", identifier)

    def close(self, identifier=0):
        return self._do_action("close", identifier)

    def toggle(self, identifier=0):
        return self._do_action("toggle", identifier)

    def get_status(self, identifier=0):
        return self._send_and_recieve({"entity": "valve",
                                       "identifier": identifier})
