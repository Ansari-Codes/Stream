from streamBlockages import StreamBlockage

class Expression:
    def __init__(self, expr,
                operators = None,
                variables = None,
                functions = None
            ):
        self.expr :str = expr
        varis = variables or {}
        self.operators = operators or {}
        functions = functions or {}
        self.defined = [i for i in {**varis, **functions}]
    
    def toPy(self):
        line = []
        word = []
        self.expr = self.expr.replace('++', '.inc()').replace('--', '.dec()')
        if self.expr.strip()[-1] not in '()' and self.expr.strip()[-1] in self.operators:
            raise StreamBlockage(f"\nMaybe you forgot to place something at end?\nOr, mistakenly placed an operator?\n\t {self.expr.strip()}\nExpression ended with an operator!")
        for n,i in enumerate(self.expr.strip() + "+"):
            if not i.strip():
                continue
            if i in self.operators:
                if word:
                    word_ = ''.join(word)
                    if word_.isdigit():
                        line.append(word_)
                    else:
                        if word_ in ["inc", "dec"]:
                            line.append(word_)
                        elif word_ not in self.defined and ((n+1) < len(self.expr.strip())) and self.expr.strip()[n+1]:
                            raise StreamBlockage(f"Callable {word_} is not defined!")
                        elif word_ not in self.defined:
                            raise StreamBlockage(f"Name {word_} is not defined!")
                        else:
                            line.append('py_' + word_ + '.value')
                word.clear()
                try:
                    line.append(self.operators[i])
                except KeyError:
                    raise StreamBlockage(f"UnKnown Operator: '{i}'")
            else:
                word.append(i)
        return ''.join(line[:len(line) - 1])

class Operator:
    operators = {
            "+":  "+",  
            "-":  "-", 
            "(":  "(", 
            ")":  ")",
            "*":  "*", 
            "/":  "/",
            "//":"//",
            "^": "**",
            "%":  "%", 
            "_":  "_",
            "&":" and ",
            "|": " or ",
            "!": " not ",
            ".": "."
        }
