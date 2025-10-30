from enum import Enum

class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOL = "BOOL"

    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    PERCENT = "PERCENT"

    # Comparisons
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    # Logical
    AND = "AND"
    OR = "OR"

    # Assignment
    ASSIGN = "ASSIGN"

    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"

    # Keywords
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    TRUE = "TRUE"
    FALSE = "FALSE"

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
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
        }

    def _peek(self):
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        return '\0'

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            char = self.source[self.pos]

            if char.isspace():
                self.pos += 1
            elif char == '/':
                if self._peek() == '/':
                    while self.pos < len(self.source) and self.source[self.pos] != '\n':
                        self.pos += 1
                else:
                    raise SyntaxError(f"Unexpected character: {char}")
            elif char.isdigit():
                tokens.append(self._read_number())
            elif char.isalpha() or char == '_':
                tokens.append(self._read_identifier())
            elif char == '"':
                tokens.append(self._read_string())
            elif char == '+':
                tokens.append(Token(TokenType.PLUS, '+'))
                self.pos += 1
            elif char == '-':
                tokens.append(Token(TokenType.MINUS, '-'))
                self.pos += 1
            elif char == '*':
                tokens.append(Token(TokenType.STAR, '*'))
                self.pos += 1
            elif char == '/':
                tokens.append(Token(TokenType.SLASH, '/'))
                self.pos += 1
            elif char == '%':
                tokens.append(Token(TokenType.PERCENT, '%'))
                self.pos += 1
            elif char == '=':
                if self._peek() == '=':
                    tokens.append(Token(TokenType.EQUAL, '=='))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.ASSIGN, '='))
                    self.pos += 1
            elif char == '!':
                if self._peek() == '=':
                    tokens.append(Token(TokenType.NOT_EQUAL, '!='))
                    self.pos += 2
                else:
                    raise SyntaxError(f"Unexpected character: {char}")
            elif char == '<':
                if self._peek() == '=':
                    tokens.append(Token(TokenType.LESS_EQUAL, '<='))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.LESS, '<'))
                    self.pos += 1
            elif char == '>':
                if self._peek() == '=':
                    tokens.append(Token(TokenType.GREATER_EQUAL, '>='))
                    self.pos += 2
                else:
                    tokens.append(Token(TokenType.GREATER, '>'))
                    self.pos += 1
            elif char == '&':
                if self._peek() == '&':
                    tokens.append(Token(TokenType.AND, '&&'))
                    self.pos += 2
                else:
                    raise SyntaxError(f"Unexpected character: {char}")
            elif char == '|':
                if self._peek() == '|':
                    tokens.append(Token(TokenType.OR, '||'))
                    self.pos += 2
                else:
                    raise SyntaxError(f"Unexpected character: {char}")
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, '('))
                self.pos += 1
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, ')'))
                self.pos += 1
            elif char == '{':
                tokens.append(Token(TokenType.LBRACE, '{'))
                self.pos += 1
            elif char == '}':
                tokens.append(Token(TokenType.RBRACE, '}'))
                self.pos += 1
            elif char == ',':
                tokens.append(Token(TokenType.COMMA, ','))
                self.pos += 1
            elif char == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';'))
                self.pos += 1
            else:
                raise SyntaxError(f"Unexpected character: {char}")
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
        token_type = self.keywords.get(name, TokenType.IDENTIFIER)
        if token_type in (TokenType.TRUE, TokenType.FALSE):
            return Token(TokenType.BOOL, name == 'true')
        return Token(token_type, name)

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
