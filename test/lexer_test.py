import unittest


class LexerTest(unittest.TestCase):
    def test_empty_show(self):
        lexer = self._lex(
            """
            show
            """
        )
        self.assertEqual(lexer.nextToken().type, lexer.SHOW)

    def _lex(self, code):
        from lexparse import LXScriptLexer
        from antlr4.InputStream import InputStream

        return LXScriptLexer(InputStream(code))
