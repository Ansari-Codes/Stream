from streamBlockages import StreamBlockage

class Expression:
    def __init__(self, expr, operators=None, variables=None, functions=None):
        self.expr: str = expr.strip()
        # Operators dict (maps custom operator → Python operator)
        self.operators = dict(operators or [])
        varis = variables or []
        functions = functions or []
        self.defined = [i.get('name') for i in varis] + [i.get('name') for i in functions]

    def filterOperators(self):
        """Tokenize expression into variables, numbers, and operators."""
        sorted_ops = sorted(self.operators.keys(), key=lambda x: -len(x))  # longest first
        filtered = []
        i = 0
        expr_len = len(self.expr)

        while i < expr_len:
            matched = False
            # Try to match an operator
            for op in sorted_ops:
                if self.expr[i:i+len(op)] == op:
                    filtered.append(op)
                    i += len(op)
                    matched = True
                    break
            if not matched:
                # Accumulate a word/variable/number
                word = ''
                while i < expr_len:
                    if any(self.expr[i:i+len(op)] == op for op in sorted_ops):
                        break
                    word += self.expr[i]
                    i += 1
                if word.strip():
                    filtered.append(word.strip())

        return filtered

    def toPy(self):
        """Convert custom expression into valid Python expression."""
        if not self.expr:
            return ''

        tokens = self.filterOperators()
        py_tokens = []

        for token in tokens:
            if token in self.operators:
                py_tokens.append(self.operators[token])
            else:
                # Number check (supports int & float)
                if token.replace('.', '', 1).isdigit():
                    py_tokens.append(token)
                else:
                    # Check if defined variable/function
                    if token not in self.defined:
                        raise StreamBlockage(
                            f"Name or function '{token}' is not defined in expression: {self.expr}"
                        )
                    py_tokens.append('___stream_' + token)

        return ' '.join(py_tokens)

