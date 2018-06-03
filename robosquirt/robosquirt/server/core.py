from pizco import Server

from robosquirt.solenoid import Valve
from robosquirt.utils import gpio_session


def serve_forever(port=8001):
    with gpio_session():
        zmq_server = Server(Valve(18), 'tcp://127.0.0.1:{port}'.format(port=port))
        zmq_server.serve_forever()
