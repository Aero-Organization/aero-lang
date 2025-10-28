from .ast import Number, String, Identifier, BinaryOp, Call

class VirtualMachine:
    def __init__(self):
        self.globals = {
            'print': self._builtin_print
        }

    def _builtin_print(self, *args):
        #
        py_args = []
        for arg in args:
            if isinstance(arg, String):
                py_args.append(arg.value)
            elif isinstance(arg, Number):
                py_args.append(arg.value)
            else:
                py_args.append(arg)
        print(*py_args)

    def execute(self, ast):
        result = self._eval(ast)



    def _eval(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node
        elif isinstance(node, Identifier):
            name = node.name
            if name in self.globals:
                return self.globals[name]
            else:
                raise NameError(f"Undefined variable: {name}")
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
            else:
                raise RuntimeError(f"{node.func.name} is not callable")
        else:
            raise RuntimeError(f"Unknown AST node: {type(node)}")
