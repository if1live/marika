#-*- coding: utf-8 -*-

import unittest
import events

class EveneQueueTest(unittest.TestCase):
    def test_put_get(self):
        evt_a = events.ClickEvent(0, 1)
        evt_b = events.ClickEvent(1, 2)

        q = events.EventQueue()
        q.put(evt_a)
        q.put(evt_b)

        self.assertEqual(evt_a, q.get())
        self.assertEqual(evt_b, q.get())

    def test_get_all(self):
        evt_a = events.ClickEvent(0, 1)
        evt_b = events.ClickEvent(1, 2)

        q = events.EventQueue()
        q.put(evt_a)
        q.put(evt_b)

        evt_list = q.get_all()
        self.assertEqual([evt_a, evt_b], evt_list)
        self.assertEqual(q.empty(), True)
