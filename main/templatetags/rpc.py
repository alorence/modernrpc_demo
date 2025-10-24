import json
import random
import typing
import xmlrpc.client
from textwrap import dedent, indent
from types import UnionType

from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

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


@register.simple_tag
def xml_rpc_example(procedure: ProcedureWrapper):
    server_url = mark_safe('<span x-text="rpc_url()"></span>')
    params = xmlrpc.client.dumps(tuple(_build_procedure_params(procedure))).rstrip()
    params = indent(params, " " * 8, predicate=lambda line: line != "<params>\n")
    tmpl = escape(
        dedent("""
            curl -X POST '{server_url}' \\
                --header 'Content-Type: application/xml' \\
                --data '<?xml version="1.0"?>
                  <methodCall>
                    <methodName>{procedure}</methodName>
                    {params}
                  </methodCall>'
        """).lstrip()
    )
    return format_html(
        tmpl, server_url=server_url, procedure=procedure.name, params=params
    )


@register.simple_tag
def json_rpc_example(procedure: ProcedureWrapper):
    server_url = mark_safe('<span x-text="rpc_url()"></span>')
    payload = {
        "jsonrpc": "2.0",
        "id": random.randint(1, 10000),
        "method": procedure.name,
        "params": _build_procedure_params(procedure),
    }
    payload = json.dumps(payload, indent=2)
    payload = indent(payload, " " * 4).lstrip()
    tmpl = dedent("""
        curl -X POST '{server_url}' \\
            --header 'Content-Type: application/json' \\
            --data '{payload}'
    """).lstrip()
    return format_html(tmpl, server_url=server_url, payload=payload)
