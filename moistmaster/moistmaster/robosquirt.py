import asyncio
import logging
from pizco import Proxy


logger = logging.getLogger(__name__)


class RoboSquirtProxy:

    """
    Communicate with a robosquirt process over a ZMQ message bus.
    """
    def __init__(self, port=8001):
        logger.info("Starting proxy to robosquirt server...")
        # We need to create an event loop in the current thread before initializing the proxy.
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.proxy = Proxy('tcp://127.0.0.1:{port}'.format(port=port))

    def __getattr__(self, name):
        return getattr(self.proxy, name)

    @property
    def status(self):
        return self.proxy.get_status()
