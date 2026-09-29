from __future__ import annotations

import pytest

from stoxx_capping_service.runtime import (
    BIND_ADDRESS_ENV,
    DEFAULT_BIND_ADDRESS,
    grpc_bind_address,
)


def test_default_bind_address_is_loopback():
    assert grpc_bind_address({}) == DEFAULT_BIND_ADDRESS == "127.0.0.1:50051"


@pytest.mark.parametrize("address", ["127.0.0.1:50061", "localhost:50061", "[::1]:50061"])
def test_loopback_bind_address_can_be_configured(address):
    assert grpc_bind_address({BIND_ADDRESS_ENV: address}) == address


@pytest.mark.parametrize(
    "address",
    [
        "[::]:50051", "0.0.0.0:50051", "192.0.2.10:50051",
        "127.0.0.1:0", "127.0.0.1:65536", "127.0.0.1:bad",
    ],
)
def test_non_loopback_or_invalid_bind_address_is_rejected(address):
    with pytest.raises(ValueError, match="STOXX_CAPPING_BIND_ADDRESS"):
        grpc_bind_address({BIND_ADDRESS_ENV: address})
