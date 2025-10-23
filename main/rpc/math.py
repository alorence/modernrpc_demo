from modernrpc import RpcNamespace

math = RpcNamespace()


@math.register_procedure(name="math.add")
def add(term_a: int | float, term_b: int | float) -> int | float:
    """
    Returns the sum of two terms.

    This procedure can be used to test different types of inputs. a and b terms can be passed as int or float, the
    result type will depends on the input ones.
    :param term_a: First term
    :param term_b: Second term
    :return: Sum of the two terms
    """
    return term_a + term_b


@math.register_procedure(name="math.divide")
def divide(dividend: int | float, divisor: int | float):
    """
    Returns the division result of two numbers.

    This procedure can be used to raise an exception. If divisor is set to 0, a ZeroDivisionError will be raised from
    the function and transformed into a proper RPC Error response.
    :param dividend: First term of the division
    :param divisor: Second term of the division
    :return: The result
    """
    return dividend / divisor
