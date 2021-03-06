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

# ---------- 1. Functions for arrays of type int ----------

@micropython.asm_thumb
def int_array_assign_scalar(r0, r1, r2):
    label(LOOP)
    str(r2, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

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
def int_array_abs(r0, r1):
    label(LOOP)
    ldr(r4, [r0, 0])
    cmp(r4, 0)
    it(lt)
    neg(r4, r4)
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
def int_array_mul_scalar(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r0, 0])
    mul(r4, r2)
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
def int_array_copy(r0, r1, r2):
    label(LOOP)
    ldr(r4, [r2, 0])
    str(r4, [r0, 0])
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

@micropython.asm_thumb
def int_array_sum(r0, r1):
    movw(r3, 0)
    label(LOOP)
    ldr(r4, [r0, 0])
    add(r3, r3, r4)
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)
    mov(r0, r3)

@micropython.asm_thumb
def int_array_max(r0, r1):
    ldr(r3, [r0, 0])
    label(LOOP)
    add(r0, 4)
    sub(r1, 1)
    ble(END)
    ldr(r4, [r0, 0])
    cmp(r3, r4)
    bge(LOOP)
    mov(r3, r4)
    b(LOOP)
    label(END)
    mov(r0, r3)

@micropython.asm_thumb
def int_array_min(r0, r1):
    ldr(r3, [r0, 0])
    label(LOOP)
    add(r0, 4)
    sub(r1, 1)
    ble(END)
    ldr(r4, [r0, 0])
    cmp(r3, r4)
    ble(LOOP)
    mov(r3, r4)
    b(LOOP)
    label(END)
    mov(r0, r3)


# --------- 2. Functions for arrays of type float ---------

@micropython.asm_thumb
def float_array_assign_scalar(r0, r1, r2):
    vldr(s0, [r2, 0])
    label(LOOP)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_add_scalar(r0, r1, r2):
    vldr(s1, [r2, 0])
    label(LOOP)
    vldr(s0, [r0, 0])
    vadd(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_sub_scalar(r0, r1, r2):
    vldr(s1, [r2, 0])
    label(LOOP)
    vldr(s0, [r0, 0])
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
def float_array_abs(r0, r1):
    movwt(r3, 0x7FFFFFFF) # mask
    label(LOOP)
    ldr(r2, [r0, 0])
    and_(r2, r3)          # this appears to work
    str(r2, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_mul_scalar(r0, r1, r2):
    vldr(s1, [r2, 0])
    label(LOOP)
    vldr(s0, [r0, 0])
    vmul(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_div_scalar(r0, r1, r2):
    vldr(s1, [r2, 0])
    label(LOOP)
    vldr(s0, [r0, 0])
    vdiv(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_add_array(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vadd(s0, s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_sub_array(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vsub(s0, s0, s1)
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
def float_array_copy(r0, r1, r2):
    label(LOOP)
    vldr(s0, [r2, 0])
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_cmp_array(r0, r1, r2):
    movw(r3, 1)
    vmov(s2, r3)
    vcvt_f32_s32(s2, s2) # 1.0 (True)
    movw(r3, 0)
    vmov(s3, r3)
    vcvt_f32_s32(s3, s3) # 0.0 (False)
    label(LOOP)
    vldr(s0, [r0, 0])
    vldr(s1, [r2, 0])
    vcmp(s0, s1)
    vmrs(APSR_nzcv, FPSCR)
    bne(NOT)
    vstr(s2, [r0, 0])
    b(NEXT)
    label(NOT)
    vstr(s3, [r0, 0])
    label(NEXT)
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

@micropython.asm_thumb
def float_array_sum(r0, r1, r2):
    movw(r3, 0)
    vmov(s0, r3)
    label(LOOP)
    vldr(s1, [r0, 0])
    vadd(s0, s0, s1)
    add(r0, 4)
    sub(r1, 1)
    bgt(LOOP)
    vstr(s0, [r2, 0])

@micropython.asm_thumb
def float_array_max(r0, r1, r2):
    vldr(s0, [r0, 0])
    label(LOOP)
    add(r0, 4)
    sub(r1, 1)
    ble(END)
    vldr(s1, [r0, 0])
    vcmp(s0, s1)
    vmrs(APSR_nzcv, FPSCR)
    bge(LOOP)
    vmov(r3, s1)
    vmov(s0, r3)
    b(LOOP)
    label(END)
    vstr(s0, [r2, 0])

@micropython.asm_thumb
def float_array_min(r0, r1, r2):
    vldr(s0, [r0, 0])
    label(LOOP)
    add(r0, 4)
    sub(r1, 1)
    ble(END)
    vldr(s1, [r0, 0])
    vcmp(s0, s1)
    vmrs(APSR_nzcv, FPSCR)
    ble(LOOP)
    vmov(r3, s1)
    vmov(s0, r3)
    b(LOOP)
    label(END)
    vstr(s0, [r2, 0])


# ---------- 3. Type conversion functions ----------

@micropython.asm_thumb
def int_array_from_float_array(r0, r1, r2):
    label(LOOP)
    vldr(s1, [r2, 0])
    vcvt_s32_f32(s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)

@micropython.asm_thumb
def float_array_from_int_array(r0, r1, r2):
    label(LOOP)
    vldr(s1, [r2, 0])
    vcvt_f32_s32(s0, s1)
    vstr(s0, [r0, 0])
    add(r0, 4)
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP)
