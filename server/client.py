#-*- coding: utf-8 -*-

import config
import json
import socket
import network
import time

UPDATE_INTERVAL = 1.0 / 2.0

def run_cycle(sock):
    sock.sendall(unicode(1))
    response = sock.recv(1024)
    serializer = network.EventSerializer()
    data = serializer.deserialize(response)
    print(data)

def client(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

        while True:
            prev_time = time.time()
            run_cycle(sock)
            curr_time = time.time()

            # 60fps속도로 업데이트 하는거로 충분하다
            cycle_time = curr_time - prev_time
            pause_time = UPDATE_INTERVAL - cycle_time
            if pause_time > 0:
                time.sleep(pause_time)


    except socket.error as e:
        print(e)
    finally:
        sock.close()

if __name__ == '__main__':
    client(config.HOST, config.PORT)
