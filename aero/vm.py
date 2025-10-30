from .lexer import TokenType
from .ast import *

class VirtualMachine:
    def __init__(self):
        self.variables = {}
        self.globals = {
            'print': self._builtin_print
        }

    def execute(self, program):
        if not isinstance(program, Program):
            raise TypeError("Expected Program AST node")
        for stmt in program.statements:
            self._eval(stmt)

    def _eval(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self._eval(stmt)
        elif isinstance(node, Block):
            for stmt in node.statements:
                self._eval(stmt)
        elif isinstance(node, Assign):
            value = self._eval(node.value)
            self.variables[node.name] = value
            return value
        elif isinstance(node, If):
            cond = self._eval(node.condition)
            if self._is_truthy(cond):
                return self._eval(node.then_branch)
            elif node.else_branch:
                return self._eval(node.else_branch)
        elif isinstance(node, While):
            while self._is_truthy(self._eval(node.condition)):
                self._eval(node.body)
        elif isinstance(node, Call):
            func = self._eval(node.func)
            args = [self._eval(arg) for arg in node.args]
            if callable(func):
                return func(*args)
            raise RuntimeError(f"{node.func.name} is not callable")
        elif isinstance(node, Identifier):
            if node.name in self.variables:
                return self.variables[node.name]
            elif node.name in self.globals:
                return self.globals[node.name]
            raise NameError(f"Undefined name: {node.name}")
        elif isinstance(node, Number):
            return node
        elif isinstance(node, String):
            return node
        elif isinstance(node, Bool):
            return node
        elif isinstance(node, BinaryOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            return self._eval_binary_op(node.op, left, right)
        else:
            raise RuntimeError(f"Unknown AST node: {type(node)}")

    def _eval_binary_op(self, op, left, right):
        # Unwrap values
        lval = left.value if hasattr(left, 'value') else left
        rval = right.value if hasattr(right, 'value') else right

        if op == TokenType.PLUS:
            if isinstance(left, String) or isinstance(right, String):
                return String(str(lval) + str(rval))
            return Number(lval + rval)
        elif op == TokenType.MINUS:
            return Number(lval - rval)
        elif op == TokenType.STAR:
            return Number(lval * rval)
        elif op == TokenType.SLASH:
            return Number(lval // rval)  # Integer division
        elif op == TokenType.PERCENT:
            return Number(lval % rval)
        elif op == TokenType.EQUAL:
            return Bool(lval == rval)
        elif op == TokenType.NOT_EQUAL:
            return Bool(lval != rval)
        elif op == TokenType.LESS:
            return Bool(lval < rval)
        elif op == TokenType.LESS_EQUAL:
            return Bool(lval <= rval)
        elif op == TokenType.GREATER:
            return Bool(lval > rval)
        elif op == TokenType.GREATER_EQUAL:
            return Bool(lval >= rval)
        elif op == TokenType.AND:
            return Bool(self._is_truthy(left) and self._is_truthy(right))
        elif op == TokenType.OR:
            return Bool(self._is_truthy(left) or self._is_truthy(right))
        else:
            raise RuntimeError(f"Unsupported operator: {op}")

    def _is_truthy(self, val):
        if isinstance(val, Bool):
            return val.value
        if isinstance(val, Number):
            return val.value != 0
        if isinstance(val, String):
            return len(val.value) > 0
        return bool(val)

    def _builtin_print(self, *args):
        py_args = []
        for arg in args:
            if hasattr(arg, 'value'):
                py_args.append(arg.value)
            else:
                py_args.append(arg)
        print(*py_args, flush=True)
