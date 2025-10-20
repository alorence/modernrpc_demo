import json
import random
import typing
import xmlrpc.client
from textwrap import dedent, indent
from types import UnionType

from django import template
from django.template import RequestContext

from modernrpc.core import ProcedureWrapper

register = template.Library()


def _get_random_value(_type: type):
    if _type is None:
        return None
    if _type is int:
        return random.randint(0, 1000)
    if _type is float:
        return random.randint(0, 1_000_000) / 1_000
    if _type is str:
        return "abcde"
    if isinstance(_type, UnionType):
        return _get_random_value(random.choice(typing.get_args(_type)))

    return "undefined"


def _build_procedure_params(procedure: ProcedureWrapper):
    if not procedure.arguments:
        return []

    return [
        _get_random_value(arg_doc.type_hint) for arg_doc in procedure.arguments.values()
    ]


@register.simple_tag(takes_context=True)
def xml_rpc_example(context: RequestContext, procedure: ProcedureWrapper):
    server_url = context.request.build_absolute_uri("/rpc")
    params = xmlrpc.client.dumps(tuple(_build_procedure_params(procedure))).lstrip()
    example = f"""
        curl -X POST '{server_url}' \\
          --header 'Content-Type: application/xml' \\
          --data '<?xml version="1.0"?>
            <methodCall>
              <methodName>{procedure.name}</methodName>
              {indent(params, " " * 14).lstrip()}
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
