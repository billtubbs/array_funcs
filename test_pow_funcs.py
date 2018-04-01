from pow_funcs import *
from timers import *
from array import array
from urandom import random
import math

def math_float_array_pow_int(x, n):
    return array('f', [math.pow(xi, n) for xi in x])

def float_array_random(n, min=-1e6, max=1e6):
    return array('f', [random()*(max - min) + min for i in range(n)])

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

n = 1000
i0, i1 = -8, 9
x = array('f', [random() - 0.5 for i in range(n)])
z = array('f', [0]*n)
print("\nPerformance on array of length {} for i in range({}, {})"
      ":".format(n, i0, i1))

results = {}
for i in range(i0, i1):
    times = []
    for j in range(5):
        t = utime.ticks_us()
        #r = float_array_pow_int(x, len(x), z, i)
        r = math_float_array_pow_int(x, i)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        times.append(delta/1000)
    avg_time = sum(times)/len(times)
    sum_value = sum(r)
    results[i] = avg_time, sum_value
    print("{}: {}ms, {}".format(i, avg_time, sum_value))

