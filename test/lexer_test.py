import unittest

from lexparse import LXScriptLexer


class LexerTest(unittest.TestCase):
    def test_number(self):
        self._lex_expect("42", [(LXScriptLexer.NUMBER, '42')])

    def test_name(self):
        self._lex_expect("foo", [(LXScriptLexer.NAME, 'foo')])

    def test_symbols_and_keywords(self):
        self._lex_expect("!${}[] out full @=", [
            LXScriptLexer.BANG,
            LXScriptLexer.DOLLARS,
            LXScriptLexer.LBRACE,
            LXScriptLexer.RBRACE,
            LXScriptLexer.LBRACKET,
            LXScriptLexer.RBRACKET,
            LXScriptLexer.OUT,
            LXScriptLexer.FULL,
            LXScriptLexer.AT,
            LXScriptLexer.EQUALS,
        ])

    def test_comment(self):
        self._lex_expect("#blah blah 42 = something\n# this is another comment", [])

    def test_mix(self):
        self._lex_expect("led12 = {foo bar} #cool stuff\n!1 = led12 @ out", [
            (LXScriptLexer.NAME, "led"),
            (LXScriptLexer.NUMBER, "12"),
            LXScriptLexer.EQUALS,
            LXScriptLexer.LBRACE,
            (LXScriptLexer.NAME, "foo"),
            (LXScriptLexer.NAME, "bar"),
            LXScriptLexer.RBRACE,
            LXScriptLexer.BANG,
            (LXScriptLexer.NUMBER, "1"),
            LXScriptLexer.EQUALS,
            (LXScriptLexer.NAME, "led"),
            (LXScriptLexer.NUMBER, "12"),
            LXScriptLexer.AT,
            LXScriptLexer.OUT,
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

        lexer = LXScriptLexer(InputStream(code))
        tokens = [(token.type, token.text) for token in lexer.getAllTokens()]
        expected_tokens = [
            (expected[0], expected[1]) if type(expected) is tuple else (expected, None) for expected in expected_tokens
        ]
        self.assertEqual(len(tokens), len(expected_tokens), msg="Wrong number of tokens produced")
        for actual, expected in zip(tokens, expected_tokens):
            msg = "Actual token {0} did not match expected token {1}".format(
                repr(actual[1]),
                repr(expected[1]) if expected[1] is not None else "(value not specified)"
            )
            self.assertEqual(actual[0], expected[0], msg=msg)
            if expected[1] is not None:
                self.assertEqual(actual[1], expected[1], msg=msg)
