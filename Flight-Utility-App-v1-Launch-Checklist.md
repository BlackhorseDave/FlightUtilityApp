# Flight Utility App — Version 1.0 Master Launch Checklist
Updated: 2026-10-25. Publisher target: Blackhorse Creations Inc., subject to verified organization enrollment.

## Status rules
Complete = evidence exists for the specific item, not full commercial readiness.
In Progress = implementation or earlier work exists; release verification remains.
Blocked = a named prerequisite is missing.
Not Started = no evidence of work is available. This may change when Dave provides confirmation.
No application code or GitHub files were changed during this review.

## Evidence and baseline
The following baseline describes the October 11 initial review and is historical. Current development uses the capacitor-setup branch; the latest verified pushed checkpoint is 9b751ed (October 25). Later implementation, fixes and test evidence are recorded in Progress below.
Reviewed GitHub default-branch latest commit 260163bef6b5d2d99cc28cc170e5af03cf020856, dated October 10, 2026: “Remove ForeFlight coordinate output and update cache to v21.”
Read index.html, app.js, sw.js, manifest.webmanifest, README.md and the lib directory.
Repository: https://github.com/BlackhorseDave/FlightUtilityApp
Historical checkpoints confirm parser/offline geodesy hardening (August 27), custom keypad/copy buttons (September 11), overflow-minute handling (September 16).
Current source includes local WGS84 UTM calculations and local lib/mgrs.js. sw.js caches the library and application files, using flight-utility-pwa-v21.
Earlier user reports confirm successful testing, but are not a complete release acceptance record for this exact commit.
The PWA's deployed bytes, physical-device behavior, and calculation accuracy were not independently validated in this initial checklist review.
No native project or package.json appears in the repository root.
D-U-N-S receipt is user-confirmed historically; matching it to the incorporated entity is unverified.
October incorporation application activity is known; no incorporation certificate or developer account approval is available as evidence.

## Phase 1 — Version 1.0 feature freeze
| Item | Status | Evidence / next requirement |
|---|---|---|
| Initial source and history review | Complete | Current source and latest commit reviewed; device review still required below. |
| Time, fuel and coordinate functions implemented | Complete | Present in current app.js and interface; implementation is not accuracy sign-off. |
| Custom coordinate keypad, copy buttons, ForeFlight removal | Complete | Current interface and commit history confirm. |
| Bug inventory and prioritization | In Progress | Baseline defects and subsequent fixes/retests recorded in Progress. Remaining concerns include failed-update behaviour, independent coordinate accuracy and MGRS geometry, final limitations wording, and device/native verification. |
| Essential time and fuel calculations verified | In Progress | T01–T16 and F01–F14 baseline tests recorded; division-by-zero wording and fuel input/Clear fixes passed local retests. Final regression on the release build and phone verification remain pending. |
| Independent coordinate accuracy verification | In Progress | Earlier boundary tests exist; validate against independent authoritative conversion references with agreed tolerances. |
| Invalid, unusual and edge input tests | In Progress | C01–C41 baseline tests and local retests of coordinate input, UTM/MGRS validation, non-finite values and division-by-zero handling recorded in Progress. Independent MGRS cell geometry and zone-boundary checks, plus final release regression, remain pending. |
| PWA offline operation verified | In Progress | Local desktop offline reload and calculations passed; incomplete-cache, timeout, v24 cache-version mismatch and recovery checks passed. Actual failed-update testing, published PWA verification and phone airplane-mode close/reopen tests remain pending. |
| Cockpit readability and usability review | In Progress | Existing refinements; assess glare, contrast, font size, touch targets, orientation and long outputs on devices. |
| Remove development wording and clutter | In Progress | Initial coordinate placeholders, runtime availability wording, README and manifest description updated. Final wording review of generated web and native builds remains pending. |
| Confirm essential feature freeze | In Progress | Recommend retaining current utility scope; Dave's review pending. |
| Stable Version 1.0 Git checkpoint | Blocked | Development checkpoint 9b751ed pushed on capacitor-setup. Final release checkpoint awaits independent accuracy checks, release-build regression and required device/offline verification; no Version 1.0 release tag created. |
| Library provenance and commercial license check | In Progress | Bundled MGRS source matched to upstream revision; attribution and full MIT notice added and verified in local offline cache. Notice inclusion in generated web and final native distributions remains pending. |
| Aviation assumptions and limitations | In Progress | README documents fixed fuel densities, conversion constants, WGS84 assumptions, display precision, supported formats and coverage. Independent validation of density assumptions and coordinate accuracy, plus final in-app limitations review, remain pending. |

## Initial release concerns
These concerns describe the initial review. Several have since been resolved; see the Progress record and updated Phase 1 statuses for completed fixes and remaining verification.
- Pending-geodesy text is hard-coded in index.html and also restored on Clear/error in app.js. It can appear in a packaged app unless adjusted; packaging does not remove strings automatically. This is wording cleanup, not evidence geodesy is absent.
- Fuel volume/mass conversions use fixed assumed densities: Jet A 0.80, Avgas 0.72, regular gasoline 0.74, diesel 0.84 kg/L. They are estimates; the interface currently has no density limitation explanation.
- “Offline ready” is initially displayed before successful caching is confirmed. Verify this claim matches actual readiness.
- Test whether editing a coordinate leaves old successful output available to copy before reparsing. Evaluate stale fuel outputs after fuel-type changes, negative fuel values, repeated calculator operations, and rounding carry.
- Validate invalid UTM zone/band combinations and MGRS digit/grid validity rather than relying only on shape checks.
- README still claims UTM/MGRS are unimplemented; this conflicts with current code.
These are review items, not a claim that every item is a confirmed calculation bug.

## Phase 2 — Shared business and developer accounts
| Item | Status | Evidence / dependency |
|---|---|---|
| Verify incorporation approval and exact legal name | Complete | Dave confirmed receipt of the Manitoba incorporation certificate for Blackhorse Creations Inc. |
| D-U-N-S number obtained | In Progress | Earlier number reported; updated corporate D-U-N-S record was pending at last confirmation. Receipt and matching corporate details still require confirmation. |
| Match D-U-N-S entity name/address to corporation | In Progress | Incorporation confirmed; updated D&B record for Blackhorse Creations Inc. was pending at last confirmation. Verify matching legal name and address before organization enrollment. |
| Company website and business contact details | Not Started | Public functional corporate site and domain email needed for Apple organization enrollment. |
| Apple Developer organization enrollment | Blocked | Legal entity, matching D-U-N-S, authority and company website/contact prerequisites. |
| Google Play organization registration | Blocked | Verified organization identity and D-U-N-S prerequisites. |
| Tax, banking, paid-app agreements/payment profiles | Blocked | Verified company and developer/merchant accounts required. |
| Identify fees and budget | In Progress | Apple US$99/year; Google US$25 once, plus domain/email, Mac access and store sales fees to assess. |
Shared with English Practice Companion: incorporation, D&B identity, corporate domain/email, developer accounts and business payment setup.

## Phase 3 — Native application preparation
| Item | Status | Dependency |
|---|---|---|
| Compare Capacitor and suitable alternatives | Complete | Approach reviewed and Capacitor selected. Reconsider only if a demonstrated release blocker requires it. |
| Select simplest reliable approach | Complete | Capacitor selected to package the existing HTML/CSS/JavaScript app while preserving the PWA. Setup work is recorded on capacitor-setup; native build and release acceptance remain separate checks. |
| Identify and make necessary PWA adaptations | In Progress | Capacitor configuration and prepare-web.cjs exist. Current root-file fixes have not yet been copied into www. Native service-worker behaviour, clipboard, navigation and safe-area handling still require review and testing. |
| Preserve native offline operation | Not Started | Bundle assets locally; test first launch without a connection, not only previously cached use. |
| Native icons, splash screens, identifiers and permissions | Not Started | Existing SVG PWA icons are source assets, not verified store-ready assets. |
| Android build and signing configuration | Not Started | Select packaging; meet current target API requirements; preserve signing credentials. |
| iOS build and signing configuration | Blocked | Build approach, compatible Mac/Xcode access and enrollment/distribution credentials. |
| Choose Mac/rental/cloud build route | Not Started | Check current Xcode/macOS compatibility and costs before purchase/rental. |
| Physical Android and iOS native tests | Blocked | Signed test builds required; browser tests do not satisfy this item. |
| Apple and Google minimum-functionality review | In Progress | Official policies checked; approval is not guaranteed by a wrapper. |
| Final native dependency/privacy review | Not Started | Confirm libraries, permissions, privacy manifests where applicable, and data behavior. |

## Phase 4 — Website and commercial setup
| Item | Status | Dependency |
|---|---|---|
| Dedicated product domain | Not Started | Choose after checking availability; corporate domain is a separate shared need. |
| Simple professional landing page | Not Started | Accurate existing features only. |
| Actual application screenshots | Not Started | Capture final release build; do not invent screens. |
| Privacy policy and support contact | Not Started | Match final app behavior and publisher identity; host public policy. |
| One-time purchase price | Not Started | No confirmed Flight Utility price; do not copy the English app's proposed price. |
| Store pricing and distribution regions | Blocked | Store accounts/app records and price decision. |
| Store links | Blocked | Listing URLs required. |
| Support and update procedures | Not Started | Working email, bug triage, release records, signing backup and periodic platform maintenance. |
A simple paid download through the stores is the proposed starting point; separate web checkout is optional unless Dave chooses web sales.

## Phase 5 — Store submission
| Item | Status | Dependency |
|---|---|---|
| Google Play description and screenshots | Not Started | Final verified functions and Android screenshots. |
| Apple description and screenshots | Not Started | Final verified functions and iOS/iPad screenshots for chosen device support. |
| Age ratings, App Privacy and Data safety | Not Started | Declarations must match final packaged app and dependencies. |
| Aviation disclaimers and limitations review | Not Started | Accuracy evidence and documented assumptions first; a disclaimer does not cure incorrect calculations. |
| Internal/external testing and applicable requirements | Blocked | Accounts and native builds required; assess actual account requirements. |
| Submit Android | Blocked | Verified account, compliant signed build, listing, declarations and tests. |
| Submit iOS | Blocked | Verified account, compliant signed build, listing, declarations and tests. |
| Address review issues | Not Started | Conditional on review feedback. |
| Verify purchase, installation and offline operation | Blocked | Store-distributed releases needed; include fresh install and later update tests. |

## Phase 6 — Commercial launch
| Item | Status | Dependency |
|---|---|---|
| Publish product website | Blocked | Website and accurate links/content ready. |
| Confirm both listings live | Blocked | Store approvals and release actions. |
| Verify purchase/download flow | Blocked | Live listings and supported regions. |
| Confirm support/update instructions | Not Started | Test contact channel and establish release procedure. |
| Establish Version 1.1 backlog | Not Started | Put optional improvements here rather than delaying 1.0. |
| Declare Version 1.0 launched | Blocked | Both stores, website, purchase/install/offline verification and support operational. |

## Official requirements checked October 11, 2026
- Apple organization enrollment requires a legal entity, matching D-U-N-S, authority to bind the organization, domain-associated work email and a functional public organization website. Membership is US$99 per year, with regional pricing.
  https://developer.apple.com/programs/enroll/
- Google organization enrollment requires organization identity details and D-U-N-S. Registration is US$25 once.
  https://support.google.com/googleplay/android-developer/answer/13628312
  https://support.google.com/googleplay/android-developer/answer/6112435
- Google's 12 testers for 14 continuous days rule is specifically for new personal accounts created after November 13, 2023; do not automatically apply it to the planned organization account. Real device testing remains essential.
  https://support.google.com/googleplay/android-developer/answer/14151465
- Apple guideline 4.2 expects adequate utility beyond a repackaged website. Google's functionality rules prohibit limited or broken functionality. Existing useful offline utilities are a basis for review, not an approval guarantee.
  https://developer.apple.com/app-store/review/guidelines/
  https://support.google.com/googleplay/android-developer/answer/9898783
- Apple currently requires Xcode 26 or later with iOS/iPadOS 26 SDK for uploads. This build SDK requirement does not mean every customer needs iOS 26.
  https://developer.apple.com/news/upcoming-requirements/
- Google currently requires new phone apps to target Android 16 (API level 36) or higher. Recheck when configuring and submitting builds; target API is separate from the oldest supported Android version.
  https://support.google.com/googleplay/android-developer/answer/11926878?hl=en
- Google requires Data safety and a privacy policy even when an app collects no user data, except applicable internal-only testing exemptions. Assess the final package rather than assuming from the PWA.
  https://support.google.com/googleplay/android-developer/answer/10787469?hl=en-GB

## Critical path
Business: incorporation confirmation → matching D&B record + corporate website/email → organization accounts → paid-app agreements and banking.
Product: exact-build acceptance tests → required fixes and limitations → stable checkpoint → native packaging → physical-device acceptance.
Both paths join at store submissions → approvals → live purchase/offline verification → product website launch.
The corporate site belongs early because Apple enrollment needs it; the product site can be developed later.

## First practical step
Incorporation is confirmed. Continue release verification from the latest pushed capacitor-setup checkpoint, using the Progress record to avoid repeating completed work.

Remaining product work includes independent coordinate accuracy and MGRS geometry checks, final regression testing, failed-update behaviour, preparing and verifying www assets and license notices, and physical-device/native offline testing.

Confirm the updated corporate D-U-N-S record when available, then continue organization enrollment prerequisites.

Proceed one small step at a time; wait for Dave's confirmation before moving to another task.

## Progress record
2026-10-11: Established checklist, reviewed current repository baseline and official enrollment/review requirements. No application changes, commits, tags, purchases or enrollments made.
Next: Dave reviews checklist and confirms incorporation status.
Recommended Git checkpoints: current v21 baseline retained; acceptance-tested feature freeze; first working native build; store-submitted release; approved Version 1.0 release tag. Do not label untested builds as final.

2026-10-22 — Release testing, published PWA with v21 cache

Time tests T01–T16: expected calculations, overflow minutes, conversions, error recovery, negative durations and editing passed. Division by zero is rejected, but incorrectly reports “Invalid time format.”

Fuel tests F01–F14: basic conversions passed for all four fuel types and all five starting units. Confirmed defects: changing fuel type leaves stale results and success status; recalculation rejects its own populated outputs; editing quantities, including arrow adjustments, leaves stale results; negative quantities are accepted. Requested behaviour: remember the active input, automatically recalculate after quantity or fuel-type changes, and display one decimal place while retaining internal precision.

Coordinate tests C01–C41: supported angular formats, rounding carry, poles and coverage-boundary behaviour checked. Confirmed defects: editing leaves old results available to copy; short UTM northings are rejected unless padded; invalid zone/band combinations and band/northing mismatches are accepted; mathematical minus “−” and space-separated signed decimal pairs are rejected; Clear and errors restore development wording. Error-message consistency and MGRS coverage wording need cleanup.

Independent coordinate accuracy verification, offline readiness checks, README and limitations documentation, MGRS license review, fixes and regression testing remain outstanding. No application code changes or new Git checkpoint made during these tests.

2026-10-23 — Fuel input fixes and local verification

Updated wireFuel() to remember the active input and its unrounded value, automatically recalculate after quantity or fuel-type changes, display converted outputs to one decimal place, reject negative quantities, and reset remembered input on Clear. The field being edited retains the user’s entered text.

node --check app.js passed. Local Chrome tests at http://127.0.0.1:8001/ passed R01–R09: automatic calculation, arrow adjustments, switching input units, negative rejection, zero recovery, Clear/reset, repeated Calculate, deleting input, and preserving volume or mass when changing fuel type.

Phone testing and broader release checks remain outstanding. Published PWA and generated www assets have not been updated.

2026-10-23 — Stale coordinate results fix and local verification

Updated wireCoordinates() so direct typing, keyboard deletion/paste, custom keypad entry/backspace, and the app's PASTE button clear previous results and reset status to Ready. PASTE now waits for PARSE rather than automatically converting. Clear and failed parsing leave every output as a dash. COPY leaves the clipboard unchanged when outputs are cleared.

node --check app.js passed. Local browser tests at http://127.0.0.1:8001/ passed: typing invalidation, stale-copy prevention, custom keypad entry, custom backspace, app PASTE, Ctrl+V, Clear, invalid-input parsing, recovery with valid input, copying fresh results, and physical-keyboard Backspace.

Changes reviewed in GitHub Desktop and confirmed confined to wireCoordinates(). Phone testing, published PWA updates, and generated www assets remain outstanding.

Follow-up: the pushed fuel Clear handler appears inconsistent with the earlier reset requirement; inspect and retest before release. Other outstanding release work remains unfinished.

2026-10-23 — Fuel Clear correction

Confirmed that Clear emptied the active field but repopulated other fields using the remembered quantity. Corrected the fuelClear handler to empty all five fields, reset activeInput and activeValue to null, and set status to Ready.

node --check app.js passed. Local browser retests passed: Clear leaves all fields empty; changing fuel type after Clear leaves them empty; Calculate after Clear reports "Enter exactly one fuel value"; entering a fresh quantity resumes automatic conversion.

This resolves the fuel Clear follow-up recorded above. Published PWA and generated www assets remain unchanged. Other release work remains outstanding.

2026-10-23 — Short UTM northing input fix

Updated parseUtm() to accept northings containing 1–8 digits, allowing zero and short values without leading-zero padding. Existing numeric range validation remains in place.

node --check app.js passed. Local browser tests passed: northing 0 accepted; northing 123 accepted; padded 0000123 produces the same result; northing 10000001 rejected with cleared outputs.

UTM zone/band combinations and band/northing consistency remain unresolved. These tests verify input handling, not independent coordinate accuracy. Published PWA and generated www assets remain unchanged.

2026-10-23 — Mathematical minus in coordinate input

Updated parseCoordinateText() to normalize mathematical minus “−” to standard minus "-" before parsing.

node --check app.js passed. Local browser tests passed for mathematical minus on longitude, mathematical minus on both coordinates, rejection of latitude −91, and ordinary-minus input. Decimal pairs were tested with a comma separator; a comma was inserted using the physical keyboard where needed.

Space-separated decimal pairs remain unresolved. Published PWA and generated www assets remain unchanged.

2026-10-23 — Space-separated decimal coordinate input

Updated parseDecimalDegrees() to accept either a comma or whitespace between the two decimal coordinates.

node --check app.js passed. Local browser tests passed: space-separated coordinates; space-separated coordinates with mathematical minus signs; rejection of an extra third number; existing comma-separated input; rejection of latitude 91.

UTM zone/band validation and other release checks remain outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — Invalid UTM grid-zone combinations

Updated utmToLatLon() to reject the nonexistent grid-zone combinations 32X, 34X, and 36X.

node --check app.js passed. Local browser tests passed: 32X, 34X, and 36X rejected with cleared outputs; valid 33X and 32V inputs still accepted.

Band/northing consistency and other coordinate validation remain outstanding. These checks do not establish independent coordinate accuracy. Published PWA and generated www assets remain unchanged.

2026-10-23 — UTM latitude-band consistency and coverage boundaries

Updated utmToLatLon() to reject calculated latitudes outside the supplied band, allowing a tolerance of 0.00001 degrees (approximately 1.1 metres) for rounded input. Accepted rounding overshoots at 80°S and 84°N are clamped to the exact coverage boundary.

node --check app.js passed. Local tests covered northern and southern band mismatches, valid N/L/X inputs, and rounded input near the 8°N band boundary.

Testing exposed an accepted southern boundary input that produced a coverage error in the output formatter. After correction, both 80°S and 84°N boundary inputs produced UTM and MGRS values. Inputs beyond tolerance at both coverage limits were rejected. Final band-mismatch regression passed.

Independent coordinate accuracy, remaining parser validation, and other release checks remain outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — Division-by-zero message

Updated the calculator to report "Cannot divide by zero" for a zero divisor. The evaluate() error handler now displays the supplied error message, retaining "Invalid time format" for malformed expressions.

node --check app.js passed. Local browser tests passed: 8 ÷ 0 and 0 ÷ 0 show the specific error; Clear followed by 8 ÷ 2 returns 4 successfully; incomplete expression 8 + retains "Invalid time format".

Other release work remains outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — Initial coordinate display wording

Replaced the initial UTM and MGRS "Browser build: pending geodesy support" text in root index.html with dashes.

Local browser tests passed: initial coordinate display shows dashes; parsing valid coordinates still produces UTM and MGRS values with successful status.

Runtime geodesy error wording and other release work remain outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — Runtime coordinate availability wording

Changed STATUS_BROWSER_GEODESY_PENDING's displayed text from "Browser build: pending geodesy support" to "Coordinate conversion unavailable". The constant name and conversion logic remain unchanged.

node --check app.js passed. Local browser regression passed: valid input produces UTM and MGRS results with successful status. The unavailable-library path was not exercised.

Other release work remains outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — MGRS numeric digit-count validation

Updated parseMgrs() to require 2, 4, 6, 8, or 10 numeric digits after the grid-square letters, rejecting unequal easting/northing precision.

node --check app.js passed. Local browser tests passed: three-digit and nine-digit inputs rejected with cleared outputs; two-digit, four-digit, and ten-digit inputs accepted as MGRS.

MGRS zone/grid-letter validity and independent accuracy checks remain outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — MGRS zone and grid-letter validation

Added validation in parseMgrs() before calling the bundled library: zones must be 1–60; combinations 32X, 34X, and 36X are rejected; grid-column letters must belong to the zone's repeating column set; grid-row letters must be A–V excluding I and O. lib/mgrs.js remains unchanged.

node --check app.js passed. Local browser tests passed: zones 0 and 61 rejected; 32X, 34X, and 36X rejected; invalid column letters rejected in zones 31, 32, and 33; row W rejected; valid 31UDQ1234 accepted after the changes.

MGRS cell/band consistency, independent coordinate accuracy, and other release checks remain outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — MGRS cell/band consistency

Added a latitude-band overlap check using the cell bounds returned by the bundled library's inverse() function. Cells wholly outside the supplied band are rejected with "MGRS cell does not match band letter". A tolerance of 0.00001 degrees is allowed.

node --check app.js passed. Local tests passed: 31UDC1234 rejected; 31UDQ1234 accepted; boundary-overlapping 31VEC00 accepted; 31UEC01 rejected; southern mismatch 31LEC00 rejected; valid southern 31LEJ00 accepted.

This check relies on the bundled library's returned bounds. Independent verification of cell geometry, zone-boundary behaviour, and coordinate accuracy remains outstanding. Published PWA and generated www assets remain unchanged.

2026-10-23 — Non-finite coordinate validation

Added Number.isFinite() checks inside validateRange() to reject non-finite latitude or longitude values before ordinary range comparisons.

node --check app.js passed. Normal coordinate parsing regression passed. Direct browser Console tests passed: NaN latitude and Infinity longitude report "Invalid coordinate format"; longitude 181 retains "Longitude out of range".

Other release checks, independent accuracy verification, and offline readiness remain outstanding. Published PWA and generated www assets remain unchanged.

### October 25, 2026 — Local offline readiness verification

- Replaced the initial "Offline ready" label with "Checking offline readiness".
- Added a service-worker message check that confirms all listed app assets are cached before displaying "Offline ready".
- Added unavailable, incomplete-cache, and timeout status messages.
- Updated the service-worker cache from v21 to v22.
- Syntax checks passed for app.js and sw.js.
- At http://localhost:8001/ in normal Chrome, stopped the local server and reloaded successfully; status remained "Offline ready".
- With the server stopped, coordinate conversion including UTM and MGRS passed, Jet A 100 litres converted to 80.0 kg, and 1:30 + :45 returned 2:15.
- Offline reload and calculation checks also passed in Incognito.
- Local Python server required an explicit application/javascript MIME mapping for .js files.
- Unresolved: normal Chrome at http://127.0.0.1:8001/ continued reporting a text/plain service-worker MIME error despite curl confirming application/javascript. Cause remains unconfirmed.
- - Incomplete-cache test passed: removed the cached icon-512.svg entry and reloaded; the app displayed "Offline files incomplete".
- Recovery passed: unregistered the localhost service worker and reloaded with the server running; "Offline ready" returned.
- Timeout testing, published GitHub Pages verification, generated www assets, phone tests, and native-app offline verification remain pending.
- This is a local verification checkpoint, not release readiness approval.

- Timeout test passed: temporarily used an unanswered readiness request; after 10 seconds the app displayed "Offline readiness unconfirmed".
- Restored the original request, disabled DevTools "Bypass for network", and reloaded; "Offline ready" returned.
- Published GitHub Pages verification, generated www assets, phone tests, and native-app offline verification remain pending.

### October 25, 2026 — README refresh

- Updated the app description, Windows local-server command, port, and browser address.
- Documented current time, fuel, coordinate, and offline-status behaviour.
- Removed the obsolete claim that browser UTM/MGRS conversion is unimplemented.
- Clarified local-server limits, phone testing, pending release verification, and the unchanged published app and generated www assets.
- Reviewed the Markdown preview and README diff; formatting was readable.

### October 25, 2026 — Fuel conversion assumptions documented

- Documented the fixed densities used in app.js: Jet A 0.80, Avgas 0.72, Regular Gasoline 0.74, and Diesel 0.84 kg/L.
- Recorded the pound, US gallon, and Imperial gallon conversion constants.
- Clarified that density is not adjusted for temperature or a measured fuel sample.
- Checked the README preview; the density table displayed correctly.
- This documents the current implementation; independent validation of the density assumptions remains pending.

### October 25, 2026 — Coordinate assumptions documented

- Documented the WGS84 ellipsoid used for UTM calculations and the absence of datum transformations.
- Recorded display precision for DD, DDM, DMS, compact aviation DMS, UTM, and MGRS.
- Documented latitude/longitude limits, UTM-based coverage from 80°S to 84°N, and unsupported polar UPS coordinates.
- Clarified that display precision does not establish positional accuracy; independent accuracy verification remains pending.
- Reviewed the README preview; the coordinate table and coverage section displayed correctly.

### October 25 — MGRS attribution and offline notice verification

- Matched bundled `lib/mgrs.js` to proj4js/mgrs commit `249d933d2e336eebf4b8b6288eba8d4f2525f876`, accounting for removed export keywords, whitespace, and the Flight Utility browser wrapper.
- Added `THIRD-PARTY-NOTICES.md` containing the upstream copyright and full MIT license, which permits commercial use subject to its notice requirements.
- Added source attribution to `lib/mgrs.js`.
- Updated `prepare-web.cjs` to include the notice in future `www` preparation and report the file count dynamically.
- Added the notice to service worker cache v23.
- Syntax checks passed for `lib/mgrs.js`, `prepare-web.cjs`, and `sw.js`.
- Confirmed the notice appears in cache v23 and its full text can be retrieved with the local HTTP server stopped.
- Generated `www` assets, native packages, and published GitHub Pages remain unchanged. Inclusion of the notice in final distributions still requires verification.

### October 25 — Offline cache-version verification

- Added cacheName to both service-worker readiness responses.
- Updated app.js to require the expected v24 cache before displaying "Offline ready"; a missing or different cache name displays "Offline version unconfirmed".
- Updated the service-worker cache to v24.
- Syntax checks passed for app.js and sw.js.
- Normal localhost reload displayed "Offline ready", and cache v24 appeared in Chrome DevTools.
- With the local server stopped, reload passed and displayed "Offline ready".
- A simulated v23 readiness response displayed "Offline version unconfirmed"; offline reload restored "Offline ready".
- Restarted the local HTTP server after testing.
- This verifies response-version checking, not detection of every failed update. An older cached app may still confirm its own older cache. An actual failed-update test remains outstanding.
- Generated www assets, native packages, and published GitHub Pages remain unchanged.

### October 25 — Manifest description cleanup

- Removed development/testing wording from the root manifest description.
- Description now reads: "Offline coordinate, fuel, and duration calculator for pilots."
- JSON syntax validation passed.
- The manifest change has not yet been incorporated into a new service-worker cache or generated www assets. Published GitHub Pages and native packages remain unchanged.

### October 25 — Main checklist status reconciliation

- Updated selected Phase 1 rows to reflect completed fixes, documentation and local testing while retaining unfinished release checks.
- Marked the original baseline and initial concerns as historical.
- Recorded confirmed incorporation and the pending status of the updated corporate D-U-N-S record.
- Recorded Capacitor selection and existing preparation work.
- Replaced the outdated first practical step with current remaining work.
- Historical Progress entries remain unchanged. This review does not establish final release readiness.

### October 25 — Day/night display option and local verification

- Added a Day/Night mode button beside the offline-status label, with matching height and font size.
- Button text names the mode available to switch to.
- Theme preference is stored locally; switching remains available if preference storage fails.
- Added a night palette and adjusted tabs, calculator display, inputs, labels, Copy buttons and calculator keys for theme readability.
- Updated the service-worker cache and app's expected cache name to v27.
- Syntax checks passed for app.js and sw.js.
- Dave approved the night appearance across Time/Calculator, Fuel and Coordinates.
- With the server stopped, reload retained night mode, displayed "Offline ready", and allowed switching between day and night.
- Restarted the local HTTP server after testing.
- Update observation: v24 remained active while newer files were being tested. A manual worker update check followed by reload restored readiness for v26. The later v27 update required approximately seven reloads before readiness confirmed. Cause remains unresolved; this is not a clean update-path acceptance result.
- Physical-device readability, theme behaviour and native offline verification remain pending.
- Generated www assets, native packages and published GitHub Pages have not been updated as part of this work.

- Follow-up: corrected the header's closing div and placed the theme button and offline status together on a separate row below the title.
- Verified that a temporarily displayed longer offline message wraps within the header at narrow desktop widths; the mode button stays alongside it.
- Final cache and expected cache name updated to v28. Online reload returned "Offline ready".
- With the server stopped, final v28 offline reload preserved the header layout, returned "Offline ready", and allowed Day/Night switching.
- Restarted the local server after final testing.
- At an extremely narrow desktop width, the Coordinates tab label was clipped; physical-phone layout verification remains pending.

### October 27–28 — Published PWA device checks and Apple icon preparation

- Changed GitHub Pages source to capacitor-setup / (root); deployment succeeded.
- iPhone: Day/Night switching and preference persistence passed. In Airplane Mode, reload and sample time, fuel, UTM and MGRS calculations passed. Home Screen launch and fuel conversion also passed.
- iPad: Home Screen launch displayed full screen. Airplane Mode close/reopen, fuel conversion and UTM/MGRS output checks passed.
- These are basic PWA device checks, not independent coordinate accuracy or native-app acceptance.
- iPad Home Screen icon showed an F while iPhone showed the compass; cause remains unconfirmed.
- Created an opaque 180x180 compass PNG at icons/apple-touch-icon.png and updated the apple-touch-icon reference.
- Added the PNG to offline assets; cache and expected cache names are flight-utility-pwa-v29.
- app.js and sw.js syntax checks passed.
- Corrected an accidental extra character in the service-worker cache name after a version mismatch. Offline ready returned; server-stopped reload passed.
- Restarted the local server; Serving HTTP confirmed.
- PNG fix remains unpublished and unverified on iPad. Generated www assets and native packages remain unchanged.