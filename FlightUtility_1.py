"""
Flight Utility App (MVP)

A small offline desktop utility built with Python standard library + tkinter.
Features:
- Coordinate parsing and format conversion
- Fuel unit conversion for Jet A and Avgas
- Basic aviation time calculations
"""

from __future__ import annotations

import re
import importlib
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk


# -----------------------------
# App constants
# -----------------------------
APP_TITLE = "Flight Utility App"
APP_SIZE = "700x500"

STATUS_READY = "Ready"
STATUS_CONVERSION_SUCCESS = "Conversion successful"
STATUS_INVALID_COORDINATE = "Invalid coordinate format"
STATUS_LAT_RANGE = "Latitude out of range"
STATUS_LON_RANGE = "Longitude out of range"
STATUS_INVALID_MINUTES = "Invalid minutes"
STATUS_INVALID_SECONDS = "Invalid seconds"
STATUS_FUEL_SUCCESS = "Fuel calculation successful"
STATUS_ENTER_ONE_FUEL = "Enter exactly one fuel value"
STATUS_TIME_SUCCESS = "Time calculation successful"
STATUS_INVALID_TIME = "Invalid time format"
STATUS_LONGITUDE_FORMAT_INVALID = "Longitude format invalid"
STATUS_INVALID_FUEL_NUMERIC = "Only numeric fuel values are allowed"
STATUS_PYGEODESY_REQUIRED = "UTM/MGRS support requires PyGeodesy. Install with: pip install pygeodesy"
STATUS_MGRS_EXPERIMENTAL = "MGRS output placeholder: requires PyGeodesy MGRS API support"

FUEL_DENSITY_KG_PER_L = {
    "Jet A": 0.80,
    "Avgas": 0.72,
}

KG_PER_POUND = 0.45359237
LITERS_PER_US_GALLON = 3.785411784
LITERS_PER_IMP_GALLON = 4.54609


# -----------------------------
# Coordinate data models
# -----------------------------
@dataclass
class CoordinateResult:
    detected_format: str
    latitude_dd: float
    longitude_dd: float


@dataclass
class FormattedCoordinate:
    decimal_degrees: str
    degrees_decimal_minutes: str
    degrees_minutes_seconds: str
    compact_aviation_dms: str
    foreflight_format: str
    utm: str
    mgrs: str


# Optional geodesy dependency used only for UTM/MGRS support.
def _load_pygeodesy_symbol(module_name: str, symbol_name: str):
    """Dynamically load an optional PyGeodesy symbol, returning None if unavailable."""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, symbol_name, None)
    except Exception:
        return None


_py_parse_mgrs = _load_pygeodesy_symbol("pygeodesy.mgrs", "parseMGRS")
_py_parse_utm = _load_pygeodesy_symbol("pygeodesy.utm", "parseUTM5")
_py_to_utm = _load_pygeodesy_symbol("pygeodesy.utm", "toUtm8")
_py_to_mgrs = _load_pygeodesy_symbol("pygeodesy", "toMgrs")


# -----------------------------
# Coordinate parsing helpers
# -----------------------------
def _validate_range(lat_dd: float, lon_dd: float) -> tuple[bool, str]:
    """Validate decimal degree ranges for aviation coordinates."""
    if not (-90.0 <= lat_dd <= 90.0):
        return False, STATUS_LAT_RANGE
    if not (-180.0 <= lon_dd <= 180.0):
        return False, STATUS_LON_RANGE
    return True, ""


def _validate_minute_second(minutes: float | int | None, seconds: float | int | None) -> tuple[bool, str]:
    """Validate minute/second fields from DDM/DMS style inputs."""
    if minutes is not None and not (0 <= float(minutes) < 60):
        return False, STATUS_INVALID_MINUTES
    if seconds is not None and not (0 <= float(seconds) < 60):
        return False, STATUS_INVALID_SECONDS
    return True, ""


def _dms_to_decimal(deg: float, minutes: float, seconds: float, hemi: str) -> float:
    """Convert DMS components + hemisphere to signed decimal degrees."""
    decimal = float(deg) + (float(minutes) / 60.0) + (float(seconds) / 3600.0)
    if hemi in ("S", "W"):
        decimal *= -1.0
    return decimal


def _decimal_to_dms_components(value: float) -> tuple[int, int, float]:
    """Convert absolute decimal degrees to DMS components, with carry handling."""
    abs_value = abs(value)
    degrees = int(abs_value)
    minutes_full = (abs_value - degrees) * 60.0
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60.0

    # Round to 2 decimals for stable output and then normalize carries.
    seconds = round(seconds, 2)
    if seconds >= 60.0:
        seconds -= 60.0
        minutes += 1
    if minutes >= 60:
        minutes -= 60
        degrees += 1

    return degrees, minutes, seconds


def _decimal_to_ddm_components(value: float) -> tuple[int, float]:
    """Convert absolute decimal degrees to DD + decimal minutes with carry handling."""
    abs_value = abs(value)
    degrees = int(abs_value)
    minutes = (abs_value - degrees) * 60.0

    # Round to 3 decimals for DDM output and normalize carry.
    minutes = round(minutes, 3)
    if minutes >= 60.0:
        minutes -= 60.0
        degrees += 1

    return degrees, minutes


def _hemi_for_value(value: float, axis: str) -> str:
    """Resolve hemisphere letter from signed decimal value and axis."""
    if axis == "lat":
        return "N" if value >= 0 else "S"
    return "E" if value >= 0 else "W"


def _parse_decimal_degrees(text: str) -> CoordinateResult | None:
    """Parse decimal degree pairs, e.g. '6.585900, 3.565636'."""
    match = re.match(
        r"^\s*([+-]?\d+(?:\.\d+)?)\s*[, ]+\s*([+-]?\d+(?:\.\d+)?)\s*$",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return None

    lat_dd = float(match.group(1))
    lon_dd = float(match.group(2))

    is_valid, message = _validate_range(lat_dd, lon_dd)
    if not is_valid:
        raise ValueError(message)

    return CoordinateResult("Decimal Degrees", lat_dd, lon_dd)


def _parse_ddm(text: str) -> CoordinateResult | None:
    """
    Parse Degrees Decimal Minutes inputs.

    Supported examples:
    - 06°35.154'N 003°33.938'E
    - 06 35.154 N 003 33.938 E

    The regex allows symbols/spaces between numeric groups while still enforcing
    hemisphere letters and expected component ordering.
    """
    pattern = re.compile(
        r"^\s*"
        r"(\d{1,2})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)\s*([NS])\s+"
        r"(\d{1,3})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)\s*([EW])"
        r"\s*$",
        flags=re.IGNORECASE,
    )
    match = pattern.match(text)
    if not match:
        return None

    lat_deg = int(match.group(1))
    lat_min = float(match.group(2))
    lat_hemi = match.group(3).upper()

    lon_deg = int(match.group(4))
    lon_min = float(match.group(5))
    lon_hemi = match.group(6).upper()

    is_valid_ms, message = _validate_minute_second(lat_min, None)
    if not is_valid_ms:
        raise ValueError(message)
    is_valid_ms, message = _validate_minute_second(lon_min, None)
    if not is_valid_ms:
        raise ValueError(message)

    lat_dd = _dms_to_decimal(lat_deg, lat_min, 0.0, lat_hemi)
    lon_dd = _dms_to_decimal(lon_deg, lon_min, 0.0, lon_hemi)

    is_valid, message = _validate_range(lat_dd, lon_dd)
    if not is_valid:
        raise ValueError(message)

    return CoordinateResult("Degrees Decimal Minutes", lat_dd, lon_dd)


def _parse_dms(text: str) -> CoordinateResult | None:
    """
    Parse full Degrees Minutes Seconds coordinates.

    Supported examples:
    - 06°35'09.24"N 003°33'56.29"E
    - 06 35 09.24 N 003 33 56.29 E
    """
    pattern = re.compile(
        r"^\s*"
        r"(\d{1,2})[^\dNSEW]+(\d{1,2})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)\s*([NS])\s+"
        r"(\d{1,3})[^\dNSEW]+(\d{1,2})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)\s*([EW])"
        r"\s*$",
        flags=re.IGNORECASE,
    )
    match = pattern.match(text)
    if not match:
        return None

    lat_deg = int(match.group(1))
    lat_min = int(match.group(2))
    lat_sec = float(match.group(3))
    lat_hemi = match.group(4).upper()

    lon_deg = int(match.group(5))
    lon_min = int(match.group(6))
    lon_sec = float(match.group(7))
    lon_hemi = match.group(8).upper()

    is_valid_ms, message = _validate_minute_second(lat_min, lat_sec)
    if not is_valid_ms:
        raise ValueError(message)
    is_valid_ms, message = _validate_minute_second(lon_min, lon_sec)
    if not is_valid_ms:
        raise ValueError(message)

    lat_dd = _dms_to_decimal(lat_deg, lat_min, lat_sec, lat_hemi)
    lon_dd = _dms_to_decimal(lon_deg, lon_min, lon_sec, lon_hemi)

    is_valid, message = _validate_range(lat_dd, lon_dd)
    if not is_valid:
        raise ValueError(message)

    return CoordinateResult("Degrees Minutes Seconds", lat_dd, lon_dd)


def _parse_compact_aviation(text: str) -> CoordinateResult | None:
    """
    Parse compact aviation DMS forms.

    Supported examples:
    - 063509.24N 0033356.29E
    - 063509.24N/0033356.29E
    - N063509.24 E0033356.29

    Strategy:
    - Try suffix hemisphere style first (digits then N/S or E/W)
    - Then try prefix hemisphere style (N/S then digits)
    - Validate minute/second limits and geographic ranges
    """
    text_u = text.strip().upper()

    suffix_pattern = re.compile(
        r"^\s*"
        r"(\d{2})(\d{2})(\d{2}(?:\.\d+)?)\s*([NS])"
        r"\s*(?:/|\s)\s*"
        r"(\d{3})(\d{2})(\d{2}(?:\.\d+)?)\s*([EW])"
        r"\s*$"
    )

    prefix_pattern = re.compile(
        r"^\s*"
        r"([NS])\s*(\d{2})(\d{2})(\d{2}(?:\.\d+)?)"
        r"\s+"
        r"([EW])\s*(\d{3})(\d{2})(\d{2}(?:\.\d+)?)"
        r"\s*$"
    )

    match = suffix_pattern.match(text_u)
    if match:
        lat_deg = int(match.group(1))
        lat_min = int(match.group(2))
        lat_sec = float(match.group(3))
        lat_hemi = match.group(4)

        lon_deg = int(match.group(5))
        lon_min = int(match.group(6))
        lon_sec = float(match.group(7))
        lon_hemi = match.group(8)
    else:
        match = prefix_pattern.match(text_u)
        if not match:
            return None

        lat_hemi = match.group(1)
        lat_deg = int(match.group(2))
        lat_min = int(match.group(3))
        lat_sec = float(match.group(4))

        lon_hemi = match.group(5)
        lon_deg = int(match.group(6))
        lon_min = int(match.group(7))
        lon_sec = float(match.group(8))

    is_valid_ms, message = _validate_minute_second(lat_min, lat_sec)
    if not is_valid_ms:
        raise ValueError(message)
    is_valid_ms, message = _validate_minute_second(lon_min, lon_sec)
    if not is_valid_ms:
        raise ValueError(message)

    lat_dd = _dms_to_decimal(lat_deg, lat_min, lat_sec, lat_hemi)
    lon_dd = _dms_to_decimal(lon_deg, lon_min, lon_sec, lon_hemi)

    is_valid, message = _validate_range(lat_dd, lon_dd)
    if not is_valid:
        raise ValueError(message)

    return CoordinateResult("Compact Aviation DMS", lat_dd, lon_dd)


def _lat_lon_from_geodesy(obj) -> tuple[float, float]:
    """Extract decimal degree latitude/longitude from common PyGeodesy objects."""
    if obj is None:
        raise ValueError(STATUS_INVALID_COORDINATE)

    if hasattr(obj, "lat") and hasattr(obj, "lon"):
        return float(obj.lat), float(obj.lon)

    if hasattr(obj, "toLatLon"):
        latlon = obj.toLatLon()
        if isinstance(latlon, (tuple, list)) and len(latlon) >= 2:
            return float(latlon[0]), float(latlon[1])
        if hasattr(latlon, "lat") and hasattr(latlon, "lon"):
            return float(latlon.lat), float(latlon.lon)

    if isinstance(obj, (tuple, list)) and len(obj) >= 2:
        return float(obj[0]), float(obj[1])

    raise ValueError(STATUS_INVALID_COORDINATE)


def _parse_utm(text: str) -> CoordinateResult | None:
    """Parse UTM text using PyGeodesy when available."""
    if _py_parse_utm is None:
        return None

    try:
        utm_obj = _py_parse_utm(text)
    except Exception:
        return None

    try:
        lat_dd, lon_dd = _lat_lon_from_geodesy(utm_obj)
    except ValueError:
        return None

    is_valid, message = _validate_range(lat_dd, lon_dd)
    if not is_valid:
        raise ValueError(message)

    return CoordinateResult("UTM", lat_dd, lon_dd)


def _parse_mgrs(text: str) -> CoordinateResult | None:
    """Parse MGRS text using PyGeodesy when available."""
    if _py_parse_mgrs is None:
        return None

    try:
        mgrs_obj = _py_parse_mgrs(text)
    except Exception:
        return None

    try:
        if hasattr(mgrs_obj, "toUtm"):
            lat_dd, lon_dd = _lat_lon_from_geodesy(mgrs_obj.toUtm())
        elif hasattr(mgrs_obj, "toUtmUps"):
            lat_dd, lon_dd = _lat_lon_from_geodesy(mgrs_obj.toUtmUps())
        else:
            lat_dd, lon_dd = _lat_lon_from_geodesy(mgrs_obj)
    except Exception:
        return None

    is_valid, message = _validate_range(lat_dd, lon_dd)
    if not is_valid:
        raise ValueError(message)

    return CoordinateResult("MGRS", lat_dd, lon_dd)


def parse_coordinate_text(text: str) -> CoordinateResult:
    """
    Detect and parse a coordinate string into decimal degrees.

    The parser tries each supported format and returns the first successful match.
    Validation errors are surfaced as ValueError with user-facing status text.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError(STATUS_INVALID_COORDINATE)

    parsers = [
        _parse_decimal_degrees,
        _parse_ddm,
        _parse_dms,
        _parse_compact_aviation,
        _parse_utm,
        _parse_mgrs,
    ]

    validation_error: ValueError | None = None
    for parser in parsers:
        try:
            result = parser(cleaned)
            if result is not None:
                return result
        except ValueError as exc:
            # Keep the latest validation error in case no parser succeeds.
            validation_error = exc

    # Heuristic for malformed compact longitude such as 00333562.9E.
    if re.search(r"\d+[EW]$", cleaned.upper()) and not re.search(r"[NS]", cleaned.upper()):
        raise ValueError(STATUS_LONGITUDE_FORMAT_INVALID)

    if validation_error is not None:
        raise validation_error

    raise ValueError(STATUS_INVALID_COORDINATE)


def format_coordinate_outputs(lat_dd: float, lon_dd: float) -> FormattedCoordinate:
    """Generate all requested output formats from decimal degree baseline."""
    lat_hemi = _hemi_for_value(lat_dd, "lat")
    lon_hemi = _hemi_for_value(lon_dd, "lon")

    lat_dms_deg, lat_dms_min, lat_dms_sec = _decimal_to_dms_components(lat_dd)
    lon_dms_deg, lon_dms_min, lon_dms_sec = _decimal_to_dms_components(lon_dd)

    lat_ddm_deg, lat_ddm_min = _decimal_to_ddm_components(lat_dd)
    lon_ddm_deg, lon_ddm_min = _decimal_to_ddm_components(lon_dd)

    decimal_degrees = f"{lat_dd:.6f}, {lon_dd:.6f}"

    degrees_decimal_minutes = (
        f"{lat_ddm_deg:02d}°{lat_ddm_min:06.3f}'{lat_hemi}\n"
        f"{lon_ddm_deg:03d}°{lon_ddm_min:06.3f}'{lon_hemi}"
    )

    degrees_minutes_seconds = (
        f"{lat_dms_deg:02d}°{lat_dms_min:02d}'{lat_dms_sec:05.2f}\"{lat_hemi}\n"
        f"{lon_dms_deg:03d}°{lon_dms_min:02d}'{lon_dms_sec:05.2f}\"{lon_hemi}"
    )

    compact_aviation_dms = (
        f"{lat_dms_deg:02d}{lat_dms_min:02d}{lat_dms_sec:05.2f}{lat_hemi} "
        f"{lon_dms_deg:03d}{lon_dms_min:02d}{lon_dms_sec:05.2f}{lon_hemi}"
    )

    foreflight_format = (
        f"{lat_dms_deg:02d}{lat_dms_min:02d}{lat_dms_sec:05.2f}{lat_hemi}/"
        f"{lon_dms_deg:03d}{lon_dms_min:02d}{lon_dms_sec:05.2f}{lon_hemi}"
    )

    # UTM/MGRS are derived from the same decimal-degree baseline so existing
    # behavior stays unchanged for all prior formats.
    if _py_to_utm is None:
        utm_value = STATUS_PYGEODESY_REQUIRED
        mgrs_value = STATUS_PYGEODESY_REQUIRED
    else:
        try:
            utm_obj = _py_to_utm(lat_dd, lon_dd)
            utm_value = str(utm_obj)
        except Exception:
            utm_obj = None
            utm_value = STATUS_PYGEODESY_REQUIRED

        if utm_obj is None:
            mgrs_value = STATUS_PYGEODESY_REQUIRED
        else:
            try:
                if _py_to_mgrs is not None:
                    mgrs_value = str(_py_to_mgrs(lat_dd, lon_dd))
                elif hasattr(utm_obj, "toMgrs"):
                    mgrs_value = str(utm_obj.toMgrs())
                else:
                    mgrs_value = STATUS_MGRS_EXPERIMENTAL
            except Exception:
                mgrs_value = STATUS_MGRS_EXPERIMENTAL

    return FormattedCoordinate(
        decimal_degrees=decimal_degrees,
        degrees_decimal_minutes=degrees_decimal_minutes,
        degrees_minutes_seconds=degrees_minutes_seconds,
        compact_aviation_dms=compact_aviation_dms,
        foreflight_format=foreflight_format,
        utm=utm_value,
        mgrs=mgrs_value,
    )


# -----------------------------
# Fuel conversion helpers
# -----------------------------
def convert_fuel_values(input_unit: str, input_value: float, fuel_type: str) -> dict[str, float]:
    """Convert one fuel input to all supported units."""
    density = FUEL_DENSITY_KG_PER_L[fuel_type]

    if input_unit == "Pounds":
        kg = input_value * KG_PER_POUND
    elif input_unit == "Kilograms":
        kg = input_value
    elif input_unit == "Litres":
        kg = input_value * density
    elif input_unit == "US Gallons":
        kg = input_value * LITERS_PER_US_GALLON * density
    elif input_unit == "Imperial Gallons":
        kg = input_value * LITERS_PER_IMP_GALLON * density
    else:
        raise ValueError("Unsupported fuel unit")

    liters = kg / density

    return {
        "Pounds": kg / KG_PER_POUND,
        "Kilograms": kg,
        "Litres": liters,
        "US Gallons": liters / LITERS_PER_US_GALLON,
        "Imperial Gallons": liters / LITERS_PER_IMP_GALLON,
    }


# -----------------------------
# Time helpers
# -----------------------------
def _parse_hhmm_clock(value: str) -> int:
    """Parse HH:MM in 24-hour clock format and return total minutes."""
    match = re.match(r"^(\d{1,2}):(\d{2})$", value.strip())
    if not match:
        raise ValueError(STATUS_INVALID_TIME)

    hours = int(match.group(1))
    minutes = int(match.group(2))

    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        raise ValueError(STATUS_INVALID_TIME)

    return hours * 60 + minutes


def _parse_hhmm_duration(value: str) -> int:
    """Parse HH:MM duration and return total minutes (hours may exceed 23)."""
    match = re.match(r"^(\d+):(\d{2})$", value.strip())
    if not match:
        raise ValueError(STATUS_INVALID_TIME)

    hours = int(match.group(1))
    minutes = int(match.group(2))

    if hours < 0 or not (0 <= minutes <= 59):
        raise ValueError(STATUS_INVALID_TIME)

    return hours * 60 + minutes


def _format_minutes_to_hhmm(minutes_total: int) -> str:
    """Format minutes to HH:MM using 24-hour wrapping."""
    normalized = minutes_total % (24 * 60)
    hours = normalized // 60
    minutes = normalized % 60
    return f"{hours:02d}:{minutes:02d}"


def _format_elapsed(minutes_total: int) -> str:
    """Format elapsed minutes as HH:MM (not wrapped to 24h)."""
    hours = minutes_total // 60
    minutes = minutes_total % 60
    return f"{hours:02d}:{minutes:02d}"


# -----------------------------
# UI
# -----------------------------
class FlightUtilityApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(650, 450)

        self.status_var = tk.StringVar(value=STATUS_READY)

        self._build_ui()

    def set_status(self, message: str) -> None:
        """Update the shared bottom status bar."""
        self.status_var.set(message)

    def _build_ui(self) -> None:
        """Construct notebook and tab content."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        self.coordinates_tab = ttk.Frame(notebook, padding=10)
        self.fuel_tab = ttk.Frame(notebook, padding=10)
        self.time_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.coordinates_tab, text="Coordinates")
        notebook.add(self.fuel_tab, text="Fuel")
        notebook.add(self.time_tab, text="Time")

        self._build_coordinates_tab()
        self._build_fuel_tab()
        self._build_time_tab()

        status = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    # -------- Coordinates tab --------
    def _build_coordinates_tab(self) -> None:
        frame = self.coordinates_tab
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Paste Coordinate").grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.coord_input_var = tk.StringVar()
        coord_entry = ttk.Entry(frame, textvariable=self.coord_input_var)
        coord_entry.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=1, sticky="w", pady=(0, 10))

        ttk.Button(button_frame, text="Parse", command=self.on_parse_coordinate).grid(
            row=0, column=0, padx=(0, 6)
        )
        ttk.Button(button_frame, text="Clear", command=self.on_clear_coordinate).grid(
            row=0, column=1
        )

        self.coord_detected_format_var = tk.StringVar()
        self.coord_status_var = tk.StringVar(value=STATUS_READY)
        self.coord_decimal_var = tk.StringVar()
        self.coord_ddm_var = tk.StringVar()
        self.coord_dms_var = tk.StringVar()
        self.coord_compact_var = tk.StringVar()
        self.coord_foreflight_var = tk.StringVar()
        self.coord_utm_var = tk.StringVar()
        self.coord_mgrs_var = tk.StringVar()

        self._add_output_row(frame, 2, "Detected Format", self.coord_detected_format_var)
        self._add_output_row(frame, 3, "Status", self.coord_status_var)
        self._add_output_row(frame, 4, "Decimal Degrees", self.coord_decimal_var)
        self._add_output_row(frame, 5, "Degrees Decimal Minutes", self.coord_ddm_var)
        self._add_output_row(frame, 6, "Degrees Minutes Seconds", self.coord_dms_var)
        self._add_output_row(frame, 7, "Compact Aviation DMS", self.coord_compact_var)
        self._add_output_row(frame, 8, "ForeFlight Format", self.coord_foreflight_var)
        self._add_output_row(frame, 9, "UTM", self.coord_utm_var)
        self._add_output_row(frame, 10, "MGRS", self.coord_mgrs_var)

    def _add_output_row(self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="nw", pady=2)
        ttk.Label(parent, textvariable=var, justify="left", anchor="w").grid(
            row=row, column=1, sticky="w", pady=2
        )

    def on_parse_coordinate(self) -> None:
        """Parse coordinate input, convert to all outputs, and update status fields."""
        text = self.coord_input_var.get().strip()

        try:
            result = parse_coordinate_text(text)
            formatted = format_coordinate_outputs(result.latitude_dd, result.longitude_dd)
        except ValueError as exc:
            message = str(exc) if str(exc) else STATUS_INVALID_COORDINATE
            self.coord_status_var.set(message)
            self.set_status(message)
            return

        self.coord_detected_format_var.set(result.detected_format)
        self.coord_status_var.set(STATUS_CONVERSION_SUCCESS)
        self.coord_decimal_var.set(formatted.decimal_degrees)
        self.coord_ddm_var.set(formatted.degrees_decimal_minutes)
        self.coord_dms_var.set(formatted.degrees_minutes_seconds)
        self.coord_compact_var.set(formatted.compact_aviation_dms)
        self.coord_foreflight_var.set(formatted.foreflight_format)
        self.coord_utm_var.set(formatted.utm)
        self.coord_mgrs_var.set(formatted.mgrs)

        if formatted.utm == STATUS_PYGEODESY_REQUIRED or formatted.mgrs == STATUS_PYGEODESY_REQUIRED:
            self.coord_status_var.set(STATUS_PYGEODESY_REQUIRED)
            self.set_status(STATUS_PYGEODESY_REQUIRED)
        else:
            self.set_status(STATUS_CONVERSION_SUCCESS)

    def on_clear_coordinate(self) -> None:
        """Clear coordinate input and outputs."""
        self.coord_input_var.set("")
        self.coord_detected_format_var.set("")
        self.coord_status_var.set(STATUS_READY)
        self.coord_decimal_var.set("")
        self.coord_ddm_var.set("")
        self.coord_dms_var.set("")
        self.coord_compact_var.set("")
        self.coord_foreflight_var.set("")
        self.coord_utm_var.set("")
        self.coord_mgrs_var.set("")
        self.set_status(STATUS_READY)

    # -------- Fuel tab --------
    def _build_fuel_tab(self) -> None:
        frame = self.fuel_tab
        frame.grid_columnconfigure(1, weight=1)

        ttk.Label(frame, text="Fuel Type").grid(row=0, column=0, sticky="w", pady=3)
        self.fuel_type_var = tk.StringVar(value="Jet A")
        fuel_type_combo = ttk.Combobox(
            frame,
            textvariable=self.fuel_type_var,
            values=list(FUEL_DENSITY_KG_PER_L.keys()),
            state="readonly",
            width=20,
        )
        fuel_type_combo.grid(row=0, column=1, sticky="w", pady=3)

        self.fuel_entry_vars: dict[str, tk.StringVar] = {
            "Pounds": tk.StringVar(),
            "Kilograms": tk.StringVar(),
            "Litres": tk.StringVar(),
            "US Gallons": tk.StringVar(),
            "Imperial Gallons": tk.StringVar(),
        }

        start_row = 1
        for idx, unit in enumerate(self.fuel_entry_vars.keys()):
            ttk.Label(frame, text=unit).grid(row=start_row + idx, column=0, sticky="w", pady=3)
            ttk.Entry(frame, textvariable=self.fuel_entry_vars[unit], width=25).grid(
                row=start_row + idx, column=1, sticky="w", pady=3
            )

        button_row = start_row + len(self.fuel_entry_vars)
        ttk.Button(frame, text="Calculate", command=self.on_calculate_fuel).grid(
            row=button_row, column=0, pady=(10, 4), sticky="w"
        )
        ttk.Button(frame, text="Clear", command=self.on_clear_fuel).grid(
            row=button_row, column=1, pady=(10, 4), sticky="w"
        )

        self.fuel_status_var = tk.StringVar(value=STATUS_READY)
        ttk.Label(frame, text="Status").grid(row=button_row + 1, column=0, sticky="nw", pady=(8, 0))
        ttk.Label(frame, textvariable=self.fuel_status_var, anchor="w").grid(
            row=button_row + 1, column=1, sticky="w", pady=(8, 0)
        )

    def on_calculate_fuel(self) -> None:
        """Convert fuel units from exactly one user-provided value."""
        non_empty: list[tuple[str, str]] = []
        for unit, var in self.fuel_entry_vars.items():
            raw = var.get().strip()
            if raw:
                non_empty.append((unit, raw))

        if len(non_empty) != 1:
            self.fuel_status_var.set(STATUS_ENTER_ONE_FUEL)
            self.set_status(STATUS_ENTER_ONE_FUEL)
            return

        input_unit, raw_value = non_empty[0]
        try:
            value = float(raw_value)
        except ValueError:
            self.fuel_status_var.set(STATUS_INVALID_FUEL_NUMERIC)
            self.set_status(STATUS_INVALID_FUEL_NUMERIC)
            return

        fuel_type = self.fuel_type_var.get()
        converted = convert_fuel_values(input_unit, value, fuel_type)

        for unit, result_value in converted.items():
            self.fuel_entry_vars[unit].set(f"{result_value:.3f}")

        self.fuel_status_var.set(STATUS_FUEL_SUCCESS)
        self.set_status(STATUS_FUEL_SUCCESS)

    def on_clear_fuel(self) -> None:
        """Clear all fuel fields and reset status."""
        for var in self.fuel_entry_vars.values():
            var.set("")

        self.fuel_status_var.set(STATUS_READY)
        self.set_status(STATUS_READY)

    # -------- Time tab --------
    def _build_time_tab(self) -> None:
        frame = self.time_tab
        frame.grid_columnconfigure(1, weight=1)

        current_row = 0

        ttk.Label(frame, text="Add Time").grid(row=current_row, column=0, sticky="w", pady=(0, 4))
        current_row += 1

        self.add_start_var = tk.StringVar()
        self.add_duration_var = tk.StringVar()
        self.add_result_var = tk.StringVar()

        ttk.Label(frame, text="Start time HH:MM").grid(row=current_row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.add_start_var, width=18).grid(row=current_row, column=1, sticky="w", pady=2)
        current_row += 1

        ttk.Label(frame, text="Duration HH:MM").grid(row=current_row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.add_duration_var, width=18).grid(row=current_row, column=1, sticky="w", pady=2)
        current_row += 1

        ttk.Button(frame, text="Calculate Add", command=self.on_add_time).grid(
            row=current_row, column=0, sticky="w", pady=4
        )
        ttk.Label(frame, text="Result HH:MM").grid(row=current_row, column=1, sticky="w", padx=(120, 0))
        ttk.Entry(frame, textvariable=self.add_result_var, width=12, state="readonly").grid(
            row=current_row, column=1, sticky="w", padx=(210, 0)
        )
        current_row += 2

        ttk.Label(frame, text="Subtract Time").grid(row=current_row, column=0, sticky="w", pady=(6, 4))
        current_row += 1

        self.sub_start_var = tk.StringVar()
        self.sub_duration_var = tk.StringVar()
        self.sub_result_var = tk.StringVar()

        ttk.Label(frame, text="Start time HH:MM").grid(row=current_row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.sub_start_var, width=18).grid(row=current_row, column=1, sticky="w", pady=2)
        current_row += 1

        ttk.Label(frame, text="Duration HH:MM").grid(row=current_row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.sub_duration_var, width=18).grid(row=current_row, column=1, sticky="w", pady=2)
        current_row += 1

        ttk.Button(frame, text="Calculate Subtract", command=self.on_subtract_time).grid(
            row=current_row, column=0, sticky="w", pady=4
        )
        ttk.Label(frame, text="Result HH:MM").grid(row=current_row, column=1, sticky="w", padx=(120, 0))
        ttk.Entry(frame, textvariable=self.sub_result_var, width=12, state="readonly").grid(
            row=current_row, column=1, sticky="w", padx=(210, 0)
        )
        current_row += 2

        ttk.Label(frame, text="Elapsed Time").grid(row=current_row, column=0, sticky="w", pady=(6, 4))
        current_row += 1

        self.el_start_var = tk.StringVar()
        self.el_end_var = tk.StringVar()
        self.el_result_var = tk.StringVar()

        ttk.Label(frame, text="Start time HH:MM").grid(row=current_row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.el_start_var, width=18).grid(row=current_row, column=1, sticky="w", pady=2)
        current_row += 1

        ttk.Label(frame, text="End time HH:MM").grid(row=current_row, column=0, sticky="w", pady=2)
        ttk.Entry(frame, textvariable=self.el_end_var, width=18).grid(row=current_row, column=1, sticky="w", pady=2)
        current_row += 1

        ttk.Button(frame, text="Calculate Elapsed", command=self.on_elapsed_time).grid(
            row=current_row, column=0, sticky="w", pady=4
        )
        ttk.Label(frame, text="Elapsed HH:MM").grid(row=current_row, column=1, sticky="w", padx=(120, 0))
        ttk.Entry(frame, textvariable=self.el_result_var, width=12, state="readonly").grid(
            row=current_row, column=1, sticky="w", padx=(210, 0)
        )

    def on_add_time(self) -> None:
        try:
            start_minutes = _parse_hhmm_clock(self.add_start_var.get())
            duration_minutes = _parse_hhmm_duration(self.add_duration_var.get())
        except ValueError:
            self.set_status(STATUS_INVALID_TIME)
            return

        self.add_result_var.set(_format_minutes_to_hhmm(start_minutes + duration_minutes))
        self.set_status(STATUS_TIME_SUCCESS)

    def on_subtract_time(self) -> None:
        try:
            start_minutes = _parse_hhmm_clock(self.sub_start_var.get())
            duration_minutes = _parse_hhmm_duration(self.sub_duration_var.get())
        except ValueError:
            self.set_status(STATUS_INVALID_TIME)
            return

        self.sub_result_var.set(_format_minutes_to_hhmm(start_minutes - duration_minutes))
        self.set_status(STATUS_TIME_SUCCESS)

    def on_elapsed_time(self) -> None:
        try:
            start_minutes = _parse_hhmm_clock(self.el_start_var.get())
            end_minutes = _parse_hhmm_clock(self.el_end_var.get())
        except ValueError:
            self.set_status(STATUS_INVALID_TIME)
            return

        elapsed = (end_minutes - start_minutes) % (24 * 60)
        self.el_result_var.set(_format_elapsed(elapsed))
        self.set_status(STATUS_TIME_SUCCESS)


def main() -> None:
    app = FlightUtilityApp()
    app.mainloop()


if __name__ == "__main__":
    main()
