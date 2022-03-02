from fractions import Fraction

from modernrpc.core import rpc_method
from modernrpc.exceptions import RPCException, RPC_CUSTOM_ERROR_BASE


@rpc_method(name="errors.custom")
def custom_error():
    """Simply raises a custom exception"""
    raise RPCException(RPC_CUSTOM_ERROR_BASE + 1, "This is a custom error")


@rpc_method(name="errors.unserializable_result")
def unserializable_result():
    """Return an instance of python builtin Fraction class, which cannot be serialized"""
    return Fraction(150, 8)
