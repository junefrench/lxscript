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
    def test_system_literal_and_declaration(self):
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

    def test_setting_literal_and_identifier(self):
        self._parse_expect(
            "foo1 @ 50",
            ('lxscript', [
                ('setting', [
                    ('system', [
                        ('identifier', ['NAME', 'NUMBER'])
                    ]),
                    'AT',
                    ('level', ['NUMBER'])
                ]),
                'EOF'
            ])
        )

    def test_setting_declaration(self):
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

    def test_compound_setting(self):
        self._parse_expect(
            """
            {
                1 @ full
                foo @ out
                bar42 @ 25
            }
            """,
            ('lxscript', [
                ('setting', [
                    'LBRACE',
                    ('setting', [
                        ('system', [('identifier', ['NUMBER'])]),
                        'AT',
                        ('level', ['FULL'])
                    ]),
                    ('setting', [
                        ('system', [('identifier', ['NAME'])]),
                        'AT',
                        ('level', ['OUT'])
                    ]),
                    ('setting', [
                        ('system', [('identifier', ['NAME', 'NUMBER'])]),
                        'AT',
                        ('level', ['NUMBER'])
                    ]),
                    'RBRACE'
                ]),
                'EOF'
            ])
        )

    def test_sequence_literal_and_declaration(self):
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
        """
        Parse some code and check the resulting parse tree against the expected tree.
        :param code: The string of code to parse.
        :param expected_tree: The expected parse tree. A terminal node is simply written as a string (the name of the
        lexer rule matched). A non-terminal node in the tree is written as a tuple (rule, [child ...]) where 'rule' is
        the name of the parser rule represented by that node, and each child is either a string (for terminals) or
        another tuple.
        :return: Does not return a value, but asserts that the parse tree returned by parsing the given code matches the
        one specified by expected_tree.
        """
        from antlr4 import TerminalNode
        from antlr4.InputStream import InputStream
        from antlr4.CommonTokenStream import CommonTokenStream
        from lexparse import LXScriptLexer, LXScriptParser

        lexer = LXScriptLexer(InputStream(code))
        parser = LXScriptParser(CommonTokenStream(lexer))

        def type_tree(parse_tree):
            """Converts a parse tree to the format used to specify expected parse trees, as described above"""
            if isinstance(parse_tree, TerminalNode):
                return _name(parse_tree.getSymbol().type, True)
            else:
                return (
                    _name(parse_tree.getRuleIndex()),
                    [type_tree(child) for child in parse_tree.getChildren()],
                )

        actual_tree = type_tree(parser.lxscript())

        self.assertEquals(actual_tree, expected_tree)
