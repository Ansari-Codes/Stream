# Stream
# Each statement starts from a keyword
# If not starting from a keyword or a symbol, surely, one and only one case exists, which is varaible assignement.
# Uses symbols and keywords
# Uses indentation
# Focuses fast code writing
# ##########################
# ######### Syntax #########
# ##########################
# 1. Variables
#   name = value
# 2. Constants
#   !name = value
# 3. Functions
#   $name[params=values ...]:
#       body...
#       -> output
#   and call it in this way:
#   name(...)
# 4. Conditions
#   condition? 
#      body else ...
#   :condition?
#      body elif ...
#   :?
#      body else ...
# 5. Loops
#   Indeterminate loop
#   >> condition:
#       body ...
#   Determinate loop
#   => i in iterable:
#       body ...
#   Break = break
#   Continue = skip
# 6. Single line (anonymous function)
#   func = [a]->a^2
# 7. Single conditions:
#   (condition) ? (expr) : (expr)
#   Or more long but single line
#   (condition) ? (expr) : (condition2) ? (expr) : ...
# 8. Module import
#   > module
#   aliases making
#   > module = alias
#   importing something specific
#   > math: sin, cosine
# 9. Match
#   match var:
#       case1: (expr)
#       case2: (expr)
#       : (else expr)
# 10. Strings
#   dynamic strings:
#   Strings are enclosed in double quotes only, they can be multiline, or single line.
#   Dynamics can be done via:
#   "{code}"
#   To disable that, just put
#   "\{regular string\}"
# 11. Data Types
#   Only number for both int and float, which is long float actually.
#   Strings are described above.
#   Booleans: true, false
#   Lists: [..,..,...]
#   Dicts: {..:..,..:..,..:..,...}
#   Sets:  {..,..,...}
#   Tuples, no! If you define lists in constant, then you got what you need!
# 12. Try-Catch
#   try code will be warped inside ~>[]
#   this way:
#   ~> [
#       try body... (no indent required)
#   ] e [
#       except body... (no indent required)
#   ]:[
#       finally body... (no indent required)
#   ]
#   Example scripts

'''
// Fact
# This is also a comment
/*
    Mutliline
*/
$fact[n]:
    (n == 0 || n == 1) ? -> 1
    result = 1
    => i :> 1..n:
        result = result * i
    -> result

// Fibonacci sequence generator
$fib[n]:
    (n == 0) ? -> 0
    : (n == 1) ? -> 1
    -> fib(n-1) + fib(n-2)

print("fib(10) = {fib(10)}")

// Sum of numbers 1..100

$sum_to[n]:
    result = 0
    => i in 1..n:
        result = result + i
    -> result

print("sum(1..100) = {sum_to(100)}")


// Mathcing

grade = "B"
match grade:
    "A": print("Excellent")
    "B": print("Good")
    "C": print("Average")
    : print("Fail")


// Dicts
person = {name:"Ansari", age:15, skills:["Python","Physics","Lua"]}

print("Name: {person.name}, Age: {person.age}")
print("Skills: {person.skills}")

// try-catch
result = ~>[10/0]e["error"]
# or
result = 0
~>[
    result = 10/0
] e [
    result = "error"
]:[
    print("Operation successfull!")
]
print("Result = {result}")

square = [x] -> x^2
nums = [1,2,3,4,5]
# list comprehension
squares = [square(n) => n in nums]
print("Squares: {squares}")

> math = m

print("sin(0.5) = {m.sin(0.5)}")
print("cos(0.5) = {m.cos(0.5)}")


'''
