# Flight Utility App — Version 1.0 Master Launch Checklist
Updated: 2026-10-11. Publisher target: Blackhorse Creations Inc., subject to verified incorporation and organization enrollment.

## Status rules
Complete = evidence exists for the specific item, not full commercial readiness.
In Progress = implementation or earlier work exists; release verification remains.
Blocked = a named prerequisite is missing.
Not Started = no evidence of work is available. This may change when Dave provides confirmation.
No application code or GitHub files were changed during this review.

## Evidence and baseline
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
| Bug inventory and prioritization | In Progress | Initial release concerns recorded below; reproduce before assigning confirmed defects. |
| Essential time and fuel calculations verified | In Progress | Prior working reports; exact-build expected/actual test record required. |
| Independent coordinate accuracy verification | In Progress | Earlier boundary tests exist; validate against independent authoritative conversion references with agreed tolerances. |
| Invalid, unusual and edge input tests | In Progress | Earlier parser tests; repeat release cases, including poles, zone edges, rounding, malformed UTM/MGRS, overflow and division by zero. |
| PWA offline operation verified | In Progress | Cache code includes local dependencies; airplane-mode close/reopen testing required on devices. |
| Cockpit readability and usability review | In Progress | Existing refinements; assess glare, contrast, font size, touch targets, orientation and long outputs on devices. |
| Remove development wording and clutter | Not Started | README is stale; initial/cleared UTM/MGRS fields show pending wording; manifest says testing. |
| Confirm essential feature freeze | In Progress | Recommend retaining current utility scope; Dave's review pending. |
| Stable Version 1.0 Git checkpoint | Blocked | Await acceptance tests and required fixes; current v21 commit is a baseline, not a release tag. |
| Library provenance and commercial license check | Not Started | Confirm mgrs source/version, license obligations and notices. |
| Aviation assumptions and limitations | Not Started | Document fixed fuel densities, WGS84 datum, precision, supported formats and UTM/MGRS coverage. |

## Initial release concerns
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
| Verify incorporation approval and exact legal name | In Progress | Application activity known; certificate/status confirmation needed. |
| D-U-N-S number obtained | Complete | Earlier user confirmation; no number needs to be shared in chat. |
| Match D-U-N-S entity name/address to corporation | Blocked | Confirm incorporation and D&B record; do not assume earlier sole-proprietor record is sufficient. |
| Company website and business contact details | Not Started | Public functional corporate site and domain email needed for Apple organization enrollment. |
| Apple Developer organization enrollment | Blocked | Legal entity, matching D-U-N-S, authority and company website/contact prerequisites. |
| Google Play organization registration | Blocked | Verified organization identity and D-U-N-S prerequisites. |
| Tax, banking, paid-app agreements/payment profiles | Blocked | Verified company and developer/merchant accounts required. |
| Identify fees and budget | In Progress | Apple US$99/year; Google US$25 once, plus domain/email, Mac access and store sales fees to assess. |
Shared with English Practice Companion: incorporation, D&B identity, corporate domain/email, developer accounts and business payment setup.

## Phase 3 — Native application preparation
| Item | Status | Dependency |
|---|---|---|
| Compare Capacitor and suitable alternatives | In Progress | Earlier conceptual discussions; no final selection. |
| Select simplest reliable approach | Not Started | Compare offline local-asset packaging, shared code, maintenance and review suitability. |
| Identify and make necessary PWA adaptations | Not Started | Decide packaging; audit service worker behavior, clipboard, navigation and safe areas. |
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
After checklist review, confirm whether the Manitoba incorporation certificate has arrived and the exact legal company name shown on it. No payment, banking or identity numbers are needed.
This resolves the earliest shared publishing dependency. If approval is still pending, the next agreed work session can focus on the v21 release acceptance tests.
Proceed one step at a time; wait for Dave's confirmation before moving to another task.

## Progress record
2026-10-11: Established checklist, reviewed current repository baseline and official enrollment/review requirements. No application changes, commits, tags, purchases or enrollments made.
Next: Dave reviews checklist and confirms incorporation status.
Recommended Git checkpoints: current v21 baseline retained; acceptance-tested feature freeze; first working native build; store-submitted release; approved Version 1.0 release tag. Do not label untested builds as final.

