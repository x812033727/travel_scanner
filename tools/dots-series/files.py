"""File boundary and hash helpers shared by the compiler and evidence audit."""
from __future__ import annotations

import hashlib
import json
import os
import struct
import zlib
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dumps(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def write_text_lf(path: Path, text: str) -> None:
    """Emit the same UTF-8 bytes that the repository stores on every platform."""
    path.write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8", newline="\n")


def copy_text_lf(source: Path, destination: Path) -> None:
    """Normalize the output copy while preserving the external original bytes."""
    write_text_lf(destination, source.read_text(encoding="utf-8"))


def contained(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes allowed workspace: {path}")
    return resolved


def scoped(path: Path, root: Path, subtree: Path) -> Path:
    """Check the highest boundary before trusting a possibly linked subtree.

    Retain the logical path so manifests and archive names do not change when an
    allowed internal link is used. Both the subtree and target must remain inside
    the explicitly named highest workspace/repository.
    """
    anchor = contained(subtree, root)
    contained(path, root)
    contained(path, anchor)
    return path


def tree_files(directory: Path, root: Path) -> list[Path]:
    """Validate directories before traversal and every file before content reads."""
    scoped(directory, root, directory)
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise ValueError(f"Expected authoring directory: {directory}")
    found, visited = [], set()

    def traversal_error(error: OSError) -> None:
        raise error

    for current, directories, names in os.walk(directory, followlinks=False, onerror=traversal_error):
        resolved = contained(Path(current), root)
        if resolved in visited:
            raise ValueError(f"Repeated linked source directory: {current}")
        visited.add(resolved)
        for name in directories:
            scoped(Path(current) / name, root, directory)
        for name in names:
            source = scoped(Path(current) / name, root, directory)
            if source.is_file():
                found.append(source)
    return sorted(found)


def verify_screenshot(path: Path) -> None:
    """Decode actual PNG, JPEG and WebP captures using the existing API runtime.

    Authenticated provenance and visual redaction remain reviewer decisions. The
    PNG fallback keeps dependency-free CI contract tests available; the production
    command uses the API environment's Pillow for every supported image format.
    """
    try:
        from PIL import Image
    except ImportError:
        verify_png(path)
        return
    raw = path.read_bytes()
    if raw.startswith(b"\x89PNG\r\n\x1a\n") and not raw.endswith(b"\x00\x00\x00\x00IEND\xaeB`\x82"):
        raise ValueError("PNG is missing its complete end marker")
    try:
        with Image.open(path) as picture:
            if picture.format not in {"PNG", "JPEG", "WEBP"}:
                raise ValueError("screenshots must be actual PNG, JPEG or WebP images")
            picture.verify()
        with Image.open(path) as picture:
            picture.load()
            width, height = picture.size
    except SyntaxError as error:
        raise ValueError("screenshot image data cannot be decoded") from error
    if width < 320 or height < 180 or width > 8000 or height > 8000:
        raise ValueError("screenshot dimensions must support readable UI")


def verify_png(path: Path) -> None:
    raw = path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Use the API Python environment with Pillow to decode JPEG/WebP captures")
    offset, pixels, ended, header = 8, bytearray(), False, None
    while offset + 12 <= len(raw):
        length = struct.unpack(">I", raw[offset:offset + 4])[0]
        kind = raw[offset + 4:offset + 8]
        data = raw[offset + 8:offset + 8 + length]
        checksum = raw[offset + 8 + length:offset + 12 + length]
        if len(checksum) != 4 or zlib.crc32(kind + data) & 0xFFFFFFFF != struct.unpack(">I", checksum)[0]:
            raise ValueError("invalid PNG chunk checksum")
        if kind == b"IHDR":
            if len(data) != 13:
                raise ValueError("invalid PNG image header")
            header = struct.unpack(">IIBBBBB", data)
        elif kind == b"IDAT":
            pixels.extend(data)
        elif kind == b"IEND":
            ended = True
            if offset + length + 12 != len(raw):
                raise ValueError("unexpected bytes after the PNG end")
            break
        offset += length + 12
    if not header or not ended or not pixels:
        raise ValueError("PNG is missing image data or its end marker")
    width, height, depth, color, compression, filtering, interlace = header
    if width < 320 or height < 180 or width > 8000 or height > 8000:
        raise ValueError("screenshot dimensions must support readable UI")
    if depth != 8 or color not in {0, 2, 4, 6} or compression or filtering or interlace:
        raise ValueError("save screenshots as ordinary, non-interlaced eight-bit PNGs")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}[color]
    try:
        decoded = zlib.decompress(pixels)
    except zlib.error as error:
        raise ValueError("PNG image data cannot be decoded") from error
    if len(decoded) != (width * channels + 1) * height:
        raise ValueError("PNG pixel data does not match its dimensions")
