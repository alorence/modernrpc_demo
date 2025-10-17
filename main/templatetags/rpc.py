import json
import random
import xmlrpc.client
from textwrap import dedent, indent

from django import template
from django.template import RequestContext

from modernrpc.core import ProcedureWrapper

register = template.Library()


def _build_procedure_params(procedure: ProcedureWrapper):
    if not procedure.args_doc:
        return []

    return []

    # FIXME: need better introspection result to build params
    # args = []
    # for _type, _ in procedure.args_doc:
    #     if _type == "int":
    #         args.append(random.randint(0, 1000))
    #     elif _type == "float":
    #         args.append(random.randint(0, 1_000_000) / 1_000)
    #     else:
    #         args.append("undefined")
    # return args


@register.simple_tag(takes_context=True)
def xml_rpc_example(context: RequestContext, procedure: ProcedureWrapper):
    server_url = context.request.build_absolute_uri("/rpc")
    params = xmlrpc.client.dumps(tuple(_build_procedure_params(procedure)))
    example = f"""
        curl -X POST '{server_url}' \\
          --header 'Content-Type: application/xml' \\
          --data '<?xml version="1.0"?>
            <methodCall>
              <methodName>{procedure.name}</methodName>
              {params}
            </methodCall>'
    """
    return dedent(example).lstrip()


@register.simple_tag(takes_context=True)
def json_rpc_example(context: RequestContext, procedure: ProcedureWrapper):
    server_url = context.request.build_absolute_uri("/rpc")
    payload = {
        "jsonrpc": "2.0",
        "id": random.randint(1, 10000),
        "method": procedure.name,
        "params": _build_procedure_params(procedure),
    }
    dumped_payload = json.dumps(payload, indent=2)
    serialized_payload = indent(dumped_payload, " " * 16).lstrip()
    example = f"""
        curl -X POST '{server_url}' \\
            --header 'Content-Type: application/json' \\
            --data '{serialized_payload}'
    """
    return dedent(example).lstrip()
