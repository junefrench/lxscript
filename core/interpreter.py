from core import engine
from lexparse import lexer, parser
from model import system, setting


class Interpreter():
    def __init__(self, engine=engine.Engine()):
        self._engine = engine

    def run(self, code):
        parse_tree = parser.Parser(lexer.Lexer(code)).lxscript()
        _Visitor(self._engine).visit(parse_tree)


class _Visitor(parser.Visitor):
    def __init__(self, engine: engine.Engine):
        self.engine = engine

    def visit_lxscript(self, node):
        for c in node.children:
            self.visit(c)

    def visit_action_setting(self, node):
        setting = self.visit(node.setting())
        setting.apply()

    def visit_declaration_system(self, node):
        name = self.visit(node.identifier())
        system = self.visit(node.system())
        self.engine.systems[name] = system

    def visit_declaration_setting(self, node):
        name = self.visit(node.identifier())
        setting = self.visit(node.setting())
        self.engine.settings[name] = setting

    def visit_declaration_sequence(self, node):
        raise NotImplementedError

    def visit_identifier(self, node):
        name = self.visit(node.NAME()) if node.NAME() else None
        number = self.visit(node.NUMBER()) if node.NUMBER() else None
        return name, number

    def visit_level(self, node):
        if node.FULL():
            return 1
        elif node.OUT():
            return 0
        else:
            number = int(self.visit(node.NUMBER()))
            if number not in range(101):
                raise ValueError('level must be in range(100)')
            return number / 100

    def visit_system_reference(self, node):
        name = self.visit(node.identifier())
        return self.engine.systems[name]

    def visit_system_literal(self, node):
        address = int(self.visit(node.NUMBER()))
        return system.OutputSystem(address, self.engine.output)

    def visit_system_compound(self, node):
        subsystems = [self.visit(s) for s in node.system()]
        return system.CompoundSystem(subsystems)

    def visit_setting_reference(self, node):
        name = self.visit(node.identifier())
        return self.engine.settings[name]

    def visit_setting_partial_reference(self, node):
        raise NotImplementedError

    def visit_setting_literal(self, node):
        system = self.visit(node.system())
        level = self.visit(node.level())
        return setting.LevelSetting(system, level)

    def visit_setting_compound(self, node):
        subsettings = [self.visit(s) for s in node.setting()]
        return setting.CompoundSetting(subsettings)

    def visit_sequence_reference(self, node):
        raise NotImplementedError

    def visit_sequence_literal(self, node):
        raise NotImplementedError

    def visit_terminal(self, node):
        return node.getText()