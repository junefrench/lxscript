from ._gen import LXScriptParser
from . import error
from antlr4 import CommonTokenStream


class Parser(LXScriptParser.LXScriptParser):
    """A parser for the LXScript language"""

    def __init__(self, input):
        super(Parser, self).__init__(input=CommonTokenStream(input))
        # Should call self.removeAllErrorListeners() but that's not available in current ANTLR python runtime
        self._listeners = [error._ExceptionErrorListener(error.ParseError)]
