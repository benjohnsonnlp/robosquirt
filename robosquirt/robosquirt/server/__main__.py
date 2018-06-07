import logging

from robosquirt.config import config
from robosquirt.server.core import main

if __name__ == "__main__":
    import sys
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if config["log_debug"] else logging.INFO,
        format="%(asctime)s -  %(levelname)s - %(name)s - %(message)s"
    )
    main()

