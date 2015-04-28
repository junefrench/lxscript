from threading import Timer


class PeriodicTimer():
    def __init__(self, interval, function, args=[], kwargs={}):
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self._timer = None

    def _handler(self):
        self.start()
        self._function(*self._args, **self._kwargs)

    def start(self):
        self._timer = Timer(self._interval, self._handler)
        self._timer.start()

    def cancel(self):
        self._timer.cancel()