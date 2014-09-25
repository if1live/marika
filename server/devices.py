#-*- coding: utf-8 -*-

# set library path
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import events
import Tkinter
from Tkinter import Tk, Frame, BOTH, IntVar, DoubleVar, Button
from ttk import Label, Scale, Style, Label
import math

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


class FakeDeviceApp(Frame):
    MIN_X = 0
    MAX_X = 50
    MIN_Y = 0
    MAX_Y = 100
    MIN_Z = 0
    MAX_Z = 200

    def __init__(self, parent):
        Frame.__init__(self, parent, background='white')
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.parent.title('Fake Device')
        self.style = Style()
        self.style.theme_use('default')

        self.pack(fill=BOTH, expand=1)

        x_scale = Scale(self, from_=self.MIN_X, to=self.MAX_X, command=self.on_scale_x)
        x_scale.place(x=0, y=0)

        y_scale = Scale(self, from_=self.MIN_Y, to=self.MAX_Y, command=self.on_scale_y)
        y_scale.place(x=0, y=20)

        z_scale = Scale(self, from_=self.MIN_Z, to=self.MAX_Z, command=self.on_scale_z)
        z_scale.place(x=0, y=40)

        angle_scale = Scale(self, from_=0, to=math.pi/2, command=self.on_scale_angle)
        angle_scale.place(x=0, y=80)

        self.x_var = IntVar()
        self.x_label = Label(self, text=0, textvariable=self.x_var)
        self.x_label.place(x=100, y=0)

        self.y_var = IntVar()
        self.y_label = Label(self, text=0, textvariable=self.y_var)
        self.y_label.place(x=100, y=20)

        self.z_var = IntVar()
        self.z_label = Label(self, text=0, textvariable=self.z_var)
        self.z_label.place(x=100, y=40)

        self.angle_var = DoubleVar()
        self.angle_label = Label(self, text=0, textvariable=self.angle_var)
        self.angle_label.place(x=100, y=80)

        self.button = Button(self, text='test', command=self.on_button)
        self.button.place(x=0, y=100)

    def on_button(self):
        print('hello')

    def on_scale_angle(self, val):
        v = float(val)
        self.angle_var.set(v)
        self.update()


    def on_scale_x(self, val):
        v = int(float(val))
        self.x_var.set(v)
        self.update()

    def on_scale_y(self, val):
        v = int(float(val))
        self.y_var.set(v)
        self.update()

    def on_scale_z(self, val):
        v = int(float(val))
        self.z_var.set(v)
        self.update()

    def update(self):
        x = self.x_var.get()
        y = self.y_var.get()
        z = self.z_var.get()
        angle = self.angle_var.get()

        sensor = events.sensor_storage
        sensor.reset()
        if not (x == 0 and y == 0 and z == 0):
            index_pos = [x, y, z]
            sensor.index_finger_pos = index_pos
            sensor.cmd_angle = angle



class FakeDevice(object):
    def __init__(self):
        root = Tk()
        root.geometry('250x150+300+300')
        app = FakeDeviceApp(root)
        root.mainloop()

    def __del__(self):
        pass
