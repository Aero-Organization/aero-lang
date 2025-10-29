from .lexer import Lexer
from .parser import Parser

def compile_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
