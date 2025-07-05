from modernrpc import RpcNamespace

math = RpcNamespace()


@math.register_procedure(name="math.add")
def add(termA, termB):
    """
    Add termA and termB, end return the result

    :param termA: First term
    :param termB: Second term
    :type termA: int, float
    :type termB: int, float
    :return: Sum of the two terms
    :rtype: int, float
    """
    return termA + termB


@math.register_procedure(name="math.divide")
def divide(dividend, divisor):
    """
    Divide the dividend by the divisor

    :param dividend: Number
    :param divisor: Number
    :return: Result of the division
    """
    return dividend / divisor
