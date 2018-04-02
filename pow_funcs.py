@micropython.asm_thumb
def float_array_pow_int(r0, r1, r2, r3):
  # Calculates y = x**n where x is a float and n is an integer
  # r0: address of y (output array)
  # r1: length of both arrays
  # r2: address of x
  # r3: n (an integer)

  # Iterate over elements of x
    label(LOOP1)
    vldr(s0, [r2, 0])      # s0 = x
    push({r0, r1, r2})
    mov(r2, r3)            # r2 = n

  # Calculate s1 = s0**r2
    label(INTPOW)
    cmp(r2, 1)
    bne(NOT1)              # if n == 1:
    vmov(r0, s0)
    vmov(s1, r0)           #   z = x
    b(END)
    label(NOT1)
    mov(r0, 1)             # r0 = 1
    vmov(s1, r0)
    vcvt_f32_s32(s1, s1)   # s1 = 1.0
    cmp(r2, 0)             # if n == 0:
    beq(END)               #   z = 1.0
    bge(LOOP2)             # if n < 0:
    vdiv(s0, s1, s0)       #   x = 1.0/x
    neg(r2, r2)            #   n = -n

    label(LOOP2)           # do:
    and_(r0, r2)
    ite(gt)                #   if n is odd:
    vmul(s1, s1, s0)       #     s1 *= x
    mov(r0, 1)
    vmul(s0, s0, s0)       #   x *= x
    lsr(r2, r0)            #   n >> 1
    cmp(r2, 0)
    bgt(LOOP2)             # while n > 0
    label(END)             # ! INTPOW complete

  # Save result and increment iterators
    pop({r0, r1, r2})
    vstr(s1, [r0, 0])      # Save s1 in address r2
    add(r0, 4)             # Increment r0, r1, r2
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP1)             # Loop to next array element


def float_array_pow_float(x, n, v):
    if isinstance(v, array):
        v = v[0]
    for i in range(n):
        x[i] = math.pow(x[i], v)


