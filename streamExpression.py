import re
from streamBlockages import StreamBlockage
from baseLib import number, string

class Expression:
    def __init__(self, expr, operators=None, variables=None, functions=None, builtins=None):
        self.builtins = builtins or []
        self.expr = expr.strip()
        self.operators = operators or {}
        self.sorted_ops = sorted(self.operators.keys(), key=lambda op: -len(op))
        varis = variables or []
        functions = functions or []
        self.defined = [i.get('name') for i in varis] + [i.get('name') for i in functions] + self.builtins

    def flatten_expr(self, expr):
        """Flatten expression into tokens, preserving chains and arguments."""
        tokens = []
        i = 0
        n = len(expr)

        while i < n:
            c = expr[i]
            if c.isspace():
                i += 1
                continue

            # String literal
            if c in '"\'':
                quote = c
                start = i
                i += 1
                while i < n:
                    if expr[i] == '\\':
                        i += 2
                    elif expr[i] == quote:
                        break
                    else:
                        i += 1
                tokens.append(expr[start:i+1])
                i += 1
                continue

            # Operators
            matched = False
            for op in self.sorted_ops:
                if expr[i:i+len(op)] == op:
                    tokens.append(op)
                    i += len(op)
                    matched = True
                    break
            if matched:
                continue

            # Number
            if c.isdigit() or (c == '.' and i+1 < n and expr[i+1].isdigit()):
                start = i
                i += 1
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    i += 1
                tokens.append(expr[start:i])
                continue

            # Identifier / chains
            if c.isalpha() or c == '_':
                start = i
                i += 1
                while i < n and (expr[i].isalnum() or expr[i] == '_'):
                    i += 1
                token = expr[start:i]

                # Collect .properties/methods and parentheses recursively
                while i < n and expr[i] in '.(':
                    if expr[i] == '.':
                        chain_start = i
                        i += 1
                        # next identifier
                        if i < n and (expr[i].isalpha() or expr[i] == '_'):
                            start = i
                            i += 1
                            while i < n and (expr[i].isalnum() or expr[i] == '_'):
                                i += 1
                            token += expr[chain_start:i]
                        else:
                            raise StreamBlockage(f"Invalid property access in: {expr}")
                    elif expr[i] == '(':
                        # parse balanced parentheses
                        parens = 1
                        start = i
                        i += 1
                        while i < n and parens > 0:
                            if expr[i] == '(':
                                parens += 1
                            elif expr[i] == ')':
                                parens -= 1
                            i += 1
                        token += expr[start:i]
                tokens.append(token)
                continue

            # Anything else
            tokens.append(c)
            i += 1

        return tokens

    def convert_token(self, token):
        """Convert a single token recursively."""
        token_str = str(token)

        # String literal
        if token_str.startswith('"') and token_str.endswith('"') or token_str.startswith("'") and token_str.endswith("'"):
            inner = token_str[1:-1]
            return f"string('{inner}')"

        # Number literal
        try:
            float(token_str)
            return f"number({token_str})"
        except ValueError:
            pass

        # Operator
        if token_str in self.operators:
            return self.operators[token_str]

        # Function/property chain or identifier
        m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)(.*)$', token_str)
        if m:
            root, rest = m.groups()

            if root not in self.defined:
                raise StreamBlockage(f"Undefined token: '{root}' in expression: {self.expr}")

            prefix = root if root in self.builtins else 'stream__' + root

            def process_rest(s):
                res = ''
                i = 0
                n = len(s)
                while i < n:
                    if s[i] == '(':
                        # parse parentheses recursively
                        parens = 1
                        start = i
                        i += 1
                        while i < n and parens > 0:
                            if s[i] == '(':
                                parens += 1
                            elif s[i] == ')':
                                parens -= 1
                            i += 1
                        inside = s[start+1:i-1]
                        converted_inside = Expression(
                            inside, self.operators,
                            [{'name': k} for k in self.defined],
                            [], self.builtins
                        ).toPy()
                        res += '(' + converted_inside + ')'
                    elif s[i] == '.':
                        res += '.'
                        i += 1
                        start = i
                        while i < n and (s[i].isalnum() or s[i] == '_'):
                            i += 1
                        sub_id = s[start:i]
                        # Treat numbers, strings, builtins, or variables correctly
                        if sub_id in self.builtins:
                            res += sub_id
                        else:
                            res += 'stream__' + sub_id
                    else:
                        res += s[i]
                        i += 1
                return res

            return prefix + process_rest(rest)

        # Single identifier
        if token_str in self.defined:
            return token_str if token_str in self.builtins else 'stream__' + token_str

        raise StreamBlockage(f"Undefined token: '{token_str}' in expression: {self.expr}")

    def toPy(self):
        tokens = self.flatten_expr(self.expr)
        return ''.join([self.convert_token(t) for t in tokens])
