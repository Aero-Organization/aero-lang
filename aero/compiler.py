from .lexer import Lexer
from .parser import Parser

def compile_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    # Simplified: return AST as "bytecode" for v0.0.1a
    return ast
