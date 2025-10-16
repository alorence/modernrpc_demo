from modernrpc import RpcNamespace, RpcRequestContext

meta = RpcNamespace()


@meta.register_procedure(name="util.printContentType", context_target="_ctx")
def content_type_printer(_ctx: RpcRequestContext):
    """
    Inspect request to extract the Content-Type header if present.
    This method demonstrate how a remote procedure can access the request object.
    :return: The Content-Type string for incoming request
    """
    # Get the current request
    request = _ctx.request
    # Return the content-type of the current request
    return request.headers.get("Content-Type", "")
