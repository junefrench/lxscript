from cmd import Cmd
from .engine import Engine


class Console(Cmd):
    """A console repl for the lxscript language.
    Processes commands and applies them to an lxscript engine.
    """

    def __init__(self, engine=Engine()):
        super(Console, self).__init__()
        self.engine = engine

    def default(self, line):
        print("Nothing doing")