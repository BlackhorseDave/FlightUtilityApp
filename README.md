# Flight Utility PWA

Offline browser test build of the Python/Tkinter Flight Utility MVP.

## Run locally

```bash
python3 -m http.server 4173 --directory flight-utility-pwa
```

Then open:

```text
http://localhost:4173
```

For iPhone testing on the same network, use the computer's LAN IP instead of `localhost`.

## Current scope

- Coordinate parsing and output formatting from the Python MVP.
- Fuel conversion for Jet A, Avgas, Regular Gasoline, and Diesel.
- Duration calculator with `h:mm`, decimal hour, `+`, `-`, `×`, and `÷` support.
- Installable PWA shell with manifest and service worker.

## Known gap

UTM/MGRS support is not implemented in the browser build yet. The Python app uses optional PyGeodesy support, so the PWA currently labels those fields as pending geodesy support.
