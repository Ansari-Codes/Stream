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
#   => i :> iterable:
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
#   "{{regular string}}"
# 11. Data Types
#   Only number for both int and float, which is long float actually.
#   Strings are described above.
#   Booleans: true, false
#   Lists: [..,..,...]
#   Dicts: {..:..,..:..,..:..,...}
#   Sets:  {..,..,...}
#   Tuples, no! If you define lists in constant, then you got what you need!
