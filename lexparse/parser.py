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


class Visitor(LXScriptVisitor.LXScriptVisitor):
    """A visitor for LXScript parse trees"""
    _visit_regex = re.compile(r'^visit_([a-z])(.*)$')

    def __getattr__(self, name):
        # Patch the visitor so that visit_foo works as an alias for visitFoo
        match = self._visit_regex.match(name)
        new_name = 'visit{0}{1}'.format(match.group(1).upper(), match.group(2))
        return getattr(self, new_name)
