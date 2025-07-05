import sentry_sdk

from modernrpc import RpcRequestContext, RpcServer

from .errors import errors
from .math import math
from .meta import meta


def main_error_handler(exc: BaseException, _: RpcRequestContext) -> None:
    sentry_sdk.capture_exception(exc)


server = RpcServer(error_handler=main_error_handler)

server.register_namespace(errors)
server.register_namespace(math)
server.register_namespace(meta)
