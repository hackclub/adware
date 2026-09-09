#!/usr/bin/env python3
"""Local preview server: no caching, and reachable on both IP stacks.

Two problems this exists to solve.

1. Caching. `python3 -m http.server` sends Last-Modified but no Cache-Control
   and no ETag, so browsers fall back to heuristic freshness, cache the page and
   serve it without revalidating. Edits then look like they did not land.

2. localhost. macOS resolves "localhost" to ::1 before 127.0.0.1. A server bound
   only to IPv4 is reachable at http://127.0.0.1:8000 but not at
   http://localhost:8000 in browsers that do not fall back the way curl does.
   So bind both loopback addresses.

Loopback only, deliberately: binding 0.0.0.0 or :: would publish the whole repo
directory on the local network, and that includes laptop.png and the internal
markdown.

Dev only. This never ships: .vercelignore excludes .claude/.
"""
import http.server
import socket
import sys
import threading

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):        # keep the console readable
        msg = fmt % args
        if ".html" in msg or "GET / " in msg or " 404 " in msg:
            super().log_message(fmt, *args)


def listener(family, host):
    class Server(http.server.ThreadingHTTPServer):
        address_family = family
        allow_reuse_address = True
        daemon_threads = True
    return Server((host, PORT), NoCacheHandler)


if __name__ == "__main__":
    servers = []
    for family, host in ((socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")):
        try:
            servers.append((host, listener(family, host)))
        except OSError as exc:
            print(f"  note: could not bind {host}:{PORT} ({exc})")

    if not servers:
        sys.exit(f"could not bind port {PORT} on either stack")

    for host, _ in servers:
        shown = f"[{host}]" if ":" in host else host
        print(f"serving http://{shown}:{PORT}  (caching disabled)")
    print(f"  -> http://localhost:{PORT}")

    for _, srv in servers[1:]:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        servers[0][1].serve_forever()
    except KeyboardInterrupt:
        pass
