import unittest

from lexparse import *


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

    def test_invalid_character(self):
        with self.assertRaises(LexError):
            self._lex_expect("+", None)

    def _lex_expect(self, code, expected_tokens):
        """
        Run some code through the lexer and check the tokens it returns.
        :param code: The string of code to lex.
        :param expected_tokens: A list where the values are either token type constants or tuples of token type
            constants and token texts, with one item for each token expected in the lexer output from lexing the code.
        :return: Does not return a value, but asserts that the output of the lexer matches the expected output.
        """
        from antlr4.InputStream import InputStream
        import itertools

        lexer = LXScriptLexer(InputStream(code))
        actual_tokens = [
            (self._name(actual.type), actual.text) if type(expected) is tuple else self._name(actual.type)
            for expected, actual in itertools.zip_longest(expected_tokens, lexer.getAllTokens())
        ]

        self.assertEqual(actual_tokens, expected_tokens)

    def _name(self, rule):
        """Get the name of a lexer rule from its index"""

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

    def test_system_reference(self):
        self._parse_expect(
            "1 = 2",
            ('lxscript', [
                ('declaration', [
                    ('identifier', ['NUMBER']),
                    'EQUALS',
                    ('system', [('identifier', ['NUMBER'])])
                ]),
                'EOF'
            ])
        )

    def test_system_compound(self):
        self._parse_expect(
            "1 = {2 3}",
            ('lxscript', [
                ('declaration', [
                    ('identifier', ['NUMBER']),
                    'EQUALS',
                    ('system', [
                        'LBRACE',
                        ('system', [('identifier', ['NUMBER'])]),
                        ('system', [('identifier', ['NUMBER'])]),
                        'RBRACE'
                    ])
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

    def test_setting_compound(self):
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

    def test_setting_partial_reference(self):
        self._parse_expect(
            "1 @ !foo",
            ('lxscript', [
                ('setting', [
                    ('system', [('identifier', ['NUMBER'])]),
                    'AT',
                    ('setting', ['BANG', ('identifier', ['NAME'])])
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

    def test_complex_example(self):
        self._parse_expect(
            """
            # Systems
            1 = @@1 ## system 1 is a dimmer at address 1
            2 = @@2
            3 = @@3
            top1 = @@51
            top2 = @@52
            top3 = @@53
            house = {@@51 @@52 @@53 @@54} # system house includes four different dimmers

            front = {1 2 3} # system front is a group including systems 1, 2, and 3
            top = {top1 top2 top3}

            !blackout = {
                # setting blackout is all channels out
                front @ out
                top @ out
                house @ out
            }

            !spot_sl = {
                # a setting for a certain look (a spotlight stage left)
                front @ out
                top @ out
                # later settings override earlier ones, so this overrides the setting of 1 to out in 'front @ out'
                1 @ full
            }
            $main = [
                # A simple cue list
                !blackout
                !spot_sl
                {
                    front @ full
                    top @ 50
                }
                front @ !blackout # recall just system front from setting blackout
                !blackout
            ]

            $check = [
                # This would bring on fixtures to 10% one at a time for dimmer check
                {!blackout 1 @ 10}
                {!blackout 2 @ 10}
                {!blackout 3 @ 10}
                {!blackout top1 @ 10}
                {!blackout top2 @ 10}
                {!blackout top3 @ 10}
            ]
            """,
            ('lxscript',
             [('declaration',
               [('identifier', ['NUMBER']),
                'EQUALS',
                ('system', ['AT', 'AT', 'NUMBER'])]),
              ('declaration',
               [('identifier', ['NUMBER']),
                'EQUALS',
                ('system', ['AT', 'AT', 'NUMBER'])]),
              ('declaration',
               [('identifier', ['NUMBER']),
                'EQUALS',
                ('system', ['AT', 'AT', 'NUMBER'])]),
              ('declaration',
               [('identifier', ['NAME', 'NUMBER']),
                'EQUALS',
                ('system', ['AT', 'AT', 'NUMBER'])]),
              ('declaration',
               [('identifier', ['NAME', 'NUMBER']),
                'EQUALS',
                ('system', ['AT', 'AT', 'NUMBER'])]),
              ('declaration',
               [('identifier', ['NAME', 'NUMBER']),
                'EQUALS',
                ('system', ['AT', 'AT', 'NUMBER'])]),
              ('declaration',
               [('identifier', ['NAME']),
                'EQUALS',
                ('system',
                 ['LBRACE',
                  ('system', ['AT', 'AT', 'NUMBER']),
                  ('system', ['AT', 'AT', 'NUMBER']),
                  ('system', ['AT', 'AT', 'NUMBER']),
                  ('system', ['AT', 'AT', 'NUMBER']),
                  'RBRACE'])]),
              ('declaration',
               [('identifier', ['NAME']),
                'EQUALS',
                ('system',
                 ['LBRACE',
                  ('system', [('identifier', ['NUMBER'])]),
                  ('system', [('identifier', ['NUMBER'])]),
                  ('system', [('identifier', ['NUMBER'])]),
                  'RBRACE'])]),
              ('declaration',
               [('identifier', ['NAME']),
                'EQUALS',
                ('system',
                 ['LBRACE',
                  ('system', [('identifier', ['NAME', 'NUMBER'])]),
                  ('system', [('identifier', ['NAME', 'NUMBER'])]),
                  ('system', [('identifier', ['NAME', 'NUMBER'])]),
                  'RBRACE'])]),
              ('declaration',
               ['BANG',
                ('identifier', ['NAME']),
                'EQUALS',
                ('setting',
                 ['LBRACE',
                  ('setting',
                   [('system', [('identifier', ['NAME'])]),
                    'AT',
                    ('level', ['OUT'])]),
                  ('setting',
                   [('system', [('identifier', ['NAME'])]),
                    'AT',
                    ('level', ['OUT'])]),
                  ('setting',
                   [('system', [('identifier', ['NAME'])]),
                    'AT',
                    ('level', ['OUT'])]),
                  'RBRACE'])]),
              ('declaration',
               ['BANG',
                ('identifier', ['NAME']),
                'EQUALS',
                ('setting',
                 ['LBRACE',
                  ('setting',
                   [('system', [('identifier', ['NAME'])]),
                    'AT',
                    ('level', ['OUT'])]),
                  ('setting',
                   [('system', [('identifier', ['NAME'])]),
                    'AT',
                    ('level', ['OUT'])]),
                  ('setting',
                   [('system', [('identifier', ['NUMBER'])]),
                    'AT',
                    ('level', ['FULL'])]),
                  'RBRACE'])]),
              ('declaration',
               ['DOLLARS',
                ('identifier', ['NAME']),
                'EQUALS',
                ('sequence',
                 ['LBRACKET',
                  ('setting', ['BANG', ('identifier', ['NAME'])]),
                  ('setting', ['BANG', ('identifier', ['NAME'])]),
                  ('setting',
                   ['LBRACE',
                    ('setting',
                     [('system', [('identifier', ['NAME'])]),
                      'AT',
                      ('level', ['FULL'])]),
                    ('setting',
                     [('system', [('identifier', ['NAME'])]),
                      'AT',
                      ('level', ['NUMBER'])]),
                    'RBRACE']),
                  ('setting',
                   [('system', [('identifier', ['NAME'])]),
                    'AT',
                    ('setting', ['BANG', ('identifier', ['NAME'])])]),
                  ('setting', ['BANG', ('identifier', ['NAME'])]),
                  'RBRACKET'])]),
              ('declaration',
               ['DOLLARS',
                ('identifier', ['NAME']),
                'EQUALS',
                ('sequence',
                 ['LBRACKET',
                  ('setting',
                   ['LBRACE',
                    ('setting', ['BANG', ('identifier', ['NAME'])]),
                    ('setting',
                     [('system', [('identifier', ['NUMBER'])]),
                      'AT',
                      ('level', ['NUMBER'])]),
                    'RBRACE']),
                  ('setting',
                   ['LBRACE',
                    ('setting', ['BANG', ('identifier', ['NAME'])]),
                    ('setting',
                     [('system', [('identifier', ['NUMBER'])]),
                      'AT',
                      ('level', ['NUMBER'])]),
                    'RBRACE']),
                  ('setting',
                   ['LBRACE',
                    ('setting', ['BANG', ('identifier', ['NAME'])]),
                    ('setting',
                     [('system', [('identifier', ['NUMBER'])]),
                      'AT',
                      ('level', ['NUMBER'])]),
                    'RBRACE']),
                  ('setting',
                   ['LBRACE',
                    ('setting', ['BANG', ('identifier', ['NAME'])]),
                    ('setting',
                     [('system', [('identifier', ['NAME', 'NUMBER'])]),
                      'AT',
                      ('level', ['NUMBER'])]),
                    'RBRACE']),
                  ('setting',
                   ['LBRACE',
                    ('setting', ['BANG', ('identifier', ['NAME'])]),
                    ('setting',
                     [('system', [('identifier', ['NAME', 'NUMBER'])]),
                      'AT',
                      ('level', ['NUMBER'])]),
                    'RBRACE']),
                  ('setting',
                   ['LBRACE',
                    ('setting', ['BANG', ('identifier', ['NAME'])]),
                    ('setting',
                     [('system', [('identifier', ['NAME', 'NUMBER'])]),
                      'AT',
                      ('level', ['NUMBER'])]),
                    'RBRACE']),
                  'RBRACKET'])]),
              'EOF'])
        )

    def test_invalid_declaration(self):
        with self.assertRaises(ParseError):
            self._parse_expect("foo = !bar", None)

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

        if symbolic and (rule == -1):
            return 'EOF'
        else:
            return (LXScriptParser.symbolicNames if symbolic else LXScriptParser.ruleNames)[rule]
