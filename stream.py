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

# Test 1: Basic string interpolation
test1_code = """
name = "Alice"
age = 30
message = "Hello, {name}! You are {age} years old."
"""
test1_expected = "___stream_message = Hello, Alice! You are 30 years old.\n"
run_test("Basic String Interpolation", test1_code, variables_to_print=['message'], expected_output=test1_expected)

# Test 2: Complex mathematical expressions
test2_code = """
a = 10
b = 5
c = a + b * 2 - 3 / 1
d = (a + b) * (a - b)
e = a ^ 2 + b ^ 2
f = a % b
"""
test2_expected = "___stream_a = 10\n___stream_b = 5\n___stream_c = 17.0\n___stream_d = 75\n___stream_e = 125\n___stream_f = 0\n"
run_test("Complex Mathematical Expressions", test2_code, variables_to_print=['a', 'b', 'c', 'd', 'e', 'f'], expected_output=test2_expected)

# Test 3: Nested conditionals with string interpolation
test3_code = """
x = 15
y = 8
(x > 10)?
    (y > 5)?
        result = "Both x and y are greater than thresholds: x={x}, y={y}"
    :?
        result = "x is greater than 10 but y is not: x={x}, y={y}"
:?
    result = "x is not greater than 10: x={x}, y={y}"
"""
test3_expected = "___stream_result = Both x and y are greater than thresholds: x=15, y=8\n"
run_test("Nested Conditionals with Interpolation", test3_code, variables_to_print=['result'], expected_output=test3_expected)

# Test 4: Boolean operations
test4_code = """
a = true
b = false
c = true
result1 = a && b
result2 = a || b
result3 = !b
result4 = (a || b) && c
"""
test4_expected = "___stream_a = True\n___stream_b = False\n___stream_c = True\n___stream_result1 = False\n___stream_result2 = True\n___stream_result3 = True\n___stream_result4 = True\n"
run_test("Boolean Operations", test4_code, variables_to_print=['a', 'b', 'c', 'result1', 'result2', 'result3', 'result4'], expected_output=test4_expected)

# Test 5: String interpolation with escape sequences
test5_code = """
msg = "This is a newline: \\nAnd this is a tab: \\tAnd this is a quote: \\\"And braces: \\{ and \\}"
"""
test5_expected = "___stream_msg = This is a newline: \nAnd this is a tab: \tAnd this is a quote: \"And braces: { and }\n"
run_test("String Interpolation with Escape Sequences", test5_code, variables_to_print=['msg'], expected_output=test5_expected)

# Test 6: Complex nested conditionals
test6_code = """
score = 85
(score >= 90)?
    grade = "A"
    comment = "Excellent work!"
:(score >= 80)?
    grade = "B"
    comment = "Good job!"
:(score >= 70)?
    grade = "C"
    comment = "You passed, but there's room for improvement."
:(score >= 60)?
    grade = "D"
    comment = "You need to work harder."
:?
    grade = "F"
    comment = "Failed. Please see me after class."
"""
test6_expected = "___stream_grade = B\n___stream_comment = Good job!\n"
run_test("Complex Nested Conditionals", test6_code, variables_to_print=['grade', 'comment'], expected_output=test6_expected)

# Test 7: Mathematical expressions with operator precedence
test7_code = """
result1 = 2 + 3 * 4
result2 = (2 + 3) * 4
result3 = 10 - 8 / 2
result4 = (10 - 8) / 2
result5 = 5 + 10 * 2 - 8 / 4
"""
test7_expected = "___stream_result1 = 14\n___stream_result2 = 20\n___stream_result3 = 6.0\n___stream_result4 = 1.0\n___stream_result5 = 23.0\n"
run_test("Mathematical Expressions with Operator Precedence", test7_code, variables_to_print=['result1', 'result2', 'result3', 'result4', 'result5'], expected_output=test7_expected)

# Test 8: String interpolation with complex expressions
test8_code = """
a = 10
b = 20
message = "The sum of {a} and {b} is {a+b}, and the product is {a*b}."
"""
test8_expected = "___stream_message = The sum of 10 and 20 is 30, and the product is 200.\n"
run_test("String Interpolation with Complex Expressions", test8_code, variables_to_print=['message'], expected_output=test8_expected)

# Test 9: Variable reassignment
test9_code = """
x = 10
x = x + 5
x = x * 2
"""
test9_expected = "___stream_x = 30\n"
run_test("Variable Reassignment", test9_code, variables_to_print=['x'], expected_output=test9_expected)

# Test 10: Constant immutability (should fail)
test10_code = """
!PI = 3.14159
PI = 3.14  # This should fail
"""
run_test("Constant Immutability", test10_code, should_fail=True)

# Test 11: Complex boolean expressions
test11_code = """
a = 10
b = 20
c = 30
result1 = (a < b) && (b < c)
result2 = (a > b) || (b < c)
result3 = !(a == b) && (c > b)
"""
test11_expected = "___stream_a = 10\n___stream_b = 20\n___stream_c = 30\n___stream_result1 = True\n___stream_result2 = True\n___stream_result3 = True\n"
run_test("Complex Boolean Expressions", test11_code, variables_to_print=['a', 'b', 'c', 'result1', 'result2', 'result3'], expected_output=test11_expected)

# Test 12: String interpolation with nested expressions
test12_code = """
a = 5
b = 10
message = "The result of {a} + {b} is {a+b}, and {a} * {b} is {a*b}. The average is {(a+b)/2}."
"""
test12_expected = "___stream_message = The result of 5 + 10 is 15, and 5 * 10 is 50. The average is 7.5.\n"
run_test("String Interpolation with Nested Expressions", test12_code, variables_to_print=['message'], expected_output=test12_expected)

# Test 13: Multiple nested conditionals
test13_code = """
x = 15
y = 8
z = 12
(x > 10)?
    (y > 5)?
        (z > 10)?
            result = "All conditions met: x={x}, y={y}, z={z}"
        :?
            result = "x and y conditions met, but not z: x={x}, y={y}, z={z}"
    :?
        result = "x condition met, but not y: x={x}, y={y}, z={z}"
:?
    result = "x condition not met: x={x}, y={y}, z={z}"
"""
test13_expected = "___stream_result = All conditions met: x=15, y=8, z=12\n"
run_test("Multiple Nested Conditionals", test13_code, variables_to_print=['result'], expected_output=test13_expected)

# Test 14: Mathematical operations with various operators
test14_code = """
a = 10
b = 3
add = a + b
sub = a - b
mul = a * b
div = a / b
mod = a % b
pow = a ^ b
"""
test14_expected = "___stream_a = 10\n___stream_b = 3\n___stream_add = 13\n___stream_sub = 7\n___stream_mul = 30\n___stream_div = 3.3333333333333335\n___stream_mod = 1\n___stream_pow = 1000\n"
run_test("Mathematical Operations with Various Operators", test14_code, variables_to_print=['a', 'b', 'add', 'sub', 'mul', 'div', 'mod', 'pow'], expected_output=test14_expected)

# Test 15: String interpolation with boolean expressions
test15_code = """
a = 10
b = 20
message = "Is {a} greater than {b}? {a > b}"
message2 = "Is {a} less than {b}? {a < b}"
"""
test15_expected = "___stream_message = Is 10 greater than 20? False\n___stream_message2 = Is 10 less than 20? True\n"
run_test("String Interpolation with Boolean Expressions", test15_code, variables_to_print=['message', 'message2'], expected_output=test15_expected)

# Test 16: Complex conditional with multiple elif branches
test16_code = """
value = 75
(value >= 90)?
    result = "A"
:(value >= 80)?
    result = "B"
:(value >= 70)?
    result = "C"
:(value >= 60)?
    result = "D"
:?
    result = "F"
"""
test16_expected = "___stream_value = 75\n___stream_result = C\n"
run_test("Complex Conditional with Multiple Elif Branches", test16_code, variables_to_print=['value', 'result'], expected_output=test16_expected)

# Test 17: String interpolation with mathematical functions
test17_code = """
radius = 5
pi = 3.14159
circumference = 2 * pi * radius
area = pi * (radius ^ 2)
"""
test17_expected = "___stream_radius = 5\n___stream_pi = 3.14159\n___stream_circumference = 31.4159\n___stream_area = 78.53975\n"
run_test("String Interpolation with Mathematical Functions", test17_code, variables_to_print=['radius', 'pi', 'circumference', 'area'], expected_output=test17_expected)

# Test 18: Variable shadowing (should work)
test18_code = """
x = 10
(x > 5)?
    x = 20
:?
    x = 30
"""
test18_expected = "___stream_x = 20\n"
run_test("Variable Shadowing", test18_code, variables_to_print=['x'], expected_output=test18_expected)


# Test 19: String interpolation with escaped braces
test19_code = """
message = "This is a literal brace: {{ and this is an escaped one: {{"
message2 = f"This is an interpolated value: {10} and this is a literal brace: {{"
"""
test19_expected = "___stream_message = This is a literal brace: { and this is an escaped one: {\n___stream_message2 = This is an interpolated value: 10 and this is a literal brace: {\n"
run_test("String Interpolation with Escaped Braces", test19_code, variables_to_print=['message', 'message2'], expected_output=test19_expected)

# Test 20: Complex expression with multiple operators (corrected expected output)
test20_code = """
a = 10
b = 5
c = 2
result = a + b * c - a / b + c ^ 2
"""
test20_expected = "___stream_a = 10\n___stream_b = 5\n___stream_c = 2\n___stream_result = 22.0\n"

run_test("Complex Expression with Multiple Operators", test20_code, variables_to_print=['a', 'b', 'c', 'result'], expected_output=test20_expected)

print(f"\n{Fore.GREEN}{'='*10} All Tests Completed {'='*10}{Style.RESET_ALL}")