#-*- coding: utf-8 -*-

# set library path
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import events

def vector_to_tuple(v):
    return (v.x, v.y, v.z)


class MyListener(Leap.Listener):
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

        # 기존에 저장된 값이 있으면 날린다.
        # 이것이 남아있으면 손을 제거한 다음에도 손이 있는것처럼 처리되니까
        events.sensor_storage.reset()

        fid = frame.id
        timestamp = frame.timestamp

        if not frame.hands:
            return

        for hand in frame.hands:
            # 개발은 오른손잡이 기준으로만 진행한다.
            if hand.is_left:
                continue

            index_finger = [x for x in hand.fingers if x.type() == 1][0]
            thumb_finger = [x for x in hand.fingers if x.type() == 0][0]

            index_pos = vector_to_tuple(index_finger.stabilized_tip_position)
            thumb_pos = vector_to_tuple(thumb_finger.stabilized_tip_position)

            index_dir = index_finger.direction
            thumb_dir = thumb_finger.direction
            angle_rad = index_dir.angle_to(thumb_dir)

            storage = events.sensor_storage
            storage.index_finger_pos = index_pos
            storage.index_finger_dir = vector_to_tuple(index_dir)
            storage.thumb_finger_pos = thumb_pos
            storage.thumb_finger_dir = vector_to_tuple(thumb_dir)
            storage.cmd_angle = angle_rad

            # TODO 일반 이벤트 처리
            print(angle_rad)


class LeapMotionDevice(object):
    def __init__(self):
        self.listener = MyListener()
        self.controller = Leap.Controller()

        # for leap motion
        self.controller.add_listener(self.listener)

    def __del__(self):
        self.controller.remove_listener(self.listener)


class FakeDevice(object):
    pass
