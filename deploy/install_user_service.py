"""Install and start the loopback-only Stoxx service as a systemd user unit."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


SERVICE_NAME = "stoxx-capping-service.service"
UNIT_TEMPLATE = Path(__file__).parent / "systemd" / f"{SERVICE_NAME}.in"
RUNTIME_REQUIREMENTS = Path(__file__).parent / "runtime-requirements.txt"


def xdg_path(variable: str, default: Path) -> Path:
    value = os.environ.get(variable)
    return Path(value).expanduser() if value else default


def systemd_value(value: Path | str) -> str:
    """Escape a path/value for a systemd unit without adding literal quotes."""

    rendered = str(value)
    if "\n" in rendered or "\r" in rendered:
        raise ValueError("systemd values cannot contain newline characters")
    escaped: list[str] = []
    for character in rendered:
        if character.isspace() or character in {'\\', '"'}:
            escaped.append(f"\\x{ord(character):02x}")
        elif character == "%":
            escaped.append("%%")
        elif character == "$":
            escaped.append("$$")
        else:
            escaped.append(character)
    return "".join(escaped)


def render_unit(source_dir: Path, runtime_dir: Path, python: Path) -> str:
    template = UNIT_TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "@RUNTIME_DIR@": systemd_value(runtime_dir),
        "@SOURCE_DIR@": systemd_value(source_dir),
        "@PACKAGE_DIR@": systemd_value(source_dir / "stoxx_capping_service"),
        "@PYTHON@": systemd_value(python),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    if "@" in template:
        raise ValueError("unresolved placeholder in systemd unit template")
    return template


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def install(*, activate: bool) -> None:
    if not sys.platform.startswith("linux"):
        raise SystemExit("This installer requires Linux and systemd user services.")
    if sys.version_info[:2] != (3, 11):
        raise SystemExit("Run this installer with Python 3.11.")
    if shutil.which("systemctl") is None:
        raise SystemExit("systemctl is required to install this user service.")
    uv = shutil.which("uv")
    if uv is None:
        raise SystemExit("uv is required to create and populate the isolated Python environment.")

    source_dir = Path(__file__).resolve().parents[1]
    data_dir = xdg_path("XDG_DATA_HOME", Path.home() / ".local/share")
    state_dir = xdg_path("XDG_STATE_HOME", Path.home() / ".local/state")
    config_dir = xdg_path("XDG_CONFIG_HOME", Path.home() / ".config")
    app_data = data_dir / "stoxx-capping-service"
    runtime_dir = state_dir / "stoxx-capping-service"
    venv_dir = app_data / "venv"
    unit_dir = config_dir / "systemd/user"
    unit_path = unit_dir / SERVICE_NAME

    if not RUNTIME_REQUIREMENTS.is_file() or not UNIT_TEMPLATE.is_file():
        raise SystemExit("Deployment files are missing from this checkout.")
    if venv_dir.exists() and not (venv_dir / "pyvenv.cfg").is_file():
        shutil.rmtree(venv_dir)
    if not venv_dir.exists():
        run([uv, "venv", "--python", sys.executable, str(venv_dir)])
    python = venv_dir / "bin/python"
    run(
        [
            uv,
            "pip",
            "install",
            "--python",
            str(python),
            "-r",
            str(RUNTIME_REQUIREMENTS),
        ]
    )
    runtime_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    unit_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    unit_path.write_text(
        render_unit(source_dir, runtime_dir, python), encoding="utf-8"
    )
    unit_path.chmod(0o600)
    run(["systemctl", "--user", "daemon-reload"])

    if activate:
        run(["systemctl", "--user", "reset-failed", SERVICE_NAME])
        run(["systemctl", "--user", "enable", "--now", SERVICE_NAME])
        run(["systemctl", "--user", "restart", SERVICE_NAME])
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            active = subprocess.run(
                ["systemctl", "--user", "is-active", "--quiet", SERVICE_NAME],
                check=False,
            )
            if active.returncode == 0:
                break
            time.sleep(0.25)
        else:
            subprocess.run(
                ["systemctl", "--user", "--no-pager", "--full", "status", SERVICE_NAME],
                check=False,
            )
            raise SystemExit(f"{SERVICE_NAME} did not remain active after startup.")
        run(["systemctl", "--user", "--no-pager", "--full", "status", SERVICE_NAME])
    else:
        print(f"Installed {unit_path}. Start it with systemctl --user enable --now {SERVICE_NAME}.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--install-only",
        action="store_true",
        help="write the unit and environment without enabling or starting it",
    )
    args = parser.parse_args()
    install(activate=not args.install_only)


if __name__ == "__main__":
    main()
