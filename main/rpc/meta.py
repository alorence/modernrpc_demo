from modernrpc import RpcNamespace, RpcRequestContext

meta = RpcNamespace()


@meta.register_procedure(name="util.printContentType", context_target="_ctx")
def content_type_printer(_ctx: RpcRequestContext):
    """
    Inspect the incoming request and extract the Content-Type header if present.
    This procedure demonstrates how a remote procedure can access the request object.

    :param _ctx: The request context provided by the RPC server.
    :type _ctx: RpcRequestContext
    :return: The Content-Type value for the incoming request, or an empty string if not set.
    :rtype: str
    """
    # Get the current request
    request = _ctx.request
    # Return the content-type of the current request
    return request.headers.get("Content-Type", "")
