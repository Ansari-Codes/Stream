import re
from streamBlockages import StreamBlockage
from baseLib import number, string

class Expression:
    def __init__(self, expr, operators=None, variables=None, functions=None, builtins = None):
        self.builtins = builtins or []
        self.expr: str = expr.strip()
        operators = operators or {}
        # operators: stream notation → replacement
        self.operators = dict(operators)
        # Sort operators by length descending
        self.sorted_ops = sorted(self.operators.keys(), key=lambda op: -len(op))
        varis = variables or []
        functions = functions or []
        self.defined = [i.get('name') for i in varis] + [i.get('name') for i in functions] + self.builtins

    def flatten(self):
        tokens = []
        i = 0
        expr_len = len(self.expr)
        while i < expr_len:
            if self.expr[i].isspace():
                i += 1
                continue
            # string literal
            if self.expr[i] in '"\'':
                quote = self.expr[i]
                i += 1
                start = i
                while i < expr_len:
                    if self.expr[i] == '\\':  # skip escaped char
                        i += 2
                    elif self.expr[i] == quote:
                        break
                    else:
                        i += 1
                tokens.append(self.expr[start-1:i+1])  # include quotes
                i += 1
                continue
            # Operators
            matched = False
            for op in self.sorted_ops:
                if self.expr[i:i+len(op)] == op:
                    tokens.append(op)
                    i += len(op)
                    matched = True
                    break
            if matched:
                continue
            # numbers, variables, functions, method names
            start = i
            if self.expr[i].isalpha() or self.expr[i] == "_":
                # identifiers (variables, functions, methods like to_number)
                i += 1
                while i < expr_len and (self.expr[i].isalnum() or self.expr[i] == "_"):
                    i += 1
            elif self.expr[i].isdigit() or (self.expr[i] == "." and i + 1 < expr_len and self.expr[i+1].isdigit()):
                # numbers (support floats like 3.14)
                i += 1
                while i < expr_len and (self.expr[i].isdigit() or self.expr[i] == "."):
                    i += 1
            else:
                i += 1
            token = self.expr[start:i]
            if token:
                tokens.append(token)
        return tokens

    def toPy(self):
        py_expr = []
        for token in self.flatten():
            token_str = str(token)
            # string literal
            # only "..." can be string. Parser will convert mutliline to "...\n...". So, no worries.
            if token_str.startswith('"') and token_str.endswith('"'):
                inner = token_str[1:-1].replace("\\", "\\\\")
                py_expr.append(f"string('{inner}')")
            # Operators
            elif token_str in self.operators:
                py_expr.append(self.operators[token_str])
            # Variables / functions
            elif token_str in self.defined:
                if token_str in self.builtins:
                    py_expr.append(token_str)
                else:
                    py_expr.append(f"___stream_{token_str}")
            # numbers
            elif re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', token_str):
                py_expr.append(token_str)
            else:
                try:
                    float(token_str)
                    py_expr.append(f"number({token_str})")
                except ValueError:
                    raise StreamBlockage(f"Undefined token: '{token_str}' in expression: {self.expr}")

        return ''.join(py_expr)

