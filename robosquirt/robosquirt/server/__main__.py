import logging
from configparser import NoSectionError

from robosquirt.config import config
from robosquirt.server.core import main

if __name__ == "__main__":
    import sys
    try:
        log_level = logging.DEBUG if config.getboolean('log', "log_debug") else logging.INFO
    except NoSectionError:
        log_level = logging.INFO
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format="%(asctime)s -  %(levelname)s - %(name)s - %(message)s"
    )
    main()

