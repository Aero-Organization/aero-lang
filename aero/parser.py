from .ast import *
from .lexer import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _current(self):
        return self.tokens[self.pos]

    def _consume(self, expected_type=None):
        if expected_type and self._current().type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {self._current().type}")
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _match(self, token_type):
        if self._current().type == token_type:
            self.pos += 1
            return True
        return False

    def parse(self):
        statements = []
        while self._current().type != TokenType.EOF:
            statements.append(self._parse_statement())
            if self._current().type == TokenType.SEMICOLON:
                self.pos += 1
        return Program(statements)

    def _parse_statement(self):
        if self._match(TokenType.IF):
            self._consume(TokenType.LPAREN)
            condition = self._parse_expression()
            self._consume(TokenType.RPAREN)
            then_branch = self._parse_statement()
            else_branch = None
            if self._match(TokenType.ELSE):
                else_branch = self._parse_statement()
            return If(condition, then_branch, else_branch)
        elif self._match(TokenType.WHILE):
            self._consume(TokenType.LPAREN)
            condition = self._parse_expression()
            self._consume(TokenType.RPAREN)
            body = self._parse_statement()
            return While(condition, body)
        elif self._current().type == TokenType.LBRACE:
            return self._parse_block()
        elif (self._current().type == TokenType.IDENTIFIER and
              self._peek_type(1) == TokenType.ASSIGN):
            name = self._consume().value
            self._consume(TokenType.ASSIGN)
            value = self._parse_expression()
            return Assign(name, value)
        else:
            return self._parse_expression()

    def _parse_block(self):
        self._consume(TokenType.LBRACE)
        statements = []
        while self._current().type != TokenType.RBRACE and self._current().type != TokenType.EOF:
            statements.append(self._parse_statement())
            if self._current().type == TokenType.SEMICOLON:
                self.pos += 1
        self._consume(TokenType.RBRACE)
        return Block(statements)

    def _parse_expression(self):
        return self._parse_logical_or()

    def _parse_logical_or(self):
        left = self._parse_logical_and()
        while self._match(TokenType.OR):
            right = self._parse_logical_and()
            left = BinaryOp(TokenType.OR, left, right)
        return left

    def _parse_logical_and(self):
        left = self._parse_equality()
        while self._match(TokenType.AND):
            right = self._parse_equality()
            left = BinaryOp(TokenType.AND, left, right)
        return left

    def _parse_equality(self):
        left = self._parse_comparison()
        while self._current().type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self._consume()
            right = self._parse_comparison()
            left = BinaryOp(op.type, left, right)
        return left

    def _parse_comparison(self):
        left = self._parse_term()
        while self._current().type in (
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL
        ):
            op = self._consume()
            right = self._parse_term()
            left = BinaryOp(op.type, left, right)
        return left

    def _parse_term(self):
        left = self._parse_factor()
        while self._current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._consume()
            right = self._parse_factor()
            left = BinaryOp(op.type, left, right)
        return left

    def _parse_factor(self):
        left = self._parse_unary()
        while self._current().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self._consume()
            right = self._parse_unary()
            left = BinaryOp(op.type, left, right)
        return left

    def _parse_unary(self):
        # No unary operators in v0.0.3a
        return self._parse_call()

    def _parse_call(self):
        expr = self._parse_primary()
        while self._match(TokenType.LPAREN):
            args = []
            if self._current().type != TokenType.RPAREN:
                args.append(self._parse_expression())
                while self._match(TokenType.COMMA):
                    args.append(self._parse_expression())
            self._consume(TokenType.RPAREN)
            expr = Call(expr, args)
        return expr

    def _parse_primary(self):
        token = self._current()
        if token.type == TokenType.NUMBER:
            self.pos += 1
            return Number(token.value)
        elif token.type == TokenType.STRING:
            self.pos += 1
            return String(token.value)
        elif token.type == TokenType.BOOL:
            self.pos += 1
            return Bool(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.pos += 1
            return Identifier(token.value)
        elif token.type == TokenType.LPAREN:
            self.pos += 1
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token.type}")

    def _peek_type(self, n):
        idx = self.pos + n
        if idx < len(self.tokens):
            return self.tokens[idx].type
        return TokenType.EOF
