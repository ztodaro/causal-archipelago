# E8 Follow-up Protocol — archival spectra census (frozen before querying)

Date: 2026-08-30. Purpose: determine whether existing public
high-resolution spectra can confirm or refute any of the top E8 GOLD
candidates without new observations. This census is a DATA-AVAILABILITY
step, intake-only. Targets: `e8_followup_targets.csv` (top 20 GOLD by
WMAD; rank 19 has a blank Gaia DR3 id from the disclosed DR2→DR3 join
gap — query it by coordinates and GALAH sobject_id).

## What counts as a usable spectrum (frozen criteria)

- Resolution R ≥ 40,000 (differential solar-twin abundances at the
  0.01-dex level; GALAH's own R ≈ 28,000 is what we are upgrading from).
- Optical coverage including ~4800–6800 Å (the Fe I/II + key-element
  line lists for differential analysis).
- Instruments in scope at ESO: HARPS (R≈115k), ESPRESSO (≈140k),
  UVES (≥40k settings only), FEROS (≈48k). X-shooter is out (R too low).
- Report SNR or exposure time as published; prefer SNR ≥ 50 per pixel
  but report everything ≥ threshold-R regardless of SNR.
- Solar reference: a same-instrument reflected-sunlight spectrum
  (asteroid/Moon) is required for differential work; HARPS and ESPRESSO
  archives are known to contain these — the census confirms availability
  rather than assuming it.

## Confirmation gate (binding)

If usable spectra exist for any candidate: NO abundance analysis, line
measurement, or spectrum download beyond checksum verification occurs
until an E8-CONFIRM spec is frozen and committed — defining the line
list, the differential method, the solar reference, the age indicators
(Li, [Y/Mg] at higher precision), and the pass/fail criterion for
"sibling" vs "analog". The E8 claim caps (28d308e) remain in force:
GOLD stars are candidates until that preregistered analysis, or an
equivalent independent one, says otherwise.

## Deliverable (agent)

`solar-siblings/data/e8_archival_census.csv` — one row per (candidate ×
dataset): rank, source_id, sobject_id, archive, instrument, R,
wavelength range, exposure/SNR, obs date, program ID, dataset ID,
public/proprietary flag. Plus PROVENANCE file with query details and
SHA-256. Empty result = valid result (reported as such).
