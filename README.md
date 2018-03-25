# Some Functions for Doing Array Computations in MicroPython

This is a collection of [MicroPython](http://docs.micropython.org/en/v1.9.2/pyboard/index.html) functions written in the 
online assembly language for use with arrays to allow fast 
(vectorized) numeric computations.

They are for use with arrays in MicroPython (Python 3)
to allow basic vectorized linear algebra computations (add, 
subtract, multiply, divide, negative, squared, square-root).

The methods were implemented using MicroPython's inline
assembler as per the examples in the [online documentation](https://docs.micropython.org/en/latest/pyboard/reference/asm_thumb2_hints_tips.html).

The purpose of writing these methods was to allow vectorization 
of calculations on the PyBoard using arrays (there is currently
no numpy ndarray for micropython as far as I know). 

NOTE: Currently only 1-dimensional arrays (vectors) are supported.
Only identically-sized arrays can be added, subtracted, multiplied 
or divided (no broadcasting) and operations are carried out 
'element-wise'.

WARNING: None of these functions have been thoroughly tested. I
cannot guarantee what happens when issues such as floating-point
overflow/underflow happen or when different array types such as
unsigned ints are used.  These are very basic functions with no
exception handling.  Although I have noticed that 'nan' and 'inf'
values are produced in some situations (e.g. sqrt(-1)).

With more work, these functions could be used to create a new 
array class (potentially multi-dimensional) for matrix or ndarray 
calculations and potentially other linear-algebra operations...

### 1. Functions for arrays of type int

| Function Name                            | Purpose         |
| ---------------------------------------- | --------------- |
| `int_array_assign_scalar(a, len(a), i)`  | `a[:] = i`      |
| `int_array_add_scalar(a, len(a), i)`     | `a = a + i`     |
| `int_array_sub_scalar(a, len(a), i)`     | `a = a - i`     |
| `int_array_div_scalar(a, len(a), i)`     | `a = a//i`      |
| `int_array_mul_scalar(a, len(a), i)`     | `a = a*i`       |
| `int_array_add_array(a, len(a), b)`      | `a = a + b`     |
| `int_array_sub_array(a, len(a), b)`      | `a = a - b`     |
| `int_array_cmp_array(a, len(a), b)`      | `a = a==b`      |
| `int_array_div_array(a, len(a), b)`      | `a = a//b`      |
| `int_array_mul_array(a, len(a), b)`      | `a = a*b`       |
| `int_array_neg(a, len(a))`               | `a = -a`        |
| `int_array_square(a, len(a))`            | `a = a*a`       |

Example usage:
``` Python
>>> import array_funcs
>>> from array import array
>>> numbers = array('i', [-1, 0, 1, 1000])
>>> array_funcs.int_array_add_scalar(numbers, len(numbers), 1)
536894992
>>> numbers
array('i', [0, 1, 2, 1001])
```

### 2. Functions for arrays of type float

| Function Name                             | Purpose         |
| ----------------------------------------- | --------------- |
| `float_array_assign_scalar(x, len(x), z)` | `x[:] = z`      |
| `float_array_add_scalar(x, len(x), z)`    | `x = x + z`     |
| `float_array_sub_scalar(x, len(x), z)`    | `x = x - z`     |
| `float_array_div_scalar(x, len(x), z)`    | `x = x/z`       |
| `float_array_mul_scalar(x, len(x), z)`    | `x = x*z`       |
| `float_array_cmp_array(x, len(x), y)`     | `x = x==y`      |
| `float_array_div_array(x, len(x), y)`     | `x = x/y`       |
| `float_array_mul_array(x, len(x), y)`     | `x = x*y`       |
| `float_array_div_int_array(x, len(x), a)` | `x = x/a`       |
| `float_array_mul_int_array(x, len(x), a)` | `x = x*a`       |
| `float_array_neg(x, len(x))`              | `x = -x`        |
| `float_array_square(x, len(x))`           | `x = x*x`      |
| `float_array_sqrt(x, len(x))`             | `x = sqrt(x)`   |

Example usage:
``` Python
>>> import array_funcs
>>> from array import array
>>> numbers = array('f', [-1.0, 0.0, 1.0, 1000.0])
>>> z = array('f', [0.5])
>>> array_funcs.float_array_add_scalar(numbers, len(numbers), z)
536887584
>>> numbers
array('f', [-0.5, 0.5, 1.5, 1000.5])
```

Run the script `test_array_funcs.py` for a demo of all the functions.


### 3. Function for `x**y`

I do not know how to implement exponents `x**y` so this function 
is still written in Python using `math.pow`.

| Function Name                            | Purpose         |
| ---------------------------------------- | --------------- |
| `float_array_power(x, len(x), z)`        | `x = x**z`      |


## Performance

Someone with more experience in the ARM instruction set might be able 
to improve the code but it is already a big improvement (170 
times faster in this quick test) compared to using python loops.

```
>>> import array_funcs as af
>>> from array import array
>>> import utime
>>> def timed_function(f, *args, **kwargs):
...     def new_func(*args, **kwargs):
...         t = utime.ticks_us()
...         result = f(*args, **kwargs)
...         delta = utime.ticks_diff(utime.ticks_us(), t)
...         print('Function Time = {:6.3f}ms'.format(delta/1000))
...         return result
...     return new_func
...
...
...
>>> timed_float_array_square = timed_function(af.float_array_square)
>>> def square(x):
...     for i in range(len(x)):
...         x[i] = x[i]*x[i]
...
...
...
>>> timed_square = timed_function(square)
>>> x = array('f', [pyb.rng() for i in range(1000)])
>>> x[0:5]
array('f', [4.933268e+08, 1.984057e+08, 7.491254e+08, 1.004226e+09, 4.843609e+08])
>>> timed_square(x)
Function Time = 19.378ms
>>> x = array('f', [pyb.rng() for i in range(1000)])
>>> timed_float_array_square(x, len(x))
Function Time =  0.113ms
536908608
>>> 19.378/0.113
171.4867
```
