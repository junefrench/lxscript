import unittest


class LexerTest(unittest.TestCase):
    def test_number(self):
        self._lex_expect("42", [('NUMBER', '42')])

    def test_name(self):
        self._lex_expect("foo", [('NAME', 'foo')])

    def test_symbols_and_keywords(self):
        self._lex_expect("!${}[] out full @=", [
            'BANG',
            'DOLLARS',
            'LBRACE',
            'RBRACE',
            'LBRACKET',
            'RBRACKET',
            'OUT',
            'FULL',
            'AT',
            'EQUALS'
        ])

    def test_comment(self):
        self._lex_expect("#blah blah 42 = something\n# this is another comment", [])

    def test_mix(self):
        self._lex_expect("led12 = {foo bar} #cool stuff\n!1 = led12 @ out", [
            ('NAME', "led"),
            ('NUMBER', "12"),
            'EQUALS',
            'LBRACE',
            ('NAME', "foo"),
            ('NAME', "bar"),
            'RBRACE',
            'BANG',
            ('NUMBER', "1"),
            'EQUALS',
            ('NAME', "led"),
            ('NUMBER', "12"),
            'AT',
            'OUT'
        ])

    def _lex_expect(self, code, expected_tokens):
        """
        Run some code through the lexer and check the tokens it returns.
        :param code: The string of code to lex.
        :param expected_tokens: A list where the values are either token type constants or tuples of token type
            constants and token texts, with one item for each token expected in the lexer output from lexing the code.
        :return: Does not return a value, but asserts that the output of the lexer matches the expected output.
        """
        from antlr4.InputStream import InputStream
        from lexparse import LXScriptLexer
        import itertools

        lexer = LXScriptLexer(InputStream(code))
        actual_tokens = [
            (self._name(actual.type), actual.text) if type(expected) is tuple else self._name(actual.type)
            for expected, actual in itertools.zip_longest(expected_tokens, lexer.getAllTokens())
        ]

        self.assertEqual(actual_tokens, expected_tokens)

    def _name(self, rule):
        """Get the name of a lexer rule from its index"""
        from lexparse import LXScriptLexer

        return LXScriptLexer.symbolicNames[rule]


class ParserTest(unittest.TestCase):
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
                return self._name(parse_tree.getSymbol().type, True)
            else:
                return (
                    self._name(parse_tree.getRuleIndex()),
                    [type_tree(child) for child in parse_tree.getChildren()],
                )

        actual_tree = type_tree(parser.lxscript())

        self.assertEquals(actual_tree, expected_tree)

    def _name(self, rule, symbolic=False):
        """Get the name of a parser rule (or of a terminal, if symbolic is True) from its rule index"""
        from lexparse import LXScriptParser

        if symbolic and (rule == -1):
            return 'EOF'
        else:
            return (LXScriptParser.symbolicNames if symbolic else LXScriptParser.ruleNames)[rule]
