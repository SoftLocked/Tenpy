import operator

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '%' : operator.mod,
        '^' : operator.xor,
        }[op]