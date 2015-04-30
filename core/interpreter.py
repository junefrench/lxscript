from core import engine
from lexparse import lexer, parser
from model import system


class Interpreter():
    def __init__(self, engine=engine.Engine()):
        self._engine = engine

    def run(self, code):
        parse_tree = parser.Parser(lexer.Lexer(code)).lxscript()
        _Visitor(self._engine).visit(parse_tree)


class _Visitor(parser.Visitor):
    def __init__(self, engine: engine.Engine):
        self.engine = engine

    def visit_declaration_system(self, ctx):
        name = ctx.identifier().getText()
        system = self.visit(ctx.system())
        self.engine.systems[name] = system

    def visit_system_literal(self, ctx):
        address = ctx.NUMBER().getText()
        return system.OutputSystem(address, self.engine.output)

    def visit_system_reference(self, ctx):
        name = ctx.identifier().getText()
        return self.engine.systems[name]