#!/usr/bin/env python3
"""Serve an unpacked preview on this computer, including HTTP byte-range seeks."""

import argparse
import functools
import http.server
import os
from pathlib import Path
import re
import socketserver


class PreviewHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range = None
        path = self.translate_path(self.path)
        if not self.headers.get("Range") or not os.path.isfile(path):
            return super().send_head()
        stream = open(path, "rb")
        size = os.fstat(stream.fileno()).st_size
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers["Range"].strip())
        if not match or not any(match.groups()) or size == 0:
            return self.invalid_range(stream, size)
        first, last = match.groups()
        if first:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        else:
            start, end = max(0, size - int(last)), size - 1
        if start > end or start >= size:
            return self.invalid_range(stream, size)
        self.byte_range = start, end
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        stream.seek(start)
        return stream

    def invalid_range(self, stream, size):
        stream.close()
        self.send_response(416)
        self.send_header("Content-Range", f"bytes */{size}")
        self.send_header("Content-Length", "0")
        self.end_headers()
        return None

    def copyfile(self, source, outputfile):
        if self.byte_range is None:
            return super().copyfile(source, outputfile)
        remaining = self.byte_range[1] - self.byte_range[0] + 1
        while remaining:
            data = source.read(min(1024 * 1024, remaining))
            if not data:
                break
            outputfile.write(data)
            remaining -= len(data)

    def log_message(self, format, *args):
        # Avoid noisy per-range media access logs; errors retain normal reporting.
        if len(args) > 1 and str(args[1]).startswith(("4", "5")):
            super().log_message(format, *args)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    directory = args.directory.resolve()
    if not (directory / "START_HERE.html").is_file():
        parser.error(f"Preview not found: {directory / 'START_HERE.html'}")
    handler = functools.partial(PreviewHandler, directory=str(directory))
    with Server(("127.0.0.1", args.port), handler) as server:
        print(f"http://127.0.0.1:{server.server_port}/START_HERE.html", flush=True)
        print("Keep this terminal open while watching; Ctrl+C stops the preview.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
