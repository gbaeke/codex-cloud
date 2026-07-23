# Pink Cookie Pop

A lightweight browser-based Cookie Clicker style game with a cohesive pink theme. The site is a single static HTML page served by Python's built-in `http.server`.

## Features

- Landing page hero with basic game instructions.
- Large accessible cookie button and visible score counters.
- Click upgrade that increases cookies earned per click.
- Passive upgrade that adds cookies every second.
- Reset button for starting over.
- Minimal `localStorage` persistence for score and upgrade counts.
- Responsive, dependency-free HTML, CSS, and JavaScript.

## Running locally

```sh
python3 server.py
```

Open <http://127.0.0.1:8000> in a browser.
