from fractions import Fraction

from modernrpc import RpcNamespace
from modernrpc.exceptions import RPCException, RPC_CUSTOM_ERROR_BASE

errors = RpcNamespace()

@errors.register_procedure(name="errors.custom")
def custom_error():
    """Simply raises a custom exception"""
    raise RPCException(RPC_CUSTOM_ERROR_BASE + 1, "This is a custom error")


@errors.register_procedure(name="errors.unserializable_result")
def unserializable_result():
    """Return an instance of python builtin Fraction class, which cannot be serialized"""
    return Fraction(150, 8)
