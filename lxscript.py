#!/usr/bin/env python3
import argparse

from core.console import Console
from core.engine import Engine
from core.interpreter import Interpreter
from ports.art_net import ArtNetPort


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Theatrical lighting control engine/language interpreter.")
    ap.add_argument('file', nargs='?',
                    help='A file of lxscript code to run before entering the interactive environment')
    ap.add_argument('--address', help='IP address to send ArtNet data to', default='<broadcast>')
    args = ap.parse_args()

    engine = Engine([ArtNetPort(1, address=args.address)])

    if args.file:
        with open(args.file, 'r') as file:
            Interpreter(engine).run(file.read())

    Console(engine).cmdloop()
