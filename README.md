# Stoxx Capping Service

## Local gRPC service

The service implements the pinned `capping.Capping/Cap` protocol. It binds to
`127.0.0.1:50051` by default. Set `STOXX_CAPPING_BIND_ADDRESS` to another
loopback `host:port` when needed, for example `127.0.0.1:50061`. The server
rejects wildcard and non-loopback addresses because this service does not
provide TLS.

From the repository root, start it with:

```sh
PYTHONPATH=.:stoxx_capping_service python -m stoxx_capping_service.capping_server
```

Remote deployments require a TLS-terminating gRPC service or proxy; do not
expose the insecure listener directly.
