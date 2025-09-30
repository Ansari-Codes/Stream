streamTypes = ['boolean', 'number', 'string', 'nil', 'true', 'false']

class boolean(int):
    def __new__(cls, value=1.0):
        val = 1 if bool(value) else 0
        obj = super().__new__(cls, val)
        obj.value = bool(val)
        return obj

    def __init__(self, value=1.0) -> None:
        super().__init__()
        self.value = bool(value)

    def __and__(self, other):
        return boolean(self.value and bool(other))
    
    def __rand__(self, other):
        return boolean(bool(other) and self.value)
    
    def __or__(self, other):
        return boolean(self.value or bool(other))
    
    def __ror__(self, other):
        return boolean(bool(other) or self.value)
    
    def __xor__(self, other):
        return boolean(bool(self.value) ^ bool(other))
    
    def __rxor__(self, other):
        return boolean(bool(other) ^ self.value)
    
    def __invert__(self):
        return boolean(not self.value)
    
    def __bool__(self):
        return self.value
    
    # Representations
    def __repr__(self):
        return "true" if self.value else "false"
    
    def __str__(self):
        return repr(self)

class number(float):
    def __new__(cls, value=0.0):
        return super().__new__(cls, float(value))
    
    def __init__(self, value=0.0):
        self.value = float(value)
    
    def is_int(self):
        return boolean(True) if self.value.is_integer() else boolean(False)
    
    def is_pos(self):
        return boolean(self.value > 0)
    
    def is_zero(self):
        return boolean(self.value == 0)
    
    def to_str(self):
        return string(self.value)
    
    def to_bool(self):
        return boolean(self.value)

    # Arithmetic
    def __add__(self, other):
        return number(self.value + float(getattr(other, 'value', other)))
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        return number(self.value - float(getattr(other, 'value', other)))
    def __rsub__(self, other):
        return number(float(getattr(other, 'value', other)) - self.value)
    def __mul__(self, other):
        if isinstance(other, number):
            return number(self.value * other.value)
        elif isinstance(other, string):
            return string(other.value * int(self.value))
        else:
            return number(self.value * float(getattr(other, 'value', other)))

    def __rmul__(self, other):
        if isinstance(other, string):
            return string(other.value * int(self.value))
        else:
            return self.__mul__(other)
    def __truediv__(self, other):
        return number(self.value / float(getattr(other, 'value', other)))
    def __rtruediv__(self, other):
        return number(float(getattr(other, 'value', other)) / self.value)
    def __floordiv__(self, other):
        return number(self.value // float(getattr(other, 'value', other)))
    def __rfloordiv__(self, other):
        return number(float(getattr(other, 'value', other)) // self.value)
    def __mod__(self, other):
        return number(self.value % float(getattr(other, 'value', other)))
    def __rmod__(self, other):
        return number(float(getattr(other, 'value', other)) % self.value)
    def __pow__(self, other, mod=None):
        return number(self.value ** float(getattr(other, 'value', other)))
    def __rpow__(self, other, mod=None):
        return number(float(getattr(other, 'value', other)) ** self.value)

    # Bitwise
    def __lshift__(self, other):
        return number(int(self.value) << int(getattr(other, 'value', other)))
    def __rshift__(self, other):
        return number(int(self.value) >> int(getattr(other, 'value', other)))
    def __and__(self, other):
        return number(int(self.value) & int(getattr(other, 'value', other)))
    def __or__(self, other):
        return number(int(self.value) | int(getattr(other, 'value', other)))
    def __xor__(self, other):
        return number(int(self.value) ^ int(getattr(other, 'value', other)))
    def __invert__(self):
        return number(~int(self.value))

    # Comparison
    def __eq__(self, other):
        return boolean(True) if self.value == float(getattr(other, 'value', other)) else boolean(False)
    def __ne__(self, other):
        return boolean(True) if self.value != float(getattr(other, 'value', other)) else boolean(False)
    def __gt__(self, other):
        return boolean(True) if self.value > float(getattr(other, 'value', other)) else boolean(False)
    def __lt__(self, other):
        return boolean(True) if self.value < float(getattr(other, 'value', other)) else boolean(False)
    def __ge__(self, other):
        return boolean(True) if self.value >= float(getattr(other, 'value', other)) else boolean(False)
    def __le__(self, other):
        return boolean(True) if self.value <= float(getattr(other, 'value', other)) else boolean(False)

    def __str__(self):
        return f"{self.value}"
    
    def __repr__(self) -> str:
        return f"number({self.value})"

class string(str):
    def __new__(cls, value=''):
        obj = super().__new__(cls, str(value))
        obj.value = str(value)
        return obj

    def __init__(self, value=''):
        self.value = str(value)

    # Concatenation
    def __add__(self, other):
        other_val = getattr(other, 'value', other)
        return string(self.value + str(other_val))

    def __radd__(self, other):
        other_val = getattr(other, 'value', other)
        return string(str(other_val) + self.value)

    # Repetition
    def __mul__(self, other):
        other_val = int(getattr(other, 'value', other))
        return string(self.value * other_val)

    def __rmul__(self, other):
        other_val = int(getattr(other, 'value', other))
        return string(self.value * other_val)

    # Comparisons
    def __eq__(self, other):
        other_val = getattr(other, 'value', other)
        return boolean(self.value == str(other_val))

    def __ne__(self, other):
        other_val = getattr(other, 'value', other)
        return boolean(self.value != str(other_val))

    def __lt__(self, other):
        other_val = getattr(other, 'value', other)
        return boolean(self.value < str(other_val))

    def __le__(self, other):
        other_val = getattr(other, 'value', other)
        return boolean(self.value <= str(other_val))

    def __gt__(self, other):
        other_val = getattr(other, 'value', other)
        return boolean(self.value > str(other_val))

    def __ge__(self, other):
        other_val = getattr(other, 'value', other)
        return boolean(self.value >= str(other_val))

    # Type conversions
    def to_number(self):
        return number(float(self.value)) if self.value else Nil

    def to_bool(self):
        return boolean(bool(self.value))

    # Representations
    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'string("{self.value}")'

class _NilType:
    def __repr__(self):
        return "Nil"
    
    def __bool__(self):
        return False
    
    def __getattr__(self, _):
        return self
    
    def __call__(self, *args, **kwargs):
        return self

Nil = _NilType()
