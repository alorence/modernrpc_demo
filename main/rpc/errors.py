from fractions import Fraction

from modernrpc import RpcNamespace
from modernrpc.exceptions import RPCException, RPC_CUSTOM_ERROR_BASE

errors = RpcNamespace()


@errors.register_procedure(name="errors.custom")
def custom_error():
    """
    Raise a custom RPC exception.

    :raises RPCException: Always raised with a custom error code and message.
    """
    raise RPCException(RPC_CUSTOM_ERROR_BASE + 1, "This is a custom error")


@errors.register_procedure(name="errors.unserializable_result")
def unserializable_result():
    """
    Return a value that cannot be serialized by the RPC transport.

    Specifically, this procedure returns an instance of Python’s built-in Fraction class,
    which is not JSON-serializable by default.

    :return: An unserializable Fraction instance.
    :rtype: Fraction
    """
    return Fraction(150, 8)
