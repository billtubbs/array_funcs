import utime
import random

def timed_function(f, *args, **kwargs):
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function Time = {:6.3f}ms'.format(delta/1000))
        return result
    return new_func

def float_array_random(n, min=-1e6, max=1e6):
    return array('f', [random()*(max - min) + min for i in range(n)])