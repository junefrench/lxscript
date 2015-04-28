from socket import *
import struct


class ArtNetOutput:
    def __init__(self, start_address, universe=0, address='<broadcast>', port=6454):
        self._start_address = start_address

        self._universe = universe

        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._address = (address, port)

        self._sequence = 0

    @staticmethod
    def address_count():
        return 512

    def range(self):
        return range(
            self._start_address,
            self._start_address + self.address_count()
        )

    def output(self, data):
        self._socket.sendto(self._pack(data), self._address)
        self._sequence += 1
        self._sequence %= 1 << 8

    def _pack(self, data):
        """Pack the current output data into an ArtDMX packet"""
        # Oh god Art-Net is horrible and keeps switching endianness
        return b'Art-Net\0' + \
               struct.pack('<H', 0x5000) + \
               struct.pack('>H', 14) + \
               bytes([self._sequence]) + \
               bytes([0]) + \
               struct.pack('<H', self._universe) + \
               struct.pack('>H', 512) + \
               bytes([int(data[i] * 255) for i in self.range()])
