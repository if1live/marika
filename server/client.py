#-*- coding: utf-8 -*-

import config
import json
import socket
import network

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        serializer = network.EventSerializer()
        data = serializer.deserialize(response)
        print(data)
    finally:
        sock.close()

if __name__ == '__main__':
    client(config.HOST, config.PORT, "request")
