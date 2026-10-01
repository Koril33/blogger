"""Uploaded SSH helper; Python 3.9+ standard library only. Never imported by the CLI."""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
import tarfile
import uuid
from pathlib import Path, PurePosixPath


def deploy(archive_path: str, root_path: str, expected_hash: str):
    requested = Path(root_path)
    if (
        not requested.is_absolute()
        or ".." in requested.parts
        or len(requested.parts) < 3
        or requested.is_symlink()
    ):
        raise ValueError("Unsafe remote root")
    root = requested.resolve()
    if len(root.parts) < 3:
        raise ValueError("Unsafe resolved remote root")
    archive_path = Path(archive_path)
    digest = hashlib.sha256()
    with archive_path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    if digest.hexdigest() != expected_hash:
        raise ValueError("Archive SHA-256 mismatch")
    root.mkdir(parents=True, exist_ok=True)
    managed = root / ".blogger"
    if (
        managed.is_symlink()
        or (managed / "owner").is_symlink()
        or (managed.exists() and not (managed / "owner").is_file())
    ):
        raise ValueError("Unmanaged release directory")
    if managed.exists() and (managed / "owner").read_text(encoding="utf-8") != "djhx-blogger\n":
        raise ValueError("Unmanaged release owner")
    managed.mkdir(mode=0o755, exist_ok=True)
    (managed / "owner").write_text("djhx-blogger\n", encoding="utf-8")
    releases = managed / "releases"
    if releases.is_symlink():
        raise ValueError("Unsafe releases directory")
    releases.mkdir(mode=0o755, exist_ok=True)
    lock = managed / "deploy.lock"
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(descriptor)
    release = releases / uuid.uuid4().hex
    incoming = root / (".blogger-link-" + release.name)
    live = root / "blog"
    backup = root / "blog.bak"
    switched = False
    legacy_backup = None
    preserved_backup = None
    previous = None
    try:
        release.mkdir(mode=0o755)
        seen, total = set(), 0
        with tarfile.open(archive_path, "r:gz") as archive:
            for member in archive:
                parts = PurePosixPath(member.name).parts
                if (
                    not parts
                    or parts[0] != "public"
                    or ".." in parts
                    or not (member.isfile() or member.isdir())
                    or member.name in seen
                ):
                    raise ValueError("Unsafe archive member: " + member.name)
                seen.add(member.name)
                total += member.size
                if total > 20 * 1024**3:
                    raise ValueError("Archive exceeds 20 GiB")
                destination = release.joinpath(*parts[1:])
                destination.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
                if member.isdir():
                    destination.mkdir(exist_ok=True, mode=0o755)
                else:
                    with archive.extractfile(member) as source, destination.open("xb") as target:
                        shutil.copyfileobj(source, target, 1024 * 1024)
                    destination.chmod(0o644)
        if not (release / "index.html").is_file() or not (release / "archive.html").is_file():
            raise ValueError("Missing generated pages")
        if live.is_symlink():
            previous = live.resolve(strict=True)
            if previous.parent != releases or not previous.is_dir():
                raise ValueError("Existing blog link is outside managed releases")
        elif live.exists():
            if (
                not live.is_dir()
                or not (live / "index.html").is_file()
                or not (live / "archive.html").is_file()
            ):
                raise ValueError("Existing blog is not a generated site")
            # One-time migration from a real directory. Roll back on switch failure.
            legacy_backup = releases / ("legacy-" + uuid.uuid4().hex)
            previous = legacy_backup
        if backup.exists() and not backup.is_symlink():
            if not backup.is_dir() or not (backup / "index.html").is_file():
                raise ValueError("Existing blog.bak is unmanaged")
            # Preserve old pre-0.3 backup; do not erase it during migration.
            preserved_backup = releases / ("legacy-backup-" + uuid.uuid4().hex)
            backup.rename(preserved_backup)
        incoming.symlink_to(release.relative_to(root), target_is_directory=True)
        if previous is not None:
            backup_link = root / (".blogger-backup-link-" + release.name)
            backup_link.symlink_to(previous.relative_to(root), target_is_directory=True)
            try:
                os.replace(backup_link, backup)
            finally:
                backup_link.unlink(missing_ok=True)
        if legacy_backup is not None:
            live.rename(legacy_backup)
        try:
            os.replace(incoming, live)
        except BaseException:
            if legacy_backup is not None:
                legacy_backup.rename(live)
            raise
        switched = True
        # Keep current + previous release; preserve legacy backups for manual review.
        for old in releases.iterdir():
            if (
                old.is_dir()
                and not old.is_symlink()
                and old not in {release, previous}
                and len(old.name) == 32
                and all(c in "0123456789abcdef" for c in old.name)
            ):
                try:
                    shutil.rmtree(old)
                except OSError as exc:
                    print(f"Deployed; could not clean old release {old}: {exc}", file=sys.stderr)
        return str(release)
    finally:
        incoming.unlink(missing_ok=True)
        if (
            not switched
            and legacy_backup is not None
            and backup.is_symlink()
            and backup.resolve() == legacy_backup
        ):
            backup.unlink()
        if not switched and preserved_backup is not None and preserved_backup.exists():
            preserved_backup.rename(backup)
        if not switched and release.exists():
            shutil.rmtree(release)
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    print(deploy(*sys.argv[1:]))
