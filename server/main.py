#-*- coding: utf-8 -*-

import network
import devices
import sys


if __name__ == '__main__':
    server = network.init_network()
    device = devices.LeapMotionDevice()
    #device = devices.FakeDevice()

    print('press enter to quit...')
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        device = None
        network.deinit_network(server)
