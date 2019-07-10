import logging

from .constants import *


logger = logging.getLogger("mositmaster")


def setup(channel, state, **_):
    logger.info("GPIO setup: channel={}, state={}".format(channel, state))


def input(channel):
    logger.info("GPIO input: channel={}".format(channel))


def output(channel, value):
    logger.info("GPIO output: channel={}, value={}".format(channel, value))


def setmode(mode):
    logger.info("GPIO setmode: mode={}".format(mode))


def cleanup():
    logger.info("GPIO cleanup")


def wait_for_edge(channel, edge):
    logger.info("GPIO wait for edge: channel={}, edge={}".format(channel, edge))


def add_event_detect(channel, edge, **_):
    logger.info("GPIO add event detect: channel={}, edge={}".format(channel, edge))


def event_detected(channel):
    logger.info("GPIO event detected: channel={}".format(channel))

def remove_event_detect(channel):
    logger.info("GPIO remove event detect: channel={}".format(channel))