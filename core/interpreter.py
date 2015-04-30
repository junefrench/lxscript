from core.engine import Engine
from lexparse.lexer import Lexer
from lexparse.parser import Parser


class Interpreter():
    def __init__(self, engine=Engine()):
        self._engine = engine

    def run(self, code):
        parse_tree = Parser(Lexer(code)).lxscript()