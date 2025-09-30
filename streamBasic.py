
from abc import abstractmethod, ABC
from typing import Any
from streamBlockages import StreamBlockage
from types import MappingProxyType
from colorama import Fore, Style, init
from streamExpression import Expression
init(autoreset=True)

def deep_freeze(obj):
    if isinstance(obj, list):
        return tuple(deep_freeze(x) for x in obj)
    elif isinstance(obj, dict):
        return MappingProxyType({k: deep_freeze(v) for k, v in obj.items()})
    elif isinstance(obj, set):
        return frozenset(deep_freeze(x) for x in obj)
    elif isinstance(obj, tuple):
        return tuple(deep_freeze(x) for x in obj)
    else:
        return obj

class Operator:
    operators = {
        "===": " is ",
        "!==": " is not ",
        "<+": "<<",
        "+>": ">>",
        "//": "//",
        "!=": "!=",
        ":>": " in ",
        "!>": " not in ",
        "&&": "&",
        "||": "|",
        "><": "^",
        "~~": "~",
        "==": "==",
        ">=": ">=",
        "<=": "<=",
        "+": "+",
        "-": "-",
        "(": "(",
        ")": ")",
        "*": "*",
        "/": "/",
        "^": "**",
        "%": "%",
        "_": "_",
        "&": " and ",
        "|": " or ",
        "!": " not ",
        ".": ".",
        ">": ">",
        "<": "<",
    }

class Comment:
    def __init__(self, value):
        self.value = value

class ComStart:
    value = "#"

class ComEnd:
    value = "\n"

class String:
    def __init__(self, value, variables = None, functions = None):
        self.value = value
        self.variables = variables or [{}]
        self.functions = functions or [{}]
    
    def __str__(self) -> str:
        return f"{Style.DIM+Fore.RED}STRING{Style.RESET_ALL}({str(self.value)})"
    
    def to_python_string(self):
        """Convert Stream string to Python string with interpolation and escapes"""
        result = []
        i = 0
        n = len(self.value)
        has_interpolation = False

        while i < n:
            if self.value[i] == '\\' and i+1 < n:
                next_char = self.value[i+1]
                if next_char == 'n':
                    result.append('\n')
                    i += 2
                elif next_char == 't':
                    result.append('\t')
                    i += 2
                elif next_char == '"':
                    result.append('\"')
                    i += 2
                elif next_char == '\\':
                    result.append('\\')
                    i += 2
                elif next_char == '{':
                    result.append('{')
                    i += 2
                elif next_char == '}':
                    result.append('}')
                    i += 2
                else:
                    result.append('\\')
                    i += 1
            elif self.value[i] == '{' and i+1 < n and self.value[i+1] == '{':
                # Escaped opening brace
                result.append('{')
                i += 2
            elif self.value[i] == '}' and i+1 < n and self.value[i+1] == '}':
                # Escaped closing brace
                result.append('}')
                i += 2
            elif self.value[i] == '{':
                # Interpolation
                has_interpolation = True
                j = i + 1
                depth = 1
                expr = []
                while j < n and depth > 0:
                    if self.value[j] == '{':
                        depth += 1
                    elif self.value[j] == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    expr.append(self.value[j])
                    j += 1
                if depth == 0:
                    expr_str = Expression(''.join(expr),
                                         Operator.operators,
                                         self.variables,
                                         self.functions
                                         ).toPy()
                    result.append(f'{{{expr_str}}}')
                    i = j + 1
                else:
                    result.append(self.value[i])
                    i += 1
            else:
                result.append(self.value[i])
                i += 1

        final_str = ''.join(result)
        if has_interpolation:
            return f'f"{final_str}"'
        else:
            return f'"{final_str}"'

class StrStart:
    value = '"'

class StrEnd:
    value = '"'

class Code:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"Code({str(self.value)})"

class StatementEnd:
    value = '\\n'

class Variable:
    def __init__(self, name: str, value, indent):
        self.name  = name
        self.value = value
        self.indent = int(indent)
        
    def __getattr__(self, item):
        return getattr(self.value, item)

    def __repr__(self):
        return f'{Style.DIM}{Fore.LIGHTBLACK_EX}{"| " + " " * self.indent}{Style.RESET_ALL}{Fore.CYAN}Variable{Style.RESET_ALL}({self.name}={self.value!r})'

class Constant:
    def __init__(self, name: str, value, indent):
        frozen_value = deep_freeze(value)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "value", frozen_value)
        object.__setattr__(self, "indent", int(indent))

    def __setattr__(self, name: str, value) -> None:
        raise StreamBlockage(f"Constant {getattr(self, 'name', '?')} CANNOT be re-assigned.")

    def __getattr__(self, item):
        return getattr(self.value, item)

    def __repr__(self):
        return f'{Style.DIM}{Fore.LIGHTBLACK_EX}{"| " + " " * self.indent}{Style.RESET_ALL}{Fore.BLUE}Constant{Style.RESET_ALL}({self.name}={self.value!r})'

class IF:
    def __init__(self, value: str, indent):
        self.value = value
        self.indent = int(indent)

    def __repr__(self):
        return f'{Style.DIM}{Fore.LIGHTBLACK_EX}{"| " + " " * self.indent}{Style.RESET_ALL}{Fore.MAGENTA}If{Style.RESET_ALL}(value={self.value!r}):'

class Elif:
    def __init__(self, value: str, indent):
        self.value = value
        self.indent = int(indent)
    
    def __repr__(self):
        return f'{Style.DIM}{Fore.LIGHTBLACK_EX}{"| " + " " * self.indent}{Style.RESET_ALL}{Fore.MAGENTA}Elif{Style.RESET_ALL}(value={self.value!r}):'

class Else:
    def __init__(self, indent):
        self.value = 'else'
        self.indent = int(indent)
    
    def __repr__(self) -> str:
        return f'{Style.DIM}{Fore.LIGHTBLACK_EX}{"| " + " " * self.indent}{Style.RESET_ALL}{Fore.MAGENTA}Else{Style.RESET_ALL}():'

class Function:
    def __init__(self, name, params, indent):
        self.name = name
        self.params = params
        self.indent = indent
    
    def __repr__(self) -> str:
        return f'{Style.DIM}{Fore.LIGHTBLACK_EX}{"| " + " " * self.indent}{Style.RESET_ALL}{Style.DIM}{Fore.YELLOW}Function{Style.RESET_ALL}(name={self.name}, params="{self.params}"):'

class Return:
    def __init__(self, value, indent):
        self.value = value
        self.indent = indent
    
    def __repr__(self) -> str:
        return f'{Style.DIM}{Fore.LIGHTBLACK_EX}{"| " + " " * self.indent}{Style.RESET_ALL}{Fore.MAGENTA}Return{Style.RESET_ALL}({self.value})'
