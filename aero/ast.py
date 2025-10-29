class ASTNode:
    pass

class Program(ASTNode):
    """Top-level container for statements"""
    def __init__(self, statements):
        self.statements = statements

class Assign(ASTNode):
    """Variable assignment: x = 5"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Call(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args
