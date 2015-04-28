import unittest

from output.artnet import *


class ArtNetTest(unittest.TestCase):
    def test_pack(self):
        output = ArtNetOutput(1, universe=42)
        data = [None] + ([0] * 512)
        data[1] = 0.25
        data[8] = 0.5
        data[512] = 1.0
        buffer = output._pack(data)
        expected = (
            b'Art-Net\0\x00\x50\x00\x0e\x00\x00\x2a\x00\x02\x00'
            b'\x3f' + bytes(6) + b'\x7f' + bytes(503) + b'\xff'
        )
        print(buffer)
        print(expected)

        self.assertEqual(buffer, expected)

