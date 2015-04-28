from socket import *
import struct

from util.timer import PeriodicTimer


class ArtNetOutput:
    def __init__(self, universe=0, period=0.05, address='<broadcast>', port=6454):
        self._universe = universe

        self._timer = PeriodicTimer(period, self._output)

        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._address = (address, port)

        self._sequence = 0

    def output(self):
        self._sequence += 1
        self._sequence %= 1 << 8
        self._socket.sendto(self._pack(), self._address)

    def enable(self):
        self._timer.start()

    def disable(self):
        self._timer.cancel()

    def _pack(self):
        """Pack the current output data into an ArtDMX packet"""
        # Oh god Art-Net is horrible and keeps switching endianness
        return b'Art-Net\0' + \
               struct.pack('<H', 0x5000) + \
               struct.pack('>H', 14) + \
               bytes([self._sequence]) + \
               bytes([0]) + \
               struct.pack('<H', self._universe) + \
               struct.pack('>H', 512) + \
               bytes([level for level in self._data])
