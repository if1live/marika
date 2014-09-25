#-*- coding: utf-8 -*-

import socket
import threading
import SocketServer
import config
import json
import events


class EventSerializer(object):
    def serialize(self, evt):
        data = json.dumps(evt)
        return data

    def deserialize(self, data):
        evt = json.loads(data)
        return evt


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """
    http://stackoverflow.com/questions/14417080/prevent-a-request-getting-closed-in-python-socketserver
    """
    def setup(self):
        print('{}:{} connected'.format(*self.client_address))

    def run_cycle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()

        sensor = events.sensor_storage
        val = {
            'index_pos': sensor.index_finger_pos,
            'thumb_pos': sensor.thumb_finger_pos,
            'angle': sensor.cmd_angle,
        }
        serializer = EventSerializer()
        response = serializer.serialize(val)
        self.request.sendall(response)

    def handle(self):
        try:
            while True:
                self.run_cycle()
        except socket.error as e:
            pass


    def finish(self):
        print('{}:{} disconnected'.format(*self.client_address))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def init_network():
    server = ThreadedTCPServer((config.HOST, config.PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    print('Server Address : %s:%d' %(ip, port))

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    return server

def deinit_network(server):
    server.shutdown()
