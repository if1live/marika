#-*- coding: utf-8 -*-

import network
import devices
import sys

if __name__ == '__main__':
    server = network.init_network()

    device_type = 'default'
    if len(sys.argv) == 2:
        device_type = sys.argv[1]
    device = devices.create_device(device_type)

    print('press enter to quit...')
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        device = None
        network.deinit_network(server)
