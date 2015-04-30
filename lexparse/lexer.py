from ._gen import LXScriptLexer
from . import error
from antlr4.InputStream import InputStream


class Lexer(LXScriptLexer.LXScriptLexer):
    """A lexer for the LXScript language"""

    def __init__(self, input=None):
        super(Lexer, self).__init__(input=InputStream(input))
        # Should call self.removeAllErrorListeners() but that's not available in current ANTLR python runtime
        self._listeners = [error._ExceptionErrorListener(error.LexError)]
