#!/usr/bin/env python3
"""Verify and package the tracked TheKeyMachine installer payload."""

from __future__ import annotations

import argparse
import ast
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_PATHS = (
    "README.md",
    "TheKeyMachine",
    "TheKeyMachine_Drag&Drop_installer.py",
    "how_to_install.txt",
    "license_gpl-3.0.txt",
)
TAG_PATTERN = re.compile(
    r"v(?P<version>[0-9]+\.[0-9]+\.[0-9]+)"
)
INSTALLER_SOURCE = "TheKeyMachine_Drag&Drop_installer.py"
VERSION_FILE = "TheKeyMachine/data/version.txt"


def release_version() -> str:
    version = (ROOT / VERSION_FILE).read_text(encoding="ascii").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError(f"Invalid version in {VERSION_FILE}: {version!r}")
    return version


def tracked_payload() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *PAYLOAD_PATHS],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    files = [ROOT / name.decode("utf-8") for name in result.stdout.split(b"\0") if name]
    tracked = {path.relative_to(ROOT).as_posix() for path in files}
    missing = [path for path in PAYLOAD_PATHS if path != "TheKeyMachine" and path not in tracked]
    if VERSION_FILE not in tracked:
        missing.append(VERSION_FILE)
    if missing or not any(path.startswith("TheKeyMachine/") for path in tracked):
        raise ValueError(f"Missing tracked payload: {', '.join(missing or ['TheKeyMachine'])}")
    for path in files:
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Payload entry must be a regular file: {path.relative_to(ROOT)}")
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def verify(tag: str | None = None) -> tuple[str, list[Path]]:
    version = release_version()
    if tag:
        match = TAG_PATTERN.fullmatch(tag)
        if not match:
            raise ValueError("Tag must look like v1.2.3")
        if match.group("version") != version:
            raise ValueError(f"Tag {tag} does not match release version {version}")

    files = tracked_payload()
    for path in files:
        if path.suffix == ".py":
            ast.parse(path.read_bytes(), filename=str(path.relative_to(ROOT)))
    return version, files


def package(output_dir: Path, tag: str | None) -> tuple[Path, Path, str]:
    version, files = verify(tag)
    tag = tag or f"v{version}"
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"TheKeyMachine-{tag}.zip"
    prefix = f"TheKeyMachine-{tag}"

    def archive_name(path: Path) -> str:
        relative = path.relative_to(ROOT).as_posix()
        if relative == INSTALLER_SOURCE:
            relative = f"TheKeyMachine_Installer_v{version.replace('.', '_')}.py"
        return f"{prefix}/{relative}"

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, archive_name(path))

    expected = [archive_name(path) for path in files]
    with zipfile.ZipFile(archive) as bundle:
        if bundle.namelist() != expected or bundle.testzip() is not None:
            raise ValueError("Packaged ZIP does not exactly match the tracked installer payload")

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    return archive, checksum, digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify_parser = subparsers.add_parser("verify", help="check versions, payload, and Python syntax")
    verify_parser.add_argument("--tag")
    package_parser = subparsers.add_parser("package", help="build and inspect the release ZIP")
    package_parser.add_argument("--tag")
    package_parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()

    try:
        if args.command == "verify":
            version, files = verify(args.tag)
            print(f"Verified Beta {version} across {len(files)} payload files")
        else:
            archive, checksum, digest = package(args.output_dir, args.tag)
            print(f"Created {archive}")
            print(f"Created {checksum}")
            print(f"SHA-256 {digest}")
    except (OSError, subprocess.CalledProcessError, SyntaxError, ValueError, zipfile.BadZipFile) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
