#! /usr/bin/env python

# python programa to comunicate with an MCP3008

# Import our SpiDe wrapper and our sleep function

import spidev

from time import sleep

# Establish SPI device on Bus 0,Device 0

spi = spidev.SpiDev()

spi.open(0, 0)


def getAdc(channel):
    # check valid channel

    if ((channel > 7) or (channel < 0)):
        print('oops')
        return -1

    # Preform SPI transaction and store returned bits in 'r'

    r = spi.xfer2([1, (8 + channel) << 4, 0])
    print('r: ' + str(r))

    # Filter data bits from retruned bits

    adcOut = ((r[1] & 3) << 8) + r[2]

    percent = int(round(100 * (adcOut - 392) * 1.0 / (792 - 392)))

    # percent = int(round(adcOut/10.24))

    # print out 0-1023 value and percentage

    print("ADC Output: {0:4d} Percentage: {1:3}%".format(adcOut, percent))

    sleep(0.1)


while True:
    getAdc(0)
