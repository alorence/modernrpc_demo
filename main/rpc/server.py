import sentry_sdk

from modernrpc import RpcRequestContext, RpcServer

from main.rpc.errors import errors
from main.rpc.math import math
from main.rpc.meta import meta
from main.rpc.http import http


def main_error_handler(exc: BaseException, _: RpcRequestContext) -> None:
    sentry_sdk.capture_exception(exc)


server = RpcServer(error_handler=main_error_handler)

server.register_namespace(errors, "errors")
server.register_namespace(math, "math")
server.register_namespace(meta, "utils")
server.register_namespace(http, "http")
