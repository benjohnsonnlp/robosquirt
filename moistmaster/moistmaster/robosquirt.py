import logging
import zmq

logger = logging.getLogger(__name__)


class RobosquirtClient:
    """
    Communicate with a robosquirt process over a ZMQ message bus.
    """

    def __init__(self, port=8001, timeout_ms=5000):
        self.context = zmq.Context()
        self.context.setsockopt(zmq.LINGER, 0)
        self.context.setsockopt(zmq.RCVTIMEO, timeout_ms)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://127.0.0.1:{port}'.format(port=port))
        logger.info("Connected to Robosquirt server on port {}...".format(port))

    def _send_and_recieve(self, message_obj):
        try:
            self.socket.send_json(message_obj)
            return self.socket.recv_json()
        except zmq.error.Again:
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
