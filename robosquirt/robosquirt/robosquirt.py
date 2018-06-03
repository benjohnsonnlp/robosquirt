import logging
from .solenoid import Valve
from .utils import gpio_session


if __name__ == "__main__":
    import sys
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s -  %(levelname)s - %(name)s - %(message)s"
    )
    channel = 18
    with gpio_session():
        my_valve = Valve(18)
        my_valve.open()
        my_valve.close()
        my_valve.test()
        print(my_valve.status)
        print(my_valve.real_status)
