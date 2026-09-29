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

## systemd user service

On Linux with systemd user services and `uv`, use Python 3.11 from the
repository root:

```sh
python3.11 deploy/install_user_service.py
```

The installer creates a dedicated virtual environment using the pinned minimal
runtime requirements, writes a hardened user unit, and enables the service on
`127.0.0.1:50051`. It keeps logs and runtime files under the user's XDG state
directory. For review without starting the service, add `--install-only`; then
start it with `systemctl --user enable --now stoxx-capping-service.service`.

The unit is local to the installing user's account and grants no network access
beyond the loopback listener. Remove it with
`systemctl --user disable --now stoxx-capping-service.service`, then delete
`~/.config/systemd/user/stoxx-capping-service.service` and the app's
`stoxx-capping-service` directories under `~/.local/share` and `~/.local/state`.
