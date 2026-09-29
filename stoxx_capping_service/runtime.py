"""Configuration for the locally hosted gRPC service."""

from __future__ import annotations

import ipaddress
import os
from collections.abc import Mapping
from urllib.parse import urlsplit


BIND_ADDRESS_ENV = "STOXX_CAPPING_BIND_ADDRESS"
DEFAULT_BIND_ADDRESS = "127.0.0.1:50051"


def grpc_bind_address(environ: Mapping[str, str] | None = None) -> str:
    """Return a validated loopback-only host:port for the insecure server."""

    settings = os.environ if environ is None else environ
    address = settings.get(BIND_ADDRESS_ENV, DEFAULT_BIND_ADDRESS).strip()
    try:
        parsed = urlsplit(f"//{address}")
        host = parsed.hostname
        port = parsed.port
    except ValueError as error:
        raise ValueError(f"{BIND_ADDRESS_ENV} must be a loopback host and valid port") from error
    if (
        not host
        or port is None
        or not 1 <= port <= 65535
        or parsed.path
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise ValueError(f"{BIND_ADDRESS_ENV} must be a loopback host and valid port")
    try:
        is_loopback = ipaddress.ip_address(host).is_loopback
    except ValueError:
        is_loopback = host.lower() == "localhost"
    if not is_loopback:
        raise ValueError(f"{BIND_ADDRESS_ENV} must be a loopback host and valid port")
    return address
