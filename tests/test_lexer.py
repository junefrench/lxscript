import unittest


def _name(rule):
    from lexparse import LXScriptLexer

    return LXScriptLexer.symbolicNames[rule]


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
            (_name(actual.type), actual.text) if type(expected) is tuple else _name(actual.type)
            for expected, actual in itertools.zip_longest(expected_tokens, lexer.getAllTokens())
        ]
        self.assertEqual(actual_tokens, expected_tokens)
