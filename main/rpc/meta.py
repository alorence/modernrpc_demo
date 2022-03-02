from modernrpc.core import rpc_method, REQUEST_KEY


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
