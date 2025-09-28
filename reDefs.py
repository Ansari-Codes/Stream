import re

patterns = {
    'var': r'^(\s*)\b([A-Za-z]\w*)\s*=\s*(.+)',
    'const': r'^(\s*)!\s*\b([A-Za-z]\w*)\s*=\s*(.+)',
    'else': r'^(\s*):\?\s*$',
    'elif': r'^(\s*):\s*(\S.+?)\s*\?\s*$',
    'if': r'^(\s*)([^\?:].*?)\s*\?\s*$'
}

def reg(line):
    for name, pattern in patterns.items():
        m = re.match(pattern, line)
        if m:
            indent = len(m.group(1)) if m.group(1) else 0
            expr = tuple(g.strip() for g in m.groups()[1:]) if len(m.groups()) > 1 else 'else'
            return name, expr, indent
    return "unexpected", None, 0


