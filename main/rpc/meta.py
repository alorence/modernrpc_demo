from modernrpc import RpcNamespace, RpcRequestContext

meta = RpcNamespace()


@meta.register_procedure(name="util.printContentType", context_target="_ctx")
def content_type_printer(_ctx: RpcRequestContext):
    """
    Inspect request to extract the Content-Type heaser if present.
    This method demonstrate how a RPC method can access the request object.
    :return: The Content-Type string for incoming request
    """
    # The other available variables are:
    # protocol = kwargs.get(MODERNRPC_PROTOCOL_PARAM_NAME)
    # entry_point = kwargs.get(MODERNRPC_ENTRY_POINT_PARAM_NAME)

    # Get the current request
    request = _ctx.request
    # Return the content-type of the current request
    return request.META.get("Content-Type", "")
