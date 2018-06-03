import logging
from robosquirt.server.core import serve_forever

if __name__ == "__main__":
    import sys
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s -  %(levelname)s - %(name)s - %(message)s"
    )
    logging.getLogger('pizco.pizco').setLevel(logging.INFO)
    serve_forever()

