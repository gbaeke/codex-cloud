"""Serve the static HTML page with Python's built-in web server."""

import json
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import urlopen

HOST = "127.0.0.1"
PORT = 8000
REQUEST_TIMEOUT = 10


def fetch_json(url):
    """Fetch JSON from an external API with a short timeout."""
    with urlopen(url, timeout=REQUEST_TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def weather_payload_for_city(city):
    """Look up a city and return current weather from Open-Meteo."""
    geocode_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={quote(city)}&count=1&language=en&format=json"
    )
    # Geocoding keeps the browser API simple: users can enter a city instead of coordinates.
    geocode = fetch_json(geocode_url)
    matches = geocode.get("results", [])
    if not matches:
        return None

    place = matches[0]
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={place['latitude']}&longitude={place['longitude']}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    )
    weather = fetch_json(weather_url)
    current = weather.get("current")
    units = weather.get("current_units", {})
    if not current:
        raise ValueError("Open-Meteo did not return current weather data.")

    return {
        "city": place.get("name", city),
        "country": place.get("country", ""),
        "admin1": place.get("admin1", ""),
        "temperature": current.get("temperature_2m"),
        "temperatureUnit": units.get("temperature_2m", "°C"),
        "humidity": current.get("relative_humidity_2m"),
        "humidityUnit": units.get("relative_humidity_2m", "%"),
        "windSpeed": current.get("wind_speed_10m"),
        "windSpeedUnit": units.get("wind_speed_10m", "km/h"),
        "weatherCode": current.get("weather_code"),
        "time": current.get("time"),
        "source": "Open-Meteo",
    }


class HtmlPageHandler(SimpleHTTPRequestHandler):
    """Serve index.html for the site root."""

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/api/status":
            payload = {
                "message": "Evergreen Studio server is running",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.send_json(200, payload)
            return

        if parsed_path.path == "/api/weather":
            # Open-Meteo is keyless for this usage, so the city query is all the client sends.
            city = parse_qs(parsed_path.query).get("city", [""])[0].strip()
            if not city:
                self.send_json(400, {"error": "Missing city. Add ?city=City Name to the request."})
                return

            try:
                payload = weather_payload_for_city(city)
            except (HTTPError, URLError, TimeoutError, ValueError) as error:
                self.send_json(502, {"error": f"Unable to fetch weather data: {error}"})
                return

            if payload is None:
                self.send_json(404, {"error": f"City not found: {city}"})
                return

            self.send_json(200, payload)
            return

        if parsed_path.path == "/":
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
