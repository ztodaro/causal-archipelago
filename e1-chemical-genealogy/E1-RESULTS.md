# E1 chemical genealogy — result: inconclusive at current power, direction suggestive

Date: 2026-08-30. Spec: E1-SPEC.md (a82ea9c, verified byte-identical before
running). Code: `e1_run.py` (operationalizations documented in header).
Data: frozen intake cb2db56. Output: `e1_results.json`.

## Verdict under the frozen decision rule

- **GALAH: INSUFFICIENT.** 912 clean unmasked stars yield only 3 treatment
  pairs. This is geometry, not chemistry: requiring BOTH members of a
  cheap-transfer pair to sit in the survey subsample scales as the square
  of the subsample fraction (~8×10⁻⁶ per pair × 912² / 2 ≈ 3).
- **APOGEE: directionally consistent, not significant.** 7,448 clean
  unmasked stars; 245 matched treatment pairs vs 2,445 matched controls.
  Median |Δ[Fe/H]|: treatment 0.160 vs control 0.281 — a −0.12 dex
  difference in the predicted direction — but the clustered bootstrap CI
  is [−0.23, +0.11] and Mann-Whitney p = 0.27. Under the frozen rule this
  is NOT a confirmation; treatment pairs share stars (a single co-moving
  clump contributes many pairs), so the effective independent sample is
  far smaller than 245, and the CI honestly reflects that.
- The frozen kill condition ("no effect in either survey") is NOT
  triggered: one survey could not test, the other points the right way
  without significance. Status: **underpowered-inconclusive**.

## Documented deviation

APOGEE clean rule corrected from ASPCAPFLAG==0 (over-strict: benign warn
bits excluded 97% of stars) to the intake's ASPCAP_STAR_BAD == 0 — which
is the literal reading of the spec's "bad bits unset". Recorded in the
script header; both runs preserved in the log.

## The design lesson (for E1b, to be frozen separately)

The 100 pc sample is the binding constraint, not the chemistry. The
powered version runs the identical pair test on the SURVEYS' OWN catalogs
(GALAH's ~million stars carry positions, proper motions, RVs, and
abundances natively out to a kiloparsec) — pair counts scale by ~10⁴.
That requires a new frozen spec and intake (E1b) and inherits this run's
calibration notes (RAVE metallicities excluded; star-clustered inference
mandatory; report effective independent clusters, not raw pair counts).

## Honest summary sentence

The first properly controlled test of chemical co-natality in the diffuse
transfer field returned a suggestive −0.12 dex similarity signal that
current sample geometry cannot confirm; the test design, not the
hypothesis, is what needs upgrading.
