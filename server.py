"""Serve the static HTML page with Python's built-in web server."""

import json
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8000


class HtmlPageHandler(SimpleHTTPRequestHandler):
    """Serve index.html for the site root."""

    def do_GET(self):
        if self.path == "/api/status":
            payload = {
                "message": "Evergreen Studio server is running",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            body = json.dumps(payload).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), HtmlPageHandler)
    print(f"Serving index.html at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
