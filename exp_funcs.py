
@micropython.asm_thumb
def float_array_exp(r0, r1, r2):
  # Calculates y = exp(x) where x, y are arrays
  # r0: address of y (output array)
  # r1: length of both arrays
  # r2: address of x (input array)

  # Iterate over elements of x
    label(LOOP1)
    vldr(s0, [r2, 0])      # s0 = x
    push({r0, r1, r2})

  # Calculate s1 = exp(s0)
    label(EXP)
    # Method (Taylor series expansion):
    # f = 1.0
    # a, b = 2.8, 8.0      # optimized for 32-bit floats
    # n = int(a*x + b)
    # for i in range(n, 0, -1):
    #    f = 1.0 + x*f/i
    # return f

    # If x is negative, set x = -x
    mov(r2, 0)             # negative flag
    vmov(s1, r2)
    vcvt_f32_s32(s1, s1)   # s1 = 0.0
    vmov(r0, s0)
    cmp(r0, 0)
    itt(lt)                # If x < 0:
    mov(r2, 1)             #   r2 = 1
    vsub(s0, s1, s0)       #   x = -x

    # Calculate n
    movwt(r1, 0x40333333)
    vmov(s2, r1)           # s2 = a = 2.8
    movwt(r1, 0x41000000)
    vmov(s1, r1)           # s1 = b = 8.0
    vmul(s2, s2, s0)
    vadd(s2, s2, s1)       # s2 = s2*x + s1
    vcvt_s32_f32(s2, s2)
    vmov(r0, s2)           # r0 = n = int(s2)

    # Initialize variables
    mov(r1, 1)
    vmov(s1, r1)
    vcvt_f32_s32(s1, s1)   # s1 = f = 1.0
    vmov(s2, r1)
    vcvt_f32_s32(s2, s2)   # s2 = 1.0
    vmov(s3, r0)
    vcvt_f32_s32(s3, s3)   # s3 = float(n)

    # for i in range(n, 0, -1):
    label(LOOP2)
    vmul(s1, s1, s0)       # f = 1.0 + x*f/i
    vdiv(s1, s1, s3)
    vadd(s1, s1, s2)
    vsub(s3, s3, s2)
    sub(r0, 1)
    bgt(LOOP2)

    # If x was negative, calculate y = 1.0/exp(x)
    cmp(r2, 0)
    beq(end)
    vmov(s2, r2)           # If negative flag == 1
    vcvt_f32_s32(s2, s2)   # s2 = 1.0
    vdiv(s1, s2, s1)       # x = s2/x
    label(end)             # ! EXP complete

  # Save result and increment iterators
    pop({r0, r1, r2})
    vstr(s1, [r0, 0])      # Save s1 in address r0
    add(r0, 4)             # Increment r0, r1, r2
    add(r2, 4)
    sub(r1, 1)
    bgt(LOOP1)             # Loop to next array element
