from modernrpc import RpcNamespace
import math as py_math

math = RpcNamespace()


@math.register_procedure(name="add")
def add(*terms: int | float) -> int | float:
    """
    Returns the sum of two or more terms.

    This procedure can be used to test variable number of inputs
    :return: Sum of the two terms
    """
    return sum(terms)


@math.register_procedure(name="subtract")
def subtract(minuend: int | float, *subtrahends: int | float) -> int | float:
    """
    Return the result of subtracting one or more numbers from a first value.

    :param minuend: The initial value from which all following values are subtracted
    :param subtrahends: One or more numbers to subtract from the minuend, in order
    :return: The subtraction result, computed as ``minuend - subtrahends[0] - subtrahends[1] - ...``
    :raises ValueError: If no ``subtrahends`` are provided
    """
    if len(subtrahends) == 0:
        raise ValueError("At least one subtrahend is required")
    result: int | float = minuend
    for s in subtrahends:
        result -= s
    return result


@math.register_procedure(name="multiply")
def multiply(*factors: int | float) -> int | float:
    """
    Return the product of two or more numbers.

    :param factors: Two or more numeric factors to multiply, in order
    :return: The multiplication result, computed as the product of all provided ``factors``
    :raises ValueError: If fewer than two ``factors`` are provided
    """
    if len(factors) < 2:
        raise ValueError("At least two factors are required")
    product: int | float = 1
    for f in factors:
        product *= f
    return product


@math.register_procedure(name="divide")
def divide(dividend: int | float, divisor: int | float) -> int | float:
    """
    Returns the division result of two numbers.

    This procedure can be used to raise an exception. If divisor is set to 0, a ZeroDivisionError will be raised from
    the function and transformed into a proper RPC Error response.
    :param dividend: First term of the division
    :param divisor: Second term of the division
    :return: The result
    """
    return dividend / divisor


@math.register_procedure(name="power")
def power(base: int | float, exponent: int | float) -> int | float:
    """
    Raise a number to a given power.

    This is equivalent to Python's ``base ** exponent``.

    :param base: The base value
    :param exponent: The exponent value (can be integer or float)
    :return: ``base`` raised to the power of ``exponent``
    """
    return base**exponent


@math.register_procedure(name="sqrt")
def sqrt(x: int | float) -> float:
    """
    Return the non-negative square root of ``x``.

    This is a thin wrapper around ``math.sqrt``. If ``x`` is negative, ``math.sqrt`` raises ``ValueError`` which will
    be converted into a proper RPC error by the framework.

    :param x: The value whose square root is requested
    :return: The square root of ``x`` as a floating-point number
    :raises ValueError: If ``x`` is negative
    """
    return py_math.sqrt(x)
