from __future__ import annotations

import asyncio
from typing import Any, Iterable

import httpx
from modernrpc import RpcNamespace


http = RpcNamespace()


@http.register_procedure(name="sleep")
async def sleep(seconds: float) -> float:
    """
    Await for the given number of seconds, then return the same value.

    This demonstrates a minimal async RPC procedure that awaits an IO-bound task.

    :param seconds: Number of seconds to await (fractions allowed)
    :return: The number of seconds actually awaited
    """
    if seconds < 0:
        raise ValueError("seconds must be >= 0")
    await asyncio.sleep(seconds)
    return float(seconds)


async def _fetch_text(client: httpx.AsyncClient, url: str, timeout: float | None) -> dict[str, Any]:
    resp = await client.get(url, timeout=timeout)
    # Limit content to a reasonable size to avoid huge payloads over RPC
    text = resp.text
    if len(text) > 50_000:
        text = text[:50_000] + "…"
    return {
        "url": str(resp.request.url),
        "status": resp.status_code,
        "headers": dict(resp.headers),
        "text": text,
    }


@http.register_procedure(name="get_text")
async def get_text(url: str, timeout: float | None = 10.0) -> dict[str, Any]:
    """
    Perform an async HTTP GET request and return response metadata and text body.

    :param url: The URL to fetch
    :param timeout: Request timeout in seconds (None = no timeout)
    :return: A dict containing ``url``, ``status``, ``headers``, and ``text``
    :raises httpx.HTTPError: On network or protocol errors
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        return await _fetch_text(client, url, timeout)


@http.register_procedure(name="get_json")
async def get_json(url: str, timeout: float | None = 10.0) -> dict[str, Any]:
    """
    Perform an async HTTP GET request and parse JSON body.

    :param url: The URL to fetch
    :param timeout: Request timeout in seconds (None = no timeout)
    :return: A dict containing ``url``, ``status``, ``headers``, and parsed ``json`` data
    :raises httpx.HTTPError: On network or protocol errors
    :raises ValueError: If the response body is not valid JSON
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, timeout=timeout)
        data = resp.json()  # May raise ValueError if not valid JSON
        return {
            "url": str(resp.request.url),
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "json": data,
        }


@http.register_procedure(name="fetch_many")
async def fetch_many(
    urls: Iterable[str],
    timeout: float | None = 10.0,
    max_concurrency: int = 5,
) -> list[dict[str, Any]]:
    """
    Fetch many URLs concurrently with a concurrency limit.

    This demonstrates awaiting multiple async tasks via ``asyncio.Semaphore`` and ``asyncio.gather``.

    :param urls: An iterable of URLs to fetch
    :param timeout: Request timeout per request (seconds)
    :param max_concurrency: Max number of concurrent requests
    :return: A list of response dicts in the same order as input URLs
    """
    if max_concurrency < 1:
        raise ValueError("max_concurrency must be >= 1")

    sem = asyncio.Semaphore(max_concurrency)

    async def bound_fetch(u: str, aclient: httpx.AsyncClient) -> dict[str, Any]:
        async with sem:
            try:
                return await _fetch_text(aclient, u, timeout)
            except httpx.HTTPError as e:
                # Return a structured error instead of failing the whole batch
                return {
                    "url": u,
                    "error": type(e).__name__,
                    "message": str(e),
                }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [bound_fetch(u, client) for u in urls]
        results = await asyncio.gather(*tasks)
        return list(results)
