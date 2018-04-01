from exp_funcs import *
from timers import *
from array import array
import math
from urandom import random


print("\nTesting function: float_array_exp(x, z)")

def num_exp(x, n=12):
    f = 1.0
    for i in range(n, 0, -1):
        f = 1.0 + x * f / i
    return f

def math_float_array_exp(x):
    """Returns an array of math.exp(xi) values for each
    xi in x."""
    return array('f', [math.exp(xi) for xi in x])

@micropython.asm_thumb
def f2i(r0):
    vldr(s0, [r0, 0])
    vmov(r0, s0)

@micropython.asm_thumb
def i2f(r0, r1):
    vmov(s0, r0)
    vstr(s0, [r1, 0])

x = array('f', [(float(i) + random() - 0.5) for i in range(-30, 31)])
z = array('f', [0.0]*len(x))

n = float_array_exp(x, len(x), z)

cum_error = 0.0
for xi, zi in zip(x, z):
    zi_m = math.exp(xi)
    e = abs(zi - zi_m)
    data = xi, zi, zi_m, e, e/zi_m
    print(data)
    cum_error += e/zi_m

print("\nAverage % error compared to math.exp:"
      " {}".format(cum_error*100/len(x)))

n = 1000
print("\nPerformance on array of length: {}".format(n))
timed_float_array_exp = timed_function(float_array_exp)
x = array('f', [(random()*60 - 30) for i in range(n)])
z = array('f', [0.0]*len(x))
timed_float_array_exp(x, len(x), z)

timed_math_float_array_exp = timed_function(math_float_array_exp)
print("\nPerformance of math_float_array_exp(x):")
timed_math_float_array_exp(x)