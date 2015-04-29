from ._gen import LXScriptParser
from . import error


class Parser(LXScriptParser.LXScriptParser):
    """A parser for the LXScript language"""

    def __init__(self, input=None):
        super(Parser, self).__init__(input=input)
        # Should call self.removeAllErrorListeners() but that's not available in current ANTLR python runtime
        self._listeners = [error._ExceptionErrorListener(error.ParseError)]