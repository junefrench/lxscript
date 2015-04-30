import re

from ._gen import LXScriptParser, LXScriptVisitor
from . import error
from antlr4 import CommonTokenStream


class Parser(LXScriptParser.LXScriptParser):
    """A parser for the LXScript language"""

    def __init__(self, input):
        super(Parser, self).__init__(input=CommonTokenStream(input))
        # Should call self.removeAllErrorListeners() but that's not available in current ANTLR python runtime
        self._listeners = [error._ExceptionErrorListener(error.ParseError)]


_VISIT_REGEX = re.compile(r'^visit([A-Z])(.*)$')


class Visitor(LXScriptVisitor.LXScriptVisitor):
    """A visitor for LXScript parse trees"""

    def __getattribute__(self, name):
        # Patch the visitor so that visit_foo works as an alias for visitFoo
        match = _VISIT_REGEX.match(name)
        if match is not None:
            new_name = 'visit_{0}{1}'.format(match.group(1).lower(), match.group(2))
            if hasattr(self, new_name):
                return getattr(self, new_name)
        return object.__getattribute__(self, name)
