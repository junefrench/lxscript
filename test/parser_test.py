import unittest

from lexparse import LXScriptParser


def _rule(name, symbolic=False):
    return (LXScriptParser.symbolicNames if symbolic else LXScriptParser.ruleNames).index(name) + 1


def _name(rule, symbolic=False):
    if symbolic and (rule == -1):
        return 'EOF'
    else:
        return (LXScriptParser.symbolicNames if symbolic else LXScriptParser.ruleNames)[rule]


class LexerTest(unittest.TestCase):
    def test_system_literal_declaration(self):
        self._parse_expect(
            "1 = @@1",
            ('lxscript', [
                ('declaration', [
                    ('identifier', ['NUMBER']),
                    'EQUALS',
                    ('system', ['AT', 'AT', 'NUMBER']),
                ]),
                'EOF'
            ])
        )

    def test_setting_literal_declaration(self):
        self._parse_expect(
            "!1 = 1 @ full",
            ('lxscript', [
                ('declaration', [
                    'BANG',
                    ('identifier', ['NUMBER']),
                    'EQUALS',
                    ('setting', [
                        ('system', [
                            ('identifier', ['NUMBER']),
                        ]),
                        'AT',
                        ('level', ['FULL'])
                    ]),
                ]),
                'EOF'
            ])
        )

    def test_sequence_literal_declaration(self):
        self._parse_expect(
            "$1 = [!1 !2]",
            ('lxscript', [
                ('declaration', [
                    'DOLLARS',
                    ('identifier', ['NUMBER']),
                    'EQUALS',
                    ('sequence', [
                        'LBRACKET',
                        ('setting', ['BANG', ('identifier', ['NUMBER'])]),
                        ('setting', ['BANG', ('identifier', ['NUMBER'])]),
                        'RBRACKET'
                    ])
                ]),
                'EOF'
            ])
        )

    def _parse_expect(self, code, expected_tree):
        from antlr4 import TerminalNode
        from antlr4.InputStream import InputStream
        from antlr4.CommonTokenStream import CommonTokenStream
        from lexparse import LXScriptLexer, LXScriptParser

        lexer = LXScriptLexer(InputStream(code))
        parser = LXScriptParser(CommonTokenStream(lexer))

        def type_tree(parse_tree):
            if isinstance(parse_tree, TerminalNode):
                return _name(parse_tree.getSymbol().type, True)
            else:
                return (
                    _name(parse_tree.getRuleIndex()),
                    [type_tree(child) for child in parse_tree.getChildren()],
                )

        actual_tree = type_tree(parser.lxscript())

        self.assertEquals(actual_tree, expected_tree)
