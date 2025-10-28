from .lexer import Lexer, TokenType
from .ast import Number, BinaryOp, Identifier, String, Call

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self._parse_expression()

    def _parse_expression(self):
        left = self._parse_term()
        while self._current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._consume()
            right = self._parse_term()
            left = BinaryOp(op.type, left, right)
        return left

    def _parse_term(self):
        token = self._current()
        if token.type == TokenType.NUMBER:
            self.pos += 1
            return Number(token.value)
        elif token.type == TokenType.STRING:
            self.pos += 1
            return String(token.value)
        elif token.type == TokenType.IDENTIFIER:
            ident = Identifier(token.value)
            self.pos += 1
            if self._current().type == TokenType.LPAREN:
                self.pos += 1
                args = []
                if self._current().type != TokenType.RPAREN:
                    args.append(self._parse_expression())
                if self._current().type != TokenType.RPAREN:
                    raise SyntaxError("Expected )")
                self.pos += 1
                return Call(ident, args)
            return ident
        elif token.type == TokenType.LPAREN:
            self.pos += 1
            expr = self._parse_expression()
            if self._current().type != TokenType.RPAREN:
                raise SyntaxError("Expected )")
            self.pos += 1
            return expr
        else:
            raise SyntaxError(f"Unexpected token in term: {token.type}")

    def _current(self):
        return self.tokens[self.pos]

    def _consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token
