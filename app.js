"use strict";

const STATUS_READY = "Ready";
const STATUS_CONVERSION_SUCCESS = "Conversion successful";
const STATUS_INVALID_COORDINATE = "Invalid coordinate format";
const STATUS_LAT_RANGE = "Latitude out of range";
const STATUS_LON_RANGE = "Longitude out of range";
const STATUS_INVALID_MINUTES = "Invalid minutes";
const STATUS_INVALID_SECONDS = "Invalid seconds";
const STATUS_FUEL_SUCCESS = "Fuel calculation successful";
const STATUS_ENTER_ONE_FUEL = "Enter exactly one fuel value";
const STATUS_TIME_SUCCESS = "Time calculation successful";
const STATUS_INVALID_TIME = "Invalid time format";
const STATUS_LONGITUDE_FORMAT_INVALID = "Longitude format invalid";
const STATUS_INVALID_FUEL_NUMERIC = "Only numeric fuel values are allowed";
const STATUS_BROWSER_GEODESY_PENDING = "Browser build: pending geodesy support";

const FUEL_DENSITY_KG_PER_L = {
  "Jet A": 0.80,
  "Avgas": 0.72,
  "Regular Gasoline": 0.74,
  "Diesel": 0.84,
};

const KG_PER_POUND = 0.45359237;
const LITERS_PER_US_GALLON = 3.785411784;
const LITERS_PER_IMP_GALLON = 4.54609;

// UTM/MGRS support notes:
// - Decimal degrees remain the app's internal baseline format.
// - UTM conversion is done locally with WGS84 math in JavaScript.
// - MGRS conversion uses the local offline lib/mgrs.js file.
// - No online APIs or CDN calls are used.

const WGS84_A = 6378137.0;
const WGS84_ECC_SQUARED = 0.00669438;
const UTM_K0 = 0.9996;

function getUtmZoneNumber(lonDd) {
  return Math.floor((lonDd + 180) / 6) + 1;
}

function getUtmBandLetter(latDd) {
  if (latDd < -80 || latDd > 84) return "";

  const bands = "CDEFGHJKLMNPQRSTUVWX";
  const index = Math.floor((latDd + 80) / 8);
  return bands[Math.min(index, bands.length - 1)];
}

function latLonToUtm(latDd, lonDd) {
  // UTM conversion from decimal degrees to WGS84 UTM.
  // Valid for normal UTM coverage: 80S to 84N.
  if (latDd < -80 || latDd > 84) {
    throw new Error("UTM is only valid from 80°S to 84°N");
  }

  const zoneNumber = getUtmZoneNumber(lonDd);
  const zoneLetter = getUtmBandLetter(latDd);
  const lonOrigin = (zoneNumber - 1) * 6 - 180 + 3;

  const latRad = latDd * Math.PI / 180;
  const lonRad = lonDd * Math.PI / 180;
  const lonOriginRad = lonOrigin * Math.PI / 180;

  const eccPrimeSquared = WGS84_ECC_SQUARED / (1 - WGS84_ECC_SQUARED);
  const n = WGS84_A / Math.sqrt(1 - WGS84_ECC_SQUARED * Math.sin(latRad) ** 2);
  const t = Math.tan(latRad) ** 2;
  const c = eccPrimeSquared * Math.cos(latRad) ** 2;
  const a = Math.cos(latRad) * (lonRad - lonOriginRad);

  const m = WGS84_A * (
    (1 - WGS84_ECC_SQUARED / 4 - 3 * WGS84_ECC_SQUARED ** 2 / 64 - 5 * WGS84_ECC_SQUARED ** 3 / 256) * latRad
    - (3 * WGS84_ECC_SQUARED / 8 + 3 * WGS84_ECC_SQUARED ** 2 / 32 + 45 * WGS84_ECC_SQUARED ** 3 / 1024) * Math.sin(2 * latRad)
    + (15 * WGS84_ECC_SQUARED ** 2 / 256 + 45 * WGS84_ECC_SQUARED ** 3 / 1024) * Math.sin(4 * latRad)
    - (35 * WGS84_ECC_SQUARED ** 3 / 3072) * Math.sin(6 * latRad)
  );

  let easting = UTM_K0 * n * (
    a + (1 - t + c) * a ** 3 / 6
    + (5 - 18 * t + t ** 2 + 72 * c - 58 * eccPrimeSquared) * a ** 5 / 120
  ) + 500000.0;

  let northing = UTM_K0 * (
    m + n * Math.tan(latRad) * (
      a ** 2 / 2
      + (5 - t + 9 * c + 4 * c ** 2) * a ** 4 / 24
      + (61 - 58 * t + t ** 2 + 600 * c - 330 * eccPrimeSquared) * a ** 6 / 720
    )
  );

  if (latDd < 0) {
    northing += 10000000.0;
  }

  easting = Math.round(easting);
  northing = Math.round(northing);

  return {
    zoneNumber,
    zoneLetter,
    easting,
    northing,
    display: `Zone ${zoneNumber}${zoneLetter} ${easting}E ${northing}N`,
    compact: `${zoneNumber}${zoneLetter} ${easting} ${northing}`
  };
}

function latLonToMgrs(latDd, lonDd) {
  // MGRS conversion happens here.
  // The local lib/mgrs.js file exposes window.mgrs.
  if (!window.mgrs || typeof window.mgrs.forward !== "function") {
    return STATUS_BROWSER_GEODESY_PENDING;
  }

  return window.mgrs.forward([lonDd, latDd], 5);
}

function formatUtmMgrsOutputs(latDd, lonDd) {
  try {
    const utm = latLonToUtm(latDd, lonDd);
    const mgrsValue = latLonToMgrs(latDd, lonDd);

    return {
      utm: `${utm.display} | ${utm.compact}`,
      mgrs: mgrsValue
    };
  } catch (error) {
    return {
      utm: error.message || STATUS_BROWSER_GEODESY_PENDING,
      mgrs: error.message || STATUS_BROWSER_GEODESY_PENDING
    };
  }
}

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

function fail(message) {
  throw new Error(message);
}

function validateRange(latDd, lonDd) {
  if (latDd < -90 || latDd > 90) fail(STATUS_LAT_RANGE);
  if (lonDd < -180 || lonDd > 180) fail(STATUS_LON_RANGE);
}

function validateMinuteSecond(minutes, seconds = null) {
  if (minutes !== null && !(Number(minutes) >= 0 && Number(minutes) < 60)) {
    fail(STATUS_INVALID_MINUTES);
  }
  if (seconds !== null && !(Number(seconds) >= 0 && Number(seconds) < 60)) {
    fail(STATUS_INVALID_SECONDS);
  }
}

function dmsToDecimal(deg, minutes, seconds, hemi) {
  let decimal = Number(deg) + Number(minutes) / 60 + Number(seconds) / 3600;
  if (hemi === "S" || hemi === "W") decimal *= -1;
  return decimal;
}

function decimalToDmsComponents(value) {
  const absValue = Math.abs(value);
  let degrees = Math.trunc(absValue);
  const minutesFull = (absValue - degrees) * 60;
  let minutes = Math.trunc(minutesFull);
  let seconds = Math.round((minutesFull - minutes) * 6000) / 100;
  if (seconds >= 60) {
    seconds -= 60;
    minutes += 1;
  }
  if (minutes >= 60) {
    minutes -= 60;
    degrees += 1;
  }
  return { degrees, minutes, seconds };
}

function decimalToDdmComponents(value) {
  const absValue = Math.abs(value);
  let degrees = Math.trunc(absValue);
  let minutes = Math.round((absValue - degrees) * 60000) / 1000;
  if (minutes >= 60) {
    minutes -= 60;
    degrees += 1;
  }
  return { degrees, minutes };
}

function hemiForValue(value, axis) {
  if (axis === "lat") return value >= 0 ? "N" : "S";
  return value >= 0 ? "E" : "W";
}

function padInt(value, width) {
  return String(value).padStart(width, "0");
}

function fixedPad(value, width, decimals) {
  return value.toFixed(decimals).padStart(width, "0");
}

function parseDecimalDegrees(text) {
  const match = text.match(/^\s*([+-]?\d+(?:\.\d+)?)\s*[, ]+\s*([+-]?\d+(?:\.\d+)?)\s*$/i);
  if (!match) return null;
  const latDd = Number(match[1]);
  const lonDd = Number(match[2]);
  validateRange(latDd, lonDd);
  return { detectedFormat: "Decimal Degrees", latitudeDd: latDd, longitudeDd: lonDd };
}

function parseDdm(text) {
  const suffixPattern = /^\s*(\d{1,2})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)[^\dNSEW]*\s*([NS])\s+(\d{1,3})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)[^\dNSEW]*\s*([EW])\s*$/i;
  const prefixPattern = /^\s*([NS])\s*(\d{1,2})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)[^\dNSEW]*\s+([EW])\s*(\d{1,3})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)[^\dNSEW]*\s*$/i;

  let match = text.match(suffixPattern);
  let latDeg;
  let latMin;
  let latHemi;
  let lonDeg;
  let lonMin;
  let lonHemi;

  if (match) {
    latDeg = Number(match[1]);
    latMin = Number(match[2]);
    latHemi = match[3].toUpperCase();
    lonDeg = Number(match[4]);
    lonMin = Number(match[5]);
    lonHemi = match[6].toUpperCase();
  } else {
    match = text.match(prefixPattern);
    if (!match) return null;
    latHemi = match[1].toUpperCase();
    latDeg = Number(match[2]);
    latMin = Number(match[3]);
    lonHemi = match[4].toUpperCase();
    lonDeg = Number(match[5]);
    lonMin = Number(match[6]);
  }

  validateMinuteSecond(latMin);
  validateMinuteSecond(lonMin);
  const latDd = dmsToDecimal(latDeg, latMin, 0, latHemi);
  const lonDd = dmsToDecimal(lonDeg, lonMin, 0, lonHemi);
  validateRange(latDd, lonDd);
  return { detectedFormat: "Degrees Decimal Minutes", latitudeDd: latDd, longitudeDd: lonDd };
}

function parseDms(text) {
  const pattern = /^\s*(\d{1,2})[^\dNSEW]+(\d{1,2})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)\s*([NS])\s+(\d{1,3})[^\dNSEW]+(\d{1,2})[^\dNSEW]+(\d{1,2}(?:\.\d+)?)\s*([EW])\s*$/i;
  const match = text.match(pattern);
  if (!match) return null;

  const latDeg = Number(match[1]);
  const latMin = Number(match[2]);
  const latSec = Number(match[3]);
  const latHemi = match[4].toUpperCase();
  const lonDeg = Number(match[5]);
  const lonMin = Number(match[6]);
  const lonSec = Number(match[7]);
  const lonHemi = match[8].toUpperCase();

  validateMinuteSecond(latMin, latSec);
  validateMinuteSecond(lonMin, lonSec);
  const latDd = dmsToDecimal(latDeg, latMin, latSec, latHemi);
  const lonDd = dmsToDecimal(lonDeg, lonMin, lonSec, lonHemi);
  validateRange(latDd, lonDd);
  return { detectedFormat: "Degrees Minutes Seconds", latitudeDd: latDd, longitudeDd: lonDd };
}

function parseCompactAviation(text) {
  const cleaned = text.trim().toUpperCase();
  const suffixPattern = /^\s*(\d{2})(\d{2})(\d{2}(?:\.\d+)?)\s*([NS])\s*(?:\/|\s)\s*(\d{3})(\d{2})(\d{2}(?:\.\d+)?)\s*([EW])\s*$/;
  const prefixPattern = /^\s*([NS])\s*(\d{2})(\d{2})(\d{2}(?:\.\d+)?)\s+([EW])\s*(\d{3})(\d{2})(\d{2}(?:\.\d+)?)\s*$/;

  let match = cleaned.match(suffixPattern);
  let latDeg;
  let latMin;
  let latSec;
  let latHemi;
  let lonDeg;
  let lonMin;
  let lonSec;
  let lonHemi;

  if (match) {
    latDeg = Number(match[1]);
    latMin = Number(match[2]);
    latSec = Number(match[3]);
    latHemi = match[4];
    lonDeg = Number(match[5]);
    lonMin = Number(match[6]);
    lonSec = Number(match[7]);
    lonHemi = match[8];
  } else {
    match = cleaned.match(prefixPattern);
    if (!match) return null;
    latHemi = match[1];
    latDeg = Number(match[2]);
    latMin = Number(match[3]);
    latSec = Number(match[4]);
    lonHemi = match[5];
    lonDeg = Number(match[6]);
    lonMin = Number(match[7]);
    lonSec = Number(match[8]);
  }

  validateMinuteSecond(latMin, latSec);
  validateMinuteSecond(lonMin, lonSec);
  const latDd = dmsToDecimal(latDeg, latMin, latSec, latHemi);
  const lonDd = dmsToDecimal(lonDeg, lonMin, lonSec, lonHemi);
  validateRange(latDd, lonDd);
  return { detectedFormat: "Compact Aviation DMS", latitudeDd: latDd, longitudeDd: lonDd };
}

function parseCoordinateText(text) {
  const cleaned = text.trim();
  if (!cleaned) fail(STATUS_INVALID_COORDINATE);

  let validationError = null;
  for (const parser of [parseDecimalDegrees, parseDdm, parseDms, parseCompactAviation]) {
    try {
      const result = parser(cleaned);
      if (result) return result;
    } catch (error) {
      validationError = error;
    }
  }

  if (/\d+[EW]$/i.test(cleaned) && !/[NS]/i.test(cleaned)) {
    fail(STATUS_LONGITUDE_FORMAT_INVALID);
  }
  if (validationError) throw validationError;
  fail(STATUS_INVALID_COORDINATE);
}

function formatCoordinateOutputs(latDd, lonDd) {
  const latHemi = hemiForValue(latDd, "lat");
  const lonHemi = hemiForValue(lonDd, "lon");
  const latDms = decimalToDmsComponents(latDd);
  const lonDms = decimalToDmsComponents(lonDd);
  const latDdm = decimalToDdmComponents(latDd);
  const lonDdm = decimalToDdmComponents(lonDd);
  const utmMgrs = formatUtmMgrsOutputs(latDd, lonDd);

  return {
    decimalDegrees: `${latDd.toFixed(6)}, ${lonDd.toFixed(6)}`,
    degreesDecimalMinutes: `${padInt(latDdm.degrees, 2)}°${fixedPad(latDdm.minutes, 6, 3)}'${latHemi}\n${padInt(lonDdm.degrees, 3)}°${fixedPad(lonDdm.minutes, 6, 3)}'${lonHemi}`,
    degreesMinutesSeconds: `${padInt(latDms.degrees, 2)}°${padInt(latDms.minutes, 2)}'${fixedPad(latDms.seconds, 5, 2)}"${latHemi}\n${padInt(lonDms.degrees, 3)}°${padInt(lonDms.minutes, 2)}'${fixedPad(lonDms.seconds, 5, 2)}"${lonHemi}`,
    compactAviationDms: `${padInt(latDms.degrees, 2)}${padInt(latDms.minutes, 2)}${fixedPad(latDms.seconds, 5, 2)}${latHemi} ${padInt(lonDms.degrees, 3)}${padInt(lonDms.minutes, 2)}${fixedPad(lonDms.seconds, 5, 2)}${lonHemi}`,
    foreflightFormat: `${padInt(latDms.degrees, 2)}${padInt(latDms.minutes, 2)}${fixedPad(latDms.seconds, 5, 2)}${latHemi}/${padInt(lonDms.degrees, 3)}${padInt(lonDms.minutes, 2)}${fixedPad(lonDms.seconds, 5, 2)}${lonHemi}`,
    utm: utmMgrs.utm,
    mgrs: utmMgrs.mgrs,
  };
}

function convertFuelValues(inputUnit, inputValue, fuelType) {
  const density = FUEL_DENSITY_KG_PER_L[fuelType];
  let kg;
  if (inputUnit === "Pounds") kg = inputValue * KG_PER_POUND;
  else if (inputUnit === "Kilograms") kg = inputValue;
  else if (inputUnit === "Litres") kg = inputValue * density;
  else if (inputUnit === "US Gallons") kg = inputValue * LITERS_PER_US_GALLON * density;
  else if (inputUnit === "Imperial Gallons") kg = inputValue * LITERS_PER_IMP_GALLON * density;
  else fail("Unsupported fuel unit");

  const liters = kg / density;
  return {
    "Pounds": kg / KG_PER_POUND,
    "Kilograms": kg,
    "Litres": liters,
    "US Gallons": liters / LITERS_PER_US_GALLON,
    "Imperial Gallons": liters / LITERS_PER_IMP_GALLON,
  };
}

function parseDurationToken(token) {
  const cleaned = token.trim();
  if (!cleaned) fail(STATUS_INVALID_TIME);
  if (cleaned.includes(":")) {
    const match = cleaned.match(/^(\d+):(\d{2})$/);
    if (!match) fail(STATUS_INVALID_TIME);
    const hours = Number(match[1]);
    const minutes = Number(match[2]);
    if (minutes < 0 || minutes > 59) fail(STATUS_INVALID_TIME);
    return { value: hours + minutes / 60, wasHhmm: true };
  }
  if (!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(cleaned)) fail(STATUS_INVALID_TIME);
  return { value: Number(cleaned), wasHhmm: false };
}

function decimalHoursToHhmm(value) {
  const sign = value < 0 ? "-" : "";
  const totalMinutes = Math.round(Math.abs(value) * 60);
  const hours = Math.trunc(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${sign}${hours}:${padInt(minutes, 2)}`;
}

function formatDecimalHours(value) {
  return value.toFixed(2);
}

function formatNumericResult(value) {
  if (Math.abs(value - Math.round(value)) < 1e-10) return String(Math.round(value));
  return value.toFixed(10).replace(/0+$/, "").replace(/\.$/, "");
}

function normalizeExpression(expression) {
  return expression.replaceAll("×", "*").replaceAll("÷", "/").replaceAll("−", "-");
}

function evaluateDurationExpression(expression) {
  const cleaned = normalizeExpression(expression).replace(/\s/g, "");
  if (!cleaned) fail(STATUS_INVALID_TIME);

  const tokenPattern = /\d+:\d{2}|\d+(?:\.\d+)?|\.\d+|[+\-*/]/g;
  const tokens = cleaned.match(tokenPattern);
  if (!tokens || tokens.join("") !== cleaned) fail(STATUS_INVALID_TIME);

  const precedence = { "+": 1, "-": 1, "*": 2, "/": 2 };
  const values = [];
  const operators = [];
  let hhmmCount = 0;
  let decimalCount = 0;
  let firstStyle = null;
  let expectValue = true;
  let unarySign = 1;

  function applyTopOperator() {
    if (values.length < 2 || !operators.length) fail(STATUS_INVALID_TIME);
    const right = values.pop();
    const left = values.pop();
    const op = operators.pop();
    if (op === "+") values.push(left + right);
    else if (op === "-") values.push(left - right);
    else if (op === "*") values.push(left * right);
    else if (op === "/") {
      if (Math.abs(right) < 1e-12) fail(STATUS_INVALID_TIME);
      values.push(left / right);
    } else fail(STATUS_INVALID_TIME);
  }

  for (const token of tokens) {
    if (expectValue) {
      if (token in precedence) {
        if (token === "-") {
          unarySign *= -1;
          continue;
        }
        if (token === "+") continue;
        fail(STATUS_INVALID_TIME);
      }
      const parsed = parseDurationToken(token);
      if (parsed.wasHhmm) {
        hhmmCount += 1;
        if (!firstStyle) firstStyle = "hhmm";
      } else if (token.includes(".")) {
        decimalCount += 1;
        if (!firstStyle) firstStyle = "decimal";
      }
      values.push(unarySign * parsed.value);
      unarySign = 1;
      expectValue = false;
    } else {
      if (!(token in precedence)) fail(STATUS_INVALID_TIME);
      while (operators.length && precedence[operators.at(-1)] >= precedence[token]) {
        applyTopOperator();
      }
      operators.push(token);
      expectValue = true;
    }
  }

  if (expectValue) fail(STATUS_INVALID_TIME);
  while (operators.length) applyTopOperator();
  if (values.length !== 1) fail(STATUS_INVALID_TIME);

  let preferredStyle;
  if (hhmmCount > decimalCount) preferredStyle = "hhmm";
  else if (decimalCount > hhmmCount) preferredStyle = "decimal";
  else if (hhmmCount === 0 && decimalCount === 0) preferredStyle = "numeric";
  else preferredStyle = firstStyle || "numeric";

  return { resultHours: values[0], preferredStyle };
}

function parseSingleDurationValue(value) {
  let cleaned = value.trim();
  if (!cleaned) fail(STATUS_INVALID_TIME);
  let sign = 1;
  if (cleaned[0] === "+" || cleaned[0] === "-") {
    sign = cleaned[0] === "-" ? -1 : 1;
    cleaned = cleaned.slice(1);
  }
  const parsed = parseDurationToken(cleaned);
  return { value: sign * parsed.value, wasHhmm: parsed.wasHhmm };
}

function setText(id, value) {
  document.getElementById(id).textContent = value || "-";
}

function setStatus(element, message, isError = false) {
  element.textContent = message;
  element.classList.toggle("error", isError);
  element.classList.toggle("success", !isError && message !== STATUS_READY);
}

function wireTabs() {
  $$(".tab-button").forEach((button) => {
    button.addEventListener("click", () => {
      $$(".tab-button").forEach((tab) => tab.classList.remove("active"));
      $$(".tab-panel").forEach((panel) => panel.classList.remove("active"));
      button.classList.add("active");
      document.getElementById(button.dataset.tab).classList.add("active");
    });
  });
}

function wireCoordinates() {
  const input = $("#coordInput");
  const status = $("#coordStatus");

  function clearOutputs() {
    for (const id of ["coordDetected", "coordDecimal", "coordDdm", "coordDms", "coordCompact", "coordForeflight"]) {
      setText(id, "-");
    }
    setText("coordUtm", STATUS_BROWSER_GEODESY_PENDING);
    setText("coordMgrs", STATUS_BROWSER_GEODESY_PENDING);
  }

  $("#coordParse").addEventListener("click", () => {
    try {
      const parsed = parseCoordinateText(input.value);
      const formatted = formatCoordinateOutputs(parsed.latitudeDd, parsed.longitudeDd);
      setText("coordDetected", parsed.detectedFormat);
      setText("coordDecimal", formatted.decimalDegrees);
      setText("coordDdm", formatted.degreesDecimalMinutes);
      setText("coordDms", formatted.degreesMinutesSeconds);
      setText("coordCompact", formatted.compactAviationDms);
      setText("coordForeflight", formatted.foreflightFormat);
      setText("coordUtm", formatted.utm);
      setText("coordMgrs", formatted.mgrs);
      setStatus(status, STATUS_CONVERSION_SUCCESS);
    } catch (error) {
      setStatus(status, error.message || STATUS_INVALID_COORDINATE, true);
    }
  });

  $("#coordClear").addEventListener("click", () => {
    input.value = "";
    clearOutputs();
    setStatus(status, STATUS_READY);
  });

  $("#coordPaste").addEventListener("click", async () => {
    try {
      input.value = await navigator.clipboard.readText();
      $("#coordParse").click();
    } catch {
      setStatus(status, "Paste is blocked by this browser", true);
    }
  });

  $$("#coordResults [data-copy-target]").forEach((button) => {
    button.addEventListener("click", async () => {
      const value = document.getElementById(button.dataset.copyTarget).textContent;
      if (!value || value === "-") return;
      try {
        await navigator.clipboard.writeText(value);
        setStatus(status, "Copied");
      } catch {
        setStatus(status, "Copy is blocked by this browser", true);
      }
    });
  });
}

function wireFuel() {
  const status = $("#fuelStatus");
  const inputs = $$("#fuelGrid input");
  const byUnit = Object.fromEntries(inputs.map((input) => [input.dataset.unit, input]));

  $("#fuelCalculate").addEventListener("click", () => {
    const nonEmpty = inputs
      .map((input) => [input.dataset.unit, input.value.trim()])
      .filter(([, value]) => value !== "");

    if (nonEmpty.length !== 1) {
      setStatus(status, STATUS_ENTER_ONE_FUEL, true);
      return;
    }

    const [unit, rawValue] = nonEmpty[0];
    const value = Number(rawValue);
    if (!Number.isFinite(value)) {
      setStatus(status, STATUS_INVALID_FUEL_NUMERIC, true);
      return;
    }

    const converted = convertFuelValues(unit, value, $("#fuelType").value);
    for (const [outputUnit, resultValue] of Object.entries(converted)) {
      byUnit[outputUnit].value = resultValue.toFixed(3);
    }
    setStatus(status, STATUS_FUEL_SUCCESS);
  });

  $("#fuelClear").addEventListener("click", () => {
    inputs.forEach((input) => {
      input.value = "";
    });
    setStatus(status, STATUS_READY);
  });
}

function wireTime() {
  const expressionEl = $("#timeExpression");
  const resultEl = $("#timeResult");
  const status = $("#timeStatus");
  let expression = "";
  let resultShown = false;

  function refresh() {
    expressionEl.textContent = expression || "0";
    if (!resultShown) resultEl.textContent = expression || "0";
  }

  function appendValue(char) {
    if (resultShown) {
      expression = "";
      resultShown = false;
    }
    expression += char;
    refresh();
  }

  function appendOperator(operator) {
    if (!expression) {
      if (operator === "−") {
        expression = "-";
        refresh();
      }
      return;
    }
    if (/[+\-*/×÷−]$/.test(expression)) {
      expression = expression.slice(0, -1) + operator;
    } else {
      expression += operator;
    }
    resultShown = false;
    refresh();
  }

  function clear() {
    expression = "";
    resultShown = false;
    refresh();
    setStatus(status, STATUS_READY);
  }

  function backspace() {
    if (resultShown) {
      clear();
      return;
    }
    expression = expression.slice(0, -1);
    refresh();
  }

  function convertValue() {
    try {
      const parsed = parseSingleDurationValue(expression);
      expression = parsed.wasHhmm ? formatDecimalHours(parsed.value) : decimalHoursToHhmm(parsed.value);
      resultShown = false;
      refresh();
      setStatus(status, STATUS_TIME_SUCCESS);
    } catch {
      setStatus(status, STATUS_INVALID_TIME, true);
    }
  }

  function evaluate() {
    try {
      const evaluated = evaluateDurationExpression(expression);
      let resultValue;
      if (evaluated.preferredStyle === "hhmm") resultValue = decimalHoursToHhmm(evaluated.resultHours);
      else if (evaluated.preferredStyle === "decimal") resultValue = formatDecimalHours(evaluated.resultHours);
      else resultValue = formatNumericResult(evaluated.resultHours);
      expressionEl.textContent = `${expression} =`;
      resultEl.textContent = resultValue;
      expression = resultValue;
      resultShown = true;
      setStatus(status, STATUS_TIME_SUCCESS);
    } catch {
      resultEl.textContent = "Error";
      setStatus(status, STATUS_INVALID_TIME, true);
    }
  }

  $("#timeButtons").addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    const label = button.textContent.trim();
    if (/^[0-9.:]$/.test(label)) appendValue(label);
    else if (["+", "−", "×", "÷"].includes(label)) appendOperator(label);
    else if (label === "C") clear();
    else if (label === "←") backspace();
    else if (label === ": to .") convertValue();
    else if (label === "=") evaluate();
  });
}

function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  navigator.serviceWorker.register("./sw.js").catch(() => {
    $("#installState").textContent = "Online preview";
  });
}

wireTabs();
wireCoordinates();
wireFuel();
wireTime();
registerServiceWorker();

window.FlightUtility = {
  parseCoordinateText,
  formatCoordinateOutputs,
  convertFuelValues,
  evaluateDurationExpression,
  decimalHoursToHhmm,
  formatDecimalHours,
};
