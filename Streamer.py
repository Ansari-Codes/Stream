from pprint import pprint
from streamBasic import *
from streamExpression import Expression
from string import ascii_letters, digits
from reDefs import reg

letters = ascii_letters + digits

isi = isinstance

class Parser:
    def __init__(self, code: str):
        self.code = code
        self.tokens = []
        self._filtered = []

    def filterStringAndComments(self):
        tokens = []
        in_string = False
        in_comment = False
        buffer = ""
        line_start = True
        in_escape = False

        def flush_buffer():
            nonlocal buffer
            if buffer:
                tokens.append(Code(buffer))
                buffer = ""

        for ch in self.code:
            # --- inside string ---
            if in_string:
                if in_escape:
                    buffer += ch
                    in_escape = False
                    continue
                if ch == '\\':
                    in_escape = True
                    continue
                if ch == '"':
                    if buffer:
                        tokens.append(String(buffer))
                        buffer = ""
                    tokens.append(StrEnd())
                    in_string = False
                else:
                    buffer += ch
                continue

            # --- inside comment ---
            if in_comment:
                if ch == "\n":
                    if buffer:
                        tokens.append(Comment(buffer))
                        buffer = ""
                    tokens.append(ComEnd())
                    in_comment = False
                    tokens.append(StatementEnd())
                    line_start = True
                else:
                    buffer += ch
                continue

            # --- normal parsing ---
            if ch == '"':
                flush_buffer()
                tokens.append(StrStart())
                in_string = True

            elif ch == "#":
                flush_buffer()
                tokens.append(ComStart())
                in_comment = True

            elif ch in ";\n":
                flush_buffer()
                tokens.append(StatementEnd())
                line_start = True

            elif ch.isspace():
                if line_start:   # keep indentation
                    buffer += ch
                else:
                    flush_buffer()

            elif ch not in letters:
                flush_buffer()
                tokens.append(Code(ch))

            else:
                buffer += ch
                line_start = False

        flush_buffer()
        # --- Purification
        ast = []
        for i in tokens:
            if isi(i, (ComStart, Comment, StrStart, StrEnd)):
                continue
            elif isi(i, String):
                ast.append(String(i.value))
            elif isi(i, Code):
                ast.append(i)
            elif isi(i, StatementEnd):
                ast.append(StatementEnd())
        return ast

PREFIX_WITH_GT = ['-', '>', '=', '~']

class Converter:
    def __init__(self, ast = None):
        self.ast = ast or []
    
    def _token(self, i: int) -> Code|None:
        if i < len(self.ast):
            return self.ast[i]
        else:
            return None
    
    def flatten(self):
        flattened = []
        line = []
        skipes = []
        indent = ""
        for idx, i in enumerate(self.ast):
            if skipes and skipes[-1]:
                skipes.pop()
                continue
            if isi(i, String):
                line.append(f"\"{i.value}\"")
            elif isi(i, Code):
                value = ''
                code_val = i.value
                # Capture indentation at start of line
                if not line and code_val and code_val[0].isspace():
                    indent = ""
                    for ch in code_val:
                        if ch.isspace():
                            indent += ch
                        else:
                            break
                    value += indent + code_val[len(indent):].strip()
                else:
                    value += code_val.strip()
                next_i = self._token(idx+1)
                if next_i:
                    next_i = next_i.value.strip().lower()
                if value in PREFIX_WITH_GT and next_i == '>':
                    value += '>'
                    skipes.append(True)
                elif value in ['=', '>', '<', '!'] and next_i == '=':
                    value += '='
                    skipes.append(True)
                elif value in [':'] and next_i == '?':
                    value += '?'
                    skipes.append(True)
                line.append(value)
            elif isi(i, StatementEnd):
                if line:
                    flattened.append(''.join(line))
                line.clear()
                indent = ""
            else:
                raise StreamBlockage(f"Unexpected token: {i}")
        return flattened
    
    def toAst(self):
        lines = self.flatten()
        ast = []
        for line in lines:
            if not line.strip(): continue
            typ, m, indent = reg(line)
            if m:
                if typ == 'var':
                    name, value = m
                    ast.append(Variable(name.strip(), value.strip(), indent))
                elif typ == 'const':
                    name, value = m
                    ast.append(Constant(name.strip(), value.strip(), indent))
                elif typ == 'if':
                    ast.append(IF(m[0].strip(), indent))
                elif typ == 'elif':
                    ast.append(Elif(m[0].strip(), indent))
                elif typ == 'else':
                    ast.append(Else(indent))
                elif typ == 'func':
                    name, params = m
                    ast.append(Function(name, params, indent))
                elif typ == 'return':
                    ast.append(Return(m[0], indent))
            else:
                raise StreamBlockage(f"Unexpected statement: {line}")
        return ast

class Generator:
    def __init__(self, code = None):
        self.ast = code or []
        self.variables = [{}]
        self.functions = [{}]
    
    def find_in_vars(self, value, by='name'):
        return [i for i in self.variables
                if i.get(by) == value]
    
    def convert(self):
        histroy = []
        lines = ['from baseLib import *']
        for idx, i in enumerate(self.ast):
            ind = " " * i.indent
            if isi(i, (Variable, Constant)):
                name = i.name
                value_str = i.value
                is_const = isi(i, Constant)
                exists = self.find_in_vars(name)
                exists = exists[0] if exists else {}
                
                # Check for string literal assignment
                if isinstance(value_str, str) and value_str.startswith('"') and value_str.endswith('"'):
                    # Process string for interpolation
                    string_content = value_str[1:-1]  # Remove quotes
                    stream_string = String(string_content, self.variables, self.functions)
                    ___stream_value = stream_string.to_python_string()
                else:
                    value = Expression(
                        value_str,
                        Operator.operators,
                        variables=self.variables,
                        functions=self.functions
                    )
                    ___stream_value = value.toPy()
                
                if exists and ind == exists.get('indent'):
                    if exists.get('is_const'):
                        raise StreamBlockage("You cannot re-assign a constant.")
                    else:
                        lines.append(f'{ind}___stream_{name} = {___stream_value}')
                        exists.update({'value': value_str})
                else:
                    lines.append(f'{ind}___stream_{name} = {___stream_value}')
                    self.variables.append({
                        'name': name,
                        'is_const': is_const,
                        'value': value_str,
                        'indent': ind,
                        'id': len(self.variables)
                    })
            elif isi(i, (IF, Elif)):
                condition = Expression(
                        i.value,
                        Operator.operators,
                        variables=self.variables,
                        functions=self.functions
                    )
                if isi(i, IF):
                    lines.append(f'{ind}if {condition.toPy()}:')
                elif isi(i, Elif):
                    lines.append(f'{ind}elif {condition.toPy()}:')
            elif isi(i, (Else)):
                lines.append(f'{ind}else:')
        return '\n'.join(lines)

