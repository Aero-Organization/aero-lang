from .ast import Number, String, Identifier, BinaryOp, Call, Program, Assign

class VirtualMachine:
    def __init__(self):
        self.variables = {}
        self.globals = {
            'print': self._builtin_print
        }

    def _builtin_print(self, *args):
        py_args = []
        for arg in args:
            if hasattr(arg, 'value'):
                py_args.append(arg.value)
            else:
                py_args.append(arg)
        print(*py_args, flush=True)

    def execute(self, program):
        if not isinstance(program, Program):
            raise TypeError("Expected Program AST node")
        for stmt in program.statements:
            self._eval(stmt)

    def _eval(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self._eval(stmt)
        elif isinstance(node, Assign):
            value = self._eval(node.value)
            self.variables[node.name] = value
            return value
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node
        elif isinstance(node, Identifier):
            if node.name in self.variables:
                return self.variables[node.name]
            elif node.name in self.globals:
                return self.globals[node.name]
            raise NameError(f"Undefined name: {node.name}")
        elif isinstance(node, BinaryOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            if node.op.name == 'PLUS':
                return left + right
            elif node.op.name == 'MINUS':
                return left - right
            else:
                raise RuntimeError(f"Unsupported operator: {node.op}")
        elif isinstance(node, Call):
            func = self._eval(node.func)
            args = [self._eval(arg) for arg in node.args]
            if callable(func):
                return func(*args)
            raise RuntimeError(f"{node.func.name} is not callable")
