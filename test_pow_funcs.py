from pow_funcs import *
from timers import *
from array import array
from urandom import random
import math

def math_float_array_pow_int(x, n):
    return array('f', [math.pow(xi, n) for xi in x])

x = array('f', [-1.0, -0.5, 0.0, 0.5, 1.0, 10.0])
z = array('f', [0.0]*len(x))
exponents = range(-10, 11)

print("x = {}".format(x))
print("\nFunction: float_array_pow_int(x, len(x), z, i)")
print("for i in range({}, {}):".format(exponents[0], exponents[-1]))

cum_error = 0.0
for i in exponents:
    float_array_pow_int(x, len(x), z, i)
    for zi, zmi in zip(z, math_float_array_pow_int(x, i)):
        if zi != zmi:
            cum_error += abs(zi - zmi)
    print(" {:3d}: {}".format(i, z))

print(cum_error)
print("\nCumulative absolute error compared to math.pow:"
      " {}".format(cum_error))

n, i = 1000, 8
print("\nPerformance on array of length {} with i={}:".format(n, i))
timed_float_array_pow_int = timed_function(float_array_pow_int)
x = array('f', [(random()*60 - 30) for i in range(n)])
z = array('f', [0.0]*len(x))
timed_float_array_pow_int(x, len(x), z, i)
