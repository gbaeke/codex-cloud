# Evergreen Studio

A small static HTML page served by Python's built-in `http.server`.

## Running locally

```sh
python3 server.py
```

Open <http://127.0.0.1:8000> in a browser. The existing `/api/status` endpoint returns a simple server health response.

## Weather lookup

The page includes a weather lookup that calls `/api/weather?city=<city name>`. The server geocodes the city and fetches current conditions from [Open-Meteo](https://open-meteo.com/), a free weather API that does not require an API key for this use case.

No additional configuration is required. If you switch to a weather provider that needs a key, read it from an environment variable and return a clear JSON error when it is not set.
