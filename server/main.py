#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

# set library path
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import socket
import threading
import SocketServer
import json

import config
import decorators

def vector_to_tuple(v):
    return (v.x, v.y, v.z)


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        sensor_data = SensorStorage.Instance().to_data()
        txt = json.dumps(sensor_data)
        #response = "{}: {}".format(cur_thread.name, data)
        response = txt
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


@decorators.Singleton
class SensorStorage(object):
    def __init__(self):
        self.index_finger_pos = None
        self.index_finger_dir = None
        self.thumb_finger_pos = None
        self.thumb_finger_dir = None
        self.cmd_angle = None

    def to_data(self):
        data = {
            'index_pos': self.index_finger_pos,
            'thumb_pos': self.thumb_finger_pos,
            'angle': self.cmd_angle
        }
        return data



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print('Initialized')

    def on_connect(self, controller):
        print('Connected')

        #제스쳐를 전부 비활성화. 이것의 인식률이 낮아서 raw input을 가공해서 사용한다
        #controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        #controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print('Disconnected')


    def on_frame(self, controller):
        frame = controller.frame()

        fid = frame.id
        timestamp = frame.timestamp

        if not frame.hands:
            return

        for hand in frame.hands:
            hand_type = 'Left hand' if hand.is_left else 'Right hand'

            #print("  %s, id %d, position: %s" % (hand_type, hand.id, hand.palm_position))

            index_finger = [x for x in hand.fingers if x.type() == 1][0]
            thumb_finger = [x for x in hand.fingers if x.type() == 0][0]

            index_pos = index_finger.stabilized_tip_position
            index_dir = index_finger.direction
            thumb_pos = thumb_finger.stabilized_tip_position
            thumb_dir = thumb_finger.direction

            angle_rag = index_dir.angle_to(thumb_dir)

            storage = SensorStorage.Instance()
            storage.index_finger_pos = vector_to_tuple(index_pos)
            storage.index_finger_dir = vector_to_tuple(index_dir)
            storage.thumb_finger_pos = vector_to_tuple(thumb_pos)
            storage.thumb_finger_dir = vector_to_tuple(thumb_dir)
            storage.cmd_angle = angle_rag

            print("update %d" % fid)


listener = SampleListener()
controller = Leap.Controller()

def main():
    print('press enter to quit...')
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
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

        # for leap motion
        controller.add_listener(listener)
        main()

    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

        try:
            server.shutdown()
        except KeyboardInterrupt:
            pass
