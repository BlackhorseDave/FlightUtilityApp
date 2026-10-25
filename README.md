# Flight Utility PWA

Flight Utility is an offline-first web app with time calculations, fuel conversions, and coordinate conversions. Version 1.0 release verification and Capacitor packaging are in progress; this branch is not yet a verified release.

## Run locally

```bash
py -c "import http.server; http.server.SimpleHTTPRequestHandler.extensions_map['.js'] = 'application/javascript'; http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, port=8001, bind='127.0.0.1')"
```

Then open:

```text
http://localhost:8001/
```

Run the server command from the project root, where index.html and app.js are located. These instructions use Windows and the Python launcher (py). Open http://localhost:8001/ on the same computer. Stop the server with Ctrl+C in its terminal. Phone installation and offline testing require a suitable HTTPS deployment; the local-only server above is not accessible from a phone.

## Current scope

- - Time and duration calculations using hours/minutes, decimal hours, addition, subtraction, multiplication, and division.
- Fuel conversions for Jet A, Avgas, Regular Gasoline, and Diesel, with automatic recalculation when a quantity or fuel type changes.
- Coordinate parsing and conversion for Decimal Degrees, Degrees and Decimal Minutes, Degrees/Minutes/Seconds, compact aviation DMS, UTM, and MGRS.
- Coordinate results are cleared when input changes; PARSE must succeed before results can be copied.
- PWA manifest and service worker, with an offline status check that verifies the listed app assets are cached.

## Fuel conversion assumptions

Mass-to-volume conversions use these fixed densities:

| Fuel | Density (kg/L) |
| --- | ---: |
| Jet A | 0.80 |
| Avgas | 0.72 |
| Regular Gasoline | 0.74 |
| Diesel | 0.84 |

The app does not adjust density for temperature or a measured fuel sample. Results reflect these fixed assumptions.

Conversion constants: 1 pound = 0.45359237 kilograms; 1 US gallon = 3.785411784 litres; 1 Imperial gallon = 4.54609 litres.

## Coordinate assumptions and display precision

UTM calculations use WGS84 ellipsoid constants. The app does not transform coordinates between datums; input coordinates must already use the intended WGS84 reference.

| Output format | Display precision |
| --- | --- |
| Decimal Degrees | 6 decimal places |
| Degrees and Decimal Minutes | 3 decimal places in minutes |
| Degrees/Minutes/Seconds | 2 decimal places in seconds |
| Compact aviation DMS | 2 decimal places in seconds |
| UTM | Easting and northing rounded to whole metres |
| MGRS | 5 digits each for easting and northing |

Displayed decimal places describe formatting, not independently verified positional accuracy.

### Coordinate coverage

Latitude/longitude inputs are limited to 90°S–90°N and 180°W–180°E. UTM and the app's UTM-based MGRS conversions are limited to 80°S–84°N, inclusive. Polar UPS coordinates are not supported.

## Verification status

UTM and MGRS conversion are implemented in the browser app. MGRS uses the bundled lib/mgrs.js file.

Local desktop tests passed for offline reload, calculations in all three tabs, missing-cache detection, cache recovery, and the readiness-check timeout. These results do not establish phone or native-app readiness.

Outstanding release work is tracked in Flight-Utility-App-v1-Launch-Checklist.md, including independent coordinate accuracy checks, fuel-density and coordinate documentation, MGRS commercial license and notices, regression testing, and final release verification.

The published GitHub Pages app and generated www assets have not yet been updated with the current release fixes.