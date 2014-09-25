#-*- coding: utf-8 -*-

import sys
if sys.version_info >= (3,):
    import queue
else:
    import Queue as queue


EVT_CLICK = 1


class ClickEvent(object):
    Type = EVT_CLICK

    def __init__(self, frame_id, timestamp):
        self.frame_id = frame_id
        self.timestamp = timestamp

class EventQueue(object):
    def __init__(self, maxsize=0):
        self.q = queue.Queue(maxsize)

    def put(self, item):
        self.q.put(item)

    def get(self):
        return self.q.get()

    def empty(self):
        return self.q.empty()

    def get_all(self):
        if self.empty():
            return []

        evt_list = []
        while not self.q.empty():
            evt = self.q.get()
            evt_list.append(evt)
        return evt_list


class SensorStorage(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.index_finger_pos = None
        self.index_finger_dir = None
        self.thumb_finger_pos = None
        self.thumb_finger_dir = None
        self.cmd_angle = None




normal_evt_queue = EventQueue()
sensor_storage = SensorStorage()
