import logging
import pprint
import voluptuous
import zmq

from robosquirt.solenoid import Valve
from robosquirt.utils import gpio_session


logger = logging.getLogger(__name__)


class Server:

    schema = voluptuous.Schema({
        voluptuous.Required("entity"): "valve",
        voluptuous.Required("identifier"): int,
        voluptuous.Required("action", default=None): voluptuous.Any(None, "open", "close", "toggle")
    })

    def __init__(self, obj, port=8001):
        self.obj = obj
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:{port}".format(port=port))
        self.should_stop = False
        logger.info("Robosquirt server started and listening on port {}...".format(port))

    def serve_forever(self):
        while not self.should_stop:
            #  Block while waiting for next request from client
            message = self.socket.recv_json()
            logger.debug("Received request: %s" % pprint.pformat(message))
            response = self.handle(message)
            #  Send reply back to client
            self.socket.send_json(response)

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


def serve_forever(port=8001):
    with gpio_session():
        zmq_server = Server(Valve(18), port=port)
        zmq_server.serve_forever()
