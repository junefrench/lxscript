from .LXScriptLexer import LXScriptLexer as _LXScriptLexer
from .LXScriptParser import LXScriptParser as _LXScriptParser
from antlr4.error.ErrorListener import ErrorListener as _ErrorListener


class _ExceptionErrorListener(_ErrorListener):
    def __init__(self, error_class):
        self.error_class = error_class

    def syntaxError(self, recognizer, offendingSymbol, line, charPositionInLine, msg, e):
        raise self.error_class(e)


class _LexParseError(Exception):
    def __init__(self, antlr_exception):
        self.antlr_exception = antlr_exception


class LexError(_LexParseError):
    pass


class ParseError(_LexParseError):
    pass


class LXScriptLexer(_LXScriptLexer):
    def __init__(self, input=None):
        super(LXScriptLexer, self).__init__(input=input)
        # Should call self.removeAllErrorListeners() but that's not available in current ANTLR python runtime
        self._listeners = [_ExceptionErrorListener(LexError)]


class LXScriptParser(_LXScriptParser):
    def __init__(self, input=None):
        super(LXScriptParser, self).__init__(input=input)
        # Should call self.removeAllErrorListeners() but that's not available in current ANTLR python runtime
        self._listeners = [_ExceptionErrorListener(ParseError)]

