from modernrpc.core import rpc_method
from modernrpc.core import REQUEST_KEY, ENTRY_POINT_KEY, PROTOCOL_KEY, HANDLER_KEY


@rpc_method(name="math.add")
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


@rpc_method(name="math.divide")
def divide(dividend, divisor):
    """
    Divide the dividend by the divisor

    :param dividend: Number
    :param divisor: Number
    :return: Result of the division
    """
    return dividend / divisor


@rpc_method(name="util.printContentType")
def content_type_printer(**kwargs):
    """
    Inspect request to extract the Content-Type heaser if present.
    This method demonstrate how a RPC method can access the request object.

    :param kwargs: Dict with current request, protocol and entry_point information.
    :return: The Content-Type string for incoming request
    """
    # The other available variables are:
    # protocol = kwargs.get(MODERNRPC_PROTOCOL_PARAM_NAME)
    # entry_point = kwargs.get(MODERNRPC_ENTRY_POINT_PARAM_NAME)

    # Get the current request
    request = kwargs.get(REQUEST_KEY)
    # Return the content-type of the current request
    return request.META.get('Content-Type', '')
