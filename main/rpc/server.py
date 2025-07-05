from modernrpc import RpcServer

from .errors import errors
from .math import math
from .meta import meta

server = RpcServer()

server.register_namespace(errors)
server.register_namespace(math)
server.register_namespace(meta)
