from model import output
from ports import art_net
from util import timer


class Engine():
    """The core object of an LXScript engine instance.
    Holds all data and deals with periodically sending output data on ports.
    """

    def __init__(self, ports=[art_net.ArtNetPort(1)]):
        # Dictionaries of show data
        self.systems = {}
        self.settings = {}
        self.sequences = {}
        self._playback = None

        # Set up output, ports, and start outputting
        self.output = output.Output()
        self.ports = set(ports)
        self._timer = timer.PeriodicTimer(0.05, self._tick)

    def _tick(self):
        for port in self.ports:
            port.send(self.output)

    def run(self):
        self._timer.start()

    def stop(self):
        self._timer.cancel()

    def load(self, sequence):
        self._playback = iter(sequence)

    def go(self):
        next(self._playback).apply()
