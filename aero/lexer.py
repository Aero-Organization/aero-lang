import re
from enum import Enum

class TokenType(Enum):
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    STRING = "STRING"
    EOF = "EOF"

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            char = self.source[self.pos]

            if char.isspace():
                self.pos += 1
            elif char.isdigit():
                tokens.append(self._read_number())
            elif char.isalpha() or char == '_':
                tokens.append(self._read_identifier())
            elif char == '+':
                tokens.append(Token(TokenType.PLUS, '+'))
                self.pos += 1
            elif char == '-':
                tokens.append(Token(TokenType.MINUS, '-'))
                self.pos += 1
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, '('))
                self.pos += 1
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, ')'))
                self.pos += 1
            elif char == '"':
                tokens.append(self._read_string())
            else:
                raise SyntaxError(f"Unexpected character: {char} at position {self.pos}")
        tokens.append(Token(TokenType.EOF, None))
        return tokens

    def _read_number(self):
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
        return Token(TokenType.NUMBER, int(self.source[start:self.pos]))

    def _read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isalnum() or self.source[self.pos] == '_':
            self.pos += 1
        name = self.source[start:self.pos]
        return Token(TokenType.IDENTIFIER, name)

    def _read_string(self):
        self.pos += 1
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\\':
                self.pos += 2
            else:
                self.pos += 1
        if self.pos >= len(self.source):
            raise SyntaxError("Unterminated string")
        value = self.source[start:self.pos]
        self.pos += 1
        return Token(TokenType.STRING, value)
