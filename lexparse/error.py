import antlr4.error.ErrorListener


class _ExceptionErrorListener(antlr4.error.ErrorListener.ErrorListener):
    def __init__(self, error_class):
        self.error_class = error_class

    def syntaxError(self, recognizer, offendingSymbol, line, charPositionInLine, msg, e):
        raise self.error_class(e)


class _AntlrError(Exception):
    def __init__(self, antlr_exception):
        self.antlr_exception = antlr_exception


class LexError(_AntlrError):
    """An exception indicating an error occurred in lexing some LXScript"""

    pass


class ParseError(_AntlrError):
    """An exception indicating an error occurred in parsing some LXScript"""

    pass