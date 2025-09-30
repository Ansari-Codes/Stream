from Streamer import *
from colorama import init, Fore, Style
import sys

init(autoreset=True)

def run_test(test_name, code, variables_to_print=None, expected_output=None, should_fail=False):
    print(f"\n{Fore.YELLOW}{'='*10} Testing: {test_name} {'='*10}{Style.RESET_ALL}")
    
    try:
        parser = Parser(';\n' + code)
        ast = Converter(parser.filterStringAndComments()).toAst()
        
        # Print AST
        print(f"{Fore.GREEN}|{'-'*10}< AST >{'-'*10}|{Style.RESET_ALL}")
        width = len(str(len(ast)))
        for j, node in enumerate(ast):
            line_number = str(j + 1).rjust(width)
            print(f" {line_number} {node!r}")

        # Generate Python
        print(f"\n{Fore.GREEN}|{'-'*10}< PYTHON >{'-'*10}|{Style.RESET_ALL}")
        gen = Generator(ast)
        converted = "from baseLib import *" + ";\n" + gen.convert()
        
        # Add print statements for variables after conversion
        if variables_to_print:
            converted += "\n\n# Print variables for testing\n"
            for var in variables_to_print:
                converted += f"print('___stream_{var} =', ___stream_{var})\n"
        
        width = len(str(len(converted.splitlines())))
        for j, node in enumerate(converted.splitlines()):
            line_number = str(j + 1).rjust(width)
            print(f" {line_number} {node!r}")

        # Execute and capture output
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            exec(converted)
            output = captured_output.getvalue()
            sys.stdout = old_stdout
            
            if should_fail:
                print(f"{Fore.RED}Test FAILED: Expected to fail but succeeded{Style.RESET_ALL}")
                return False
            else:
                print(f"\n{Fore.GREEN}Output:{Style.RESET_ALL}")
                print(output)
                
                if expected_output is not None:
                    if output.strip() == expected_output.strip():
                        print(f"{Fore.GREEN}Test PASSED: Output matches expected result{Style.RESET_ALL}")
                        return True
                    else:
                        print(f"{Fore.RED}Test FAILED: Output doesn't match expected result{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}Expected:{Style.RESET_ALL}\n{expected_output}")
                        return False
                else:
                    print(f"{Fore.GREEN}Test PASSED: Code executed without errors{Style.RESET_ALL}")
                    return True
        except Exception as e:
            sys.stdout = old_stdout
            if should_fail:
                print(f"{Fore.GREEN}Test PASSED: Failed as expected with error: {e}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}Test FAILED: Execution error: {e}{Style.RESET_ALL}")
                return False
    except Exception as e:
        if should_fail:
            print(f"{Fore.GREEN}Test PASSED: Failed as expected with error: {e}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}Test FAILED: Parsing error: {e}{Style.RESET_ALL}")
            return False

tough_tests = [
    {
        "name": "String Repetition with Escapes",
        "code": """
x = 3
y = "Hello\nWorld" * x
z = "\tStart " + y + " End"
""",
        "variables_to_print": ['x', 'y', 'z'],
        "expected_output": None
    },
    {
        "name": "Number Arithmetic and Bool Comparisons",
        "code": r"""
a = 5
b = 2
c = (a + b) * (a - b)
is_c_gt_10 = c > 10
""",
        "variables_to_print": ['a', 'b', 'c', 'is_c_gt_10'],
        "expected_output": None
    },
    {
        "name": "Nested Expressions with Strings and Numbers",
        "code": r"""
n = 4
s = "X"
result = (s * n) + "-" + String(n*2)
""",
        "variables_to_print": ['n', 's', 'result'],
        "expected_output": None
    },
    {
        "name": "Escaped Backslashes in Path Strings",
        "code": r"""
path = "C:\\Users\\Test" + "\\Documents"
""",
        "variables_to_print": ['path'],
        "expected_output": None
    },
    {
        "name": "Mixed Operations",
        "code": r"""
num = 5
txt = "A"
combined = txt * num + String(num*2) + "!"
check = num > 3
""",
        "variables_to_print": ['num', 'txt', 'combined', 'check'],
        "expected_output": None
    },
]

# Run all tough tests
for i,test in enumerate(tough_tests):
    run_test(
        str(i+1) + '. ' + test['name'],
        code=test['code'],
        variables_to_print=test.get('variables_to_print'),
        expected_output=test.get('expected_output')
    )
