
from abc import abstractmethod, ABC
from typing import Any
from streamBlockages import StreamBlockage
from types import MappingProxyType
from colorama import Fore, Style, init

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

class Comment:
    def __init__(self, value):
        self.value = value

class ComStart:
    value = "#"

class ComEnd:
    value = "\n"

class String:
    def __init__(self, value):
        self.value = value
    
    def __str__(self) -> str:
        return f"{Style.DIM+Fore.RED}STRING{Style.RESET_ALL}({str(self.value)})"

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

class Number:
    def __init__(self, value):
        self.value = float(value)
    
    def inc(self):
        self.value += 1
    
    def dec(self):
        self.value -= 1

    def __str__(self) -> str:
        return f"{Fore.GREEN}Number{Style.RESET_ALL}{str(self.value)})"

class Variable:
    def __init__(self, name: str, value, indent):
        self.name  = name
        self.value = value
        self.indent = int(indent)
        
    def __getattr__(self, item):
        return getattr(self.value, item)

    def __repr__(self):
        return f"{' ' * self.indent}{Fore.CYAN}Variable{Style.RESET_ALL}({self.name}={self.value!r}, indent={self.indent})"

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
        return f"{' ' * self.indent}{Fore.BLUE}Constant{Style.RESET_ALL}({self.name}={self.value!r}, indent={self.indent})"

class IF:
    def __init__(self, value: str, indent):
        self.value = value
        self.indent = int(indent)

    def __repr__(self):
        return f"{' ' * self.indent}{Fore.MAGENTA}If{Style.RESET_ALL}(value={self.value!r}, indent={self.indent})"

class Elif:
    def __init__(self, value: str, indent):
        self.value = value
        self.indent = int(indent)
    
    def __repr__(self):
        return f"{Fore.MAGENTA}Elif{Style.RESET_ALL}(value={self.value!r}, indent={self.indent})"

class Else:
    def __init__(self, indent):
        self.value = 'else'
        self.indent = int(indent)
    
    def __repr__(self) -> str:
        return f'{" " * self.indent}{Fore.MAGENTA}Else{Style.RESET_ALL}()'
