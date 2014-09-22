#-*- coding: utf-8 -*-

import config
import json
import socket

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        data = json.loads(response)
        print(data)
    finally:
        sock.close()

if __name__ == '__main__':
    client(config.HOST, config.PORT, "Hello World 1")
