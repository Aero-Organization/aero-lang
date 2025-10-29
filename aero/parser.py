from .lexer import Lexer, TokenType
from .ast import Number, BinaryOp, Identifier, String, Call, Program, Assign

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self._current().type != TokenType.EOF:
            statements.append(self._parse_statement())
            # Optional: consume semicolon
            if self._current().type == TokenType.SEMICOLON:
                self.pos += 1
        return Program(statements)

    def _parse_expression(self):
        left = self._parse_term()
        while self._current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._consume()
            right = self._parse_term()
            left = BinaryOp(op.type, left, right)
        return left

    def _parse_statement(self):
        # Assignment: x = expr
        if (self._lookahead_is(TokenType.IDENTIFIER) and
            self._lookahead(1).type == TokenType.ASSIGN):
            name = self._consume().value
            self.pos += 1
            value = self._parse_expression()
            return Assign(name, value)
        # Expression statement (e.g., print(...))
        return self._parse_expression()

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
                    while self._current().type == TokenType.COMMA:
                        self.pos += 1
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
    
    # Helper
    def _lookahead(self, n):
        idx = self.pos + n
        if idx < len(self.tokens):
            return self.tokens[idx]
        return Token(TokenType.EOF, None)

    def _lookahead_is(self, tt):
        return self._current().type == tt
