from model.output import Output
from ports.art_net import ArtNetPort
from util.timer import PeriodicTimer


class Instance():
    """The core object of an LXScript engine instance.
    Holds all data and deals with periodically sending output data on ports.
    """

    def __init__(self):
        # Dictionaries of show data
        self.systems = {}
        self.settings = {}

        # Set up output, ports, and start outputting
        self.output = Output()
        self.ports = {ArtNetPort(self.output, 1)}
        self._timer = PeriodicTimer(0.05, self._tick)

    def _tick(self):
        for port in self.ports:
            port.send()

    def run(self):
        self._timer.start()

    def stop(self):
        self._timer.cancel()
