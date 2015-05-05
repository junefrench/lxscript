#!/usr/bin/env python3
import argparse

from core.console import Console
from core.engine import Engine
from ports.art_net import ArtNetPort


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Theatrical lighting control engine/language interpreter.")
    ap.add_argument('--address', help='IP address to send ArtNet data to', default='<broadcast>')
    args = ap.parse_args()

    engine = Engine([ArtNetPort(1, address=args.address)])
    Console(engine).cmdloop()
