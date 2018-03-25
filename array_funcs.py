'''
Additional functions for use with arrays in MicroPython to
allow basic, fast linear algebra computations.

The methods were implemented using MicroPython's inline
assembler as per the examples in the online documentation.

The purpose of these methods is to allow vectorization of
calculations using arrays. With more work, these methods could
be used to create a new array object (potentially multi-
dimensional) for matrix or ndarray operations...


1. Functions for arrays of type int

Example usage:
>>> import array_funcs
>>> from array import array
>>> numbers = array('i', [-1, 0, 1, 1000])
>>> array_funcs.int_array_add_scalar(numbers, len(numbers), 1)
536894992
>>> numbers
array('i', [0, 1, 2, 1001])


2. Functions for arrays of type float

Example usage:
>>> import array_funcs
>>> from array import array
>>> numbers = array('f', [-1.0, 0.0, 1.0, 1000.0])
>>> a = array('f', [0.5])
>>> array_funcs.float_array_add_scalar(numbers, len(numbers), a)
536887584
>>> numbers
array('f', [-0.5, 0.5, 1.5, 1000.5])
'''

from array import array
from uctypes import addressof
import math

'''
1. Functions for arrays of type int
'''

@micropython.asm_thumb
def int_array_add_scalar(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    add(r4, r4, r2)
    str(r4, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_sub_scalar(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    sub(r4, r4, r2)
    str(r4, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_neg(r0, r1):
    label(LOOP)
    ldr(r4, [r0, 0])
    neg(r4, r4)
    str(r4, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_mul_scalar(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    mul(r4, r2)
    str(r4, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_div_scalar(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    sdiv(r4, r4, r2)
    str(r4, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_add_array(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    ldr(r5, [r2, 0])
    add(r4, r4, r5)
    str(r4, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_sub_array(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    ldr(r5, [r2, 0])
    sub(r4, r4, r5)
    str(r4, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_mul_array(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    ldr(r5, [r2, 0])
    mul(r4, r5)
    str(r4, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_div_array(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    ldr(r5, [r2, 0])
    sdiv(r4, r4, r5)
    str(r4, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_cmp_array(r0, r1, r2):
    label(LOOP)
    ldr(r3, [r0, 0])
    ldr(r4, [r2, 0])
    cmp(r3, r4)
    bne(NOT)
    movw(r3, 1)
    b(NEXT)
    label(NOT)
    movw(r3, 0)
    label(NEXT)
    str(r3, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def int_array_square(r0, r1):
    label(LOOP)
    ldr(r2, [r0, 0])
    mul(r2, r2)
    str(r2, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)


'''
2. Functions for arrays of type float
'''

@micropython.asm_thumb
def float_array_add_scalar(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vadd(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_sub_scalar(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vsub(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_neg(r0, r1):
    label(LOOP)
    vldr(s0, [r0, 0])
    vneg(s0, s0)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_mul_scalar(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vmul(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_div_scalar(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vdiv(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_mul_array(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vmul(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_mul_int_array(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vcvt_f32_s32(s1, s1)
    vmul(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_div_array(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vdiv(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_div_int_array(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vcvt_f32_s32(s1, s1)
    vdiv(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_cmp_array(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vcmp(s0, s1)
    vmrs(APSR_nzcv, FPSCR)
    bne(NOT)
    movw(r3, 1)
    vmov(s0, r3)
    b(NEXT)
    label(NOT)
    movw(r3, 0)
    vmov(s0, r3)
    label(NEXT)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_square(r0, r1):
    label(LOOP)
    vldr(s0, [r0, 0])
    vmul(s0, s0, s0)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_sqrt(r0, r1):
    label(LOOP)
    vldr(s0, [r0, 0])
    vsqrt(s0, s0)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

def float_array_power(x, n, y):
    if isinstance(y, array):
        y = y[0]
    for i in range(n):
        x[i] = math.pow(x[i], y)
