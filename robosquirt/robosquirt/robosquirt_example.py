import logging
from robosquirt.solenoid import Valve
from robosquirt.utils import gpio_session


if __name__ == "__main__":
    import sys
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s -  %(levelname)s - %(name)s - %(message)s"
    )
    channel = 18
    with gpio_session():
        my_valve = Valve(18)
        my_valve.open()
        my_valve.close()
        print("Get ready...")
        import time
        time.sleep(4)

        my_valve.test(seconds_on=10)
        print(my_valve.status)
        print(my_valve.real_status)
