import cmd
import traceback

import lexparse.error
from core import interpreter
from . import engine


class Console(cmd.Cmd):
    """A console repl for the lxscript language.
    Processes commands and applies them to an lxscript engine.
    """

    def __init__(self, engine=engine.Engine()):
        super(Console, self).__init__()
        self.engine = engine
        self.engine.run()
        self.prompt = '(lxscript) > '

    def default(self, line):
        try:
            interpreter.Interpreter(self.engine).run(line)
        except (lexparse.error.LexError, lexparse.error.ParseError):
            print("Syntax Error")
        except NotImplementedError:
            print("Not Implemented (yet)")
        except Exception as e:
            print("Error: " + str(e))
            print(traceback.format_exc())
