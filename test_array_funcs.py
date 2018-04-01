from array import array
import array_funcs as af

def init():
    x = array('f', [-0.1, 0.0, 0.1, 0.2])
    y = array('f', [-1.0, 0.0, 1.0, 2.0])
    a = array('i', [-10, 0, 10, 20])
    b = array('i', [-1, 0, 1, 2])
    i = 2
    z = array('f', [1.5])
    return a, b, x, y, i, z

def array_compare(x, y, tol=0):
    # checks all values the same
    return all([not(abs(x[i] - y[i]) > tol) for i in range(len(x))])

funcs = {
    'int_array+scalar': {
        'int_array_add_scalar': af.int_array_add_scalar,
        'int_array_sub_scalar': af.int_array_sub_scalar,
        'af.int_array_div_scalar': af.int_array_div_scalar,
        'af.int_array_mul_scalar': af.int_array_mul_scalar
    },

    'int_array+array': {
        'int_array_add_array': af.int_array_add_array,
        'int_array_sub_array': af.int_array_sub_array,
        'int_array_cmp_array': af.int_array_cmp_array,
        'int_array_div_array': af.int_array_div_array,
        'int_array_mul_array': af.int_array_mul_array
    },

    'int_array': {
        'int_array_neg': af.int_array_neg,
        'int_array_abs': af.int_array_abs,
        'int_array_square': af.int_array_square
    },

    'int_array->scalar': {
        'int_array_sum': af.int_array_sum,
        'int_array_max': af.int_array_max,
        'int_array_min': af.int_array_min
    },

    'float_array+scalar': {
        'float_array_add_scalar': af.float_array_add_scalar,
        'float_array_sub_scalar': af.float_array_sub_scalar,
        'float_array_div_scalar': af.float_array_div_scalar,
        'float_array_mul_scalar': af.float_array_mul_scalar,
        'float_array_power': af.float_array_power
    },

    'float_array+array': {
        'float_array_add_array': af.float_array_add_array,
        'float_array_sub_array': af.float_array_sub_array,
        'float_array_div_array': af.float_array_div_array,
        'float_array_mul_array': af.float_array_mul_array,
        'float_array_cmp_array': af.float_array_cmp_array
    },

    'float_array+int_array': {
        'float_array_div_int_array': af.float_array_div_int_array,
        'float_array_mul_int_array': af.float_array_mul_int_array
    },

    'float_array': {
        'float_array_neg': af.float_array_neg,
        'float_array_abs': af.float_array_abs,
        'float_array_square': af.float_array_square,
        'float_array_sqrt': af.float_array_sqrt
    },

    'float_array->scalar': {
        'float_array_sum': af.float_array_sum,
        'float_array_max': af.float_array_max,
        'float_array_min': af.float_array_min
    },

    'float_array->int_array': {
        'int_array_from_float_array': af.int_array_from_float_array
    },

    'int_array->float_array': {
        'float_array_from_int_array': af.float_array_from_int_array
    }
}

print("\n-------- Testing Array Functions ----------")

for fname, f in funcs['int_array+scalar'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(a, len(a), i)".format(fname))
    print("a: {}".format(a))
    print("i: {}".format(i))
    f(a, len(a), i)
    print("Result: {}".format(a))

input("\nPress enter to continue")

for fname, f in funcs['int_array+array'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(a, len(a), b)".format(fname))
    print("a: {}".format(a))
    print("b: {}".format(b))
    f(a, len(a), b)
    print("Result: {}".format(a))

input("\nPress enter to continue")

for fname, f in funcs['int_array'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(a, len(a))".format(fname))
    print("a: {}".format(a))
    f(a, len(a))
    print("Result: {}".format(a))

input("\nPress enter to continue")

for fname, f in funcs['int_array->scalar'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(a, len(a))".format(fname))
    print("a: {}".format(a))
    print("Result: {}".format(f(a, len(a))))

input("\nPress enter to continue")

for fname, f in funcs['float_array+scalar'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(x, len(x), z)".format(fname))
    print("x: {}".format(x))
    print("z: {}".format(z))
    f(x, len(x), z)
    print("Result: {}".format(x))

input("\nPress enter to continue")

for fname, f in funcs['float_array+array'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(x, len(x), y)".format(fname))
    print("x: {}".format(x))
    print("y: {}".format(y))
    f(x, len(x), y)
    print("Result: {}".format(x))

input("\nPress enter to continue")

for fname, f in funcs['float_array+int_array'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(x, len(x), a)".format(fname))
    print("x: {}".format(x))
    print("a: {}".format(a))
    f(x, len(x), a)
    print("Result: {}".format(x))

input("\nPress enter to continue")

for fname, f in funcs['float_array'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(x, len(x))".format(fname))
    print("x: {}".format(x))
    f(x, len(x))
    print("Result: {}".format(x))

input("\nPress enter to continue")

for fname, f in funcs['float_array->scalar'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(x, len(x), z)".format(fname))
    print("x: {}".format(x))
    f(x, len(x), z)
    print("Result: {}".format(z))

input("\nPress enter to continue")

for fname, f in funcs['float_array->int_array'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(y, len(y), a)".format(fname))
    print("y: {}".format(y))
    f(y, len(y), a)
    print("Result: {}".format(a))

input("\nPress enter to continue")

for fname, f in funcs['int_array->float_array'].items():
    a, b, x, y, i, z = init()
    print("\nFunction: {}(a, len(a), y)".format(fname))
    print("a: {}".format(a))
    f(a, len(a), y)
    print("Result: {}".format(y))
