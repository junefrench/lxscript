from cmd import Cmd
from core.interpreter import Interpreter
from .engine import Engine
from lexparse.lexer import Lexer
from lexparse.parser import Parser


class Console(Cmd):
    """A console repl for the lxscript language.
    Processes commands and applies them to an lxscript engine.
    """

    def __init__(self, engine=Engine()):
        super(Console, self).__init__()
        self.engine = engine
        self.prompt = '(lxscript) > '

    def default(self, line):
        Interpreter(self.engine).run(line)
