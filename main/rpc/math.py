from modernrpc import RpcNamespace

math = RpcNamespace()


@math.register_procedure(name="math.add")
def add(term_a, term_b):
    """
    Add termA and termB, end return the result

    :param term_a: First term
    :param term_b: Second term
    :type term_a: int, float
    :type term_b: int, float
    :return: Sum of the two terms
    :rtype: int, float
    """
    return term_a + term_b


@math.register_procedure(name="math.divide")
def divide(dividend, divisor):
    """
    Divide the dividend by the divisor

    :param dividend: Number
    :param divisor: Number
    :return: Result of the division
    """
    return dividend / divisor
