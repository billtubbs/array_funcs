# Some Functions for Doing Array Computations in MicroPython

This is a collection of [MicroPython](http://docs.micropython.org/en/v1.9.2/pyboard/index.html) (Python 3) functions written in the inline assembly language for use with [arrays](https://docs.micropython.org/en/latest/pyboard/library/array.html) to allow fast (vectorized) numeric computations.

They allow the basic linear algebra computations such as add, subtract, multiply, divide, negative, squared, square-root, sum, max, min and comparison to be carried out on one-dimensional arrays of data much faster than can be achieved with lists, loops or any built-in functions.

The methods were implemented using MicroPython's inline assembler as per the examples in the [online documentation](https://docs.micropython.org/en/latest/pyboard/reference/asm_thumb2_hints_tips.html).

The purpose of writing these methods was to allow small microcomputers such as the PyBoard and [ESP32](https://www.adafruit.com/product/3269) to process data (e.g. from sensors) in real time and potentially do some online analysis or machine intelligence.  There is currently nothing similar to the [numpy ndarray](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html) for MicroPython as far as I know. 

NOTES:
- Currently, only 1-dimensional arrays (vectors) are supported,
- only identically-sized arrays can be added, subtracted, multiplied 
or divided (no broadcasting),
- operations are carried out 'element-wise', and
- only int and float data types are supported.

WARNINGS:
- None of these functions have been thoroughly tested
- I cannot guarantee what happens when issues such as floating-point overflow/underflow happen or when different array types such as unsigned ints are used (although 'nan' and 'inf' values are produced by default in some situations such as sqrt(-1))
- The functions are written in assembler and there is virtually no type checking or exception handling
- If you don't specify the function arguments correctly you can easily overwrite memory and crash your processor.

With more work, these functions could be used to create a new array class (potentially multi-dimensional) for matrix or ndarray calculations and potentially other linear-algebra operations.  See 'Future Work' discussion below.

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
| `int_array_sum(a, len(a))`               | `sum(a)`        |
| `int_array_max(a, len(a))`               | `max(a)`        |
| `int_array_min(a, len(a))`               | `min(a)`        |

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
| `float_array_add_array(x, len(x), y)`     | `x = x + y`     |
| `float_array_sub_array(x, len(x), y)`     | `x = x - y`     |
| `float_array_cmp_array(x, len(x), y)`     | `x = x==y`      |
| `float_array_div_array(x, len(x), y)`     | `x = x/y`       |
| `float_array_mul_array(x, len(x), y)`     | `x = x*y`       |
| `float_array_div_int_array(x, len(x), a)` | `x = x/a`       |
| `float_array_mul_int_array(x, len(x), a)` | `x = x*a`       |
| `float_array_neg(x, len(x))`              | `x = -x`        |
| `float_array_square(x, len(x))`           | `x = x*x`       |
| `float_array_sqrt(x, len(x))`             | `x = sqrt(x)`   |
| `float_array_sum(x, len(x), z)`           | `z = sum(x)`    |
| `float_array_max(x, len(x), z)`           | `z = max(x)`    |
| `float_array_min(x, len(x), z)`           | `z = min(x)`    |

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

I do not know how to implement exponents (`x**y`) so this function 
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

Comparing the array sum functions written in assembler with the 
built-in `sum` function, there is a 15-times speed increase for 
int arrays and almost 60-times speed increase for float arrays.

```
>>> timed_float_array_sum = timed_function(af.float_array_sum)
>>> timed_sum = timed_function(sum)
>>> x = array('f', [pyb.rng() for i in range(1000)])
>>> timed_sum(x)
Function <function> Time =  5.494ms
5.339773e+11
>>> z = array('f', [0])
>>> timed_float_array_sum(x, len(x), z)
Function <function> Time =  0.093ms
536949808
>>> z
array('f', [5.339773e+11])
>>> 5.494/0.093
59.07527
```

The reason for the slow speed of Python arrays is [explained here](https://stackoverflow.com/questions/36778568/why-are-pythons-arrays-slow).

## Possible Future Work

### Create New Array Class

To make this collection of functions more usable, it would make sense to create a new Array class or potentially sub-class the MicroPython array class so that the functions are invoked seamlessly by the math operators.

For example:

``` Python
from array_funcs import Array

a = Array('f', [0.322, -1.141, -0.702, 1.103])
b = Array('f', [5.93, 13.85, -1.97, 8.36])
x = Array('f', [0.0, 1.0, 2.0, 3.0])
y = a*x + b
```

### Other Math Functions

This project was motivated by the need to do fast vectorized calculations on arrays.  However, it is limited by what is easily implementable in assembler language and by memory capacity of most microcontrollers.  It would be nice to develop vectorized versions of some of the more common functions from the [math module](https://docs.micropython.org/en/latest/pyboard/library/math.html) such as sin, cos, tan, ...etc, exp, log, pow, and perhaps random too.  But these functions are written in c so it would probably make more sense to develop this project as a [c module](http://micropython-dev-docs.readthedocs.io/en/latest/adding-module.html) to do this.

### 2-Dimensional Arrays (Matrices)

These would be useful for many applications (e.g. machine learning, control of robots).  [jalawson](https://github.com/jalawson) has already written a versatile matrix manipulation module in Micropython called [ulinalg](https://github.com/jalawson/ulinalg).  However, this was not designed for speed and uses lists not [arrays](https://docs.micropython.org/en/latest/pyboard/library/array.html?highlight=array#module-array).  Converting it to use arrays would be considerable work but would also limit its versatility and robustness (arrays do not support complex or bool types for example).  It might be better to keep a 'high-performance' matrix class in this module and keep the two projects separate.

### Support For Other Data Types

Potentially, double, byte or bool

I welcome people's suggestions on the current state of this project, possible future direction and priorities.
