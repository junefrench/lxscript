from unittest import TestCase
from unittest.mock import Mock

from ports.artnet import *


class ArtNetTest(TestCase):
    def test_pack(self):
        data = [0] * 512
        data[0] = 0.25
        data[7] = 0.5
        data[511] = 1.0

        def get_level(address):
            return data[address - 1]

        output = Mock()
        output.get_level = get_level
        port = ArtNetPort(output, 1, universe=42)

        buffer = port._pack()
        expected = (
            b'Art-Net\0\x00\x50\x00\x0e\x00\x00\x2a\x00\x02\x00'
            b'\x3f' + bytes(6) + b'\x7f' + bytes(503) + b'\xff'
        )
        print(buffer)
        print(expected)

        self.assertEqual(buffer, expected)

