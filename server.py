"""Serve the static HTML page with Python's built-in web server."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8000


class HtmlPageHandler(SimpleHTTPRequestHandler):
    """Serve index.html for the site root."""

    def do_GET(self):
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
