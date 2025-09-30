from Streamer import *
from streamExpression import Expression
from streamBlockages import StreamBlockage
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
        converted = gen.convert()
        
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

test_code = """
msg = "How are you are you okay"
"""
expected_code = """___stream_msg = 'How are you \nare you okay?'"""
run_test(
    "String Interpolation", 
    code=test_code,
    expected_output=expected_code, 
    variables_to_print=['msg']
    )