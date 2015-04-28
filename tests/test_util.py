from unittest import TestCase

from util.timer import *


class TimerTest(TestCase):
    def test_periodic_timer(self):
        import time

        self._counter = 0

        def increment(by, negative=False):
            self._counter += (-by if negative else by)

        t = PeriodicTimer(0.05, increment, [1], {'negative': True})
        t.start()

        time.sleep(0.225)
        t.cancel()
        self.assertEqual(self._counter, -4)
        time.sleep(0.1)
        self.assertEqual(self._counter, -4)
