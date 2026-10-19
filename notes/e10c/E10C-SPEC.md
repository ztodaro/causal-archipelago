# E10c — APOGEE [C/N] giant-age replication of the E10b purity curve

**STATUS: NOT FROZEN, NOT RUN — INFEASIBLE AT THE POWER FLOOR.** See
E10C-FEASIBILITY.md. This spec is preserved as drafted so that the
design is on record for a survey that does contain comoving giant
pairs.

Drafted 2026-09-01. Motivation: the Deep Check literature review's
recommendation ("APOGEE replication — tests generality, not survival"). This is a
replication; it needs no novelty licence and makes no priority claim.

## Question

Does an independent survey, with an independent age clock, reproduce
the E10b ordering — the conatal mixture weight of present-day
comoving pairs is lower above 4.5 Gyr than below it — within the same
frozen model? It measures purity, P(conatal | selected, age), exactly
as E10b did; it says nothing about physical pair survival.

## Inputs (all in hand)

- Treatment pairs and chance template: E1c's APOGEE C4 pairs (919
  treatment pairs with full-orbit controls, S_min = 300 pc), recovered
  by replaying E1c's construction (seed 1701, bootstrap draws
  replayed) and gated on exact agreement with e1c_results.json
  (919 / 6,150 / medians 0.1047 / 0.1373).
- Chemistry outcome: |d[Fe/H]| from the E1b APOGEE file, as in E1c.
  Carbon and nitrogen are used only as the clock and never enter the
  outcome; [Fe/H] is the outcome in both E10b and E10c.
- Ages: the Spoo et al. 2022 APOGEE DR17 calibration,
  log[Age(yr)] = 10.14 + 2.23 [C/N], applied to both members from
  solar-siblings/data/e8_apogee_abund.csv (b3ee7b2) joined on exact
  integer-string GAIAEDR3_SOURCE_ID. Domain, per the calibration:
  log g < 3.3 and −0.53 ≤ [Fe/H] ≤ 0.31 for both members; C_FE and
  N_FE finite, non-sentinel, with positive errors, and with no ASPCAP
  ELEMFLAG bad bit set (bits 0–4 and 6; warning bits allowed —
  declared because the strict flag = 0 rule discards nearly all
  giants for warning-only reasons). Per-star log-age error
  sigma_log = sqrt(2.23² (e_C² + e_N²) + 0.10²), the 0.10 dex term a
  declared calibration-scatter floor (conservative against the
  paper's "trusted to 10%" statement); linear-age error
  sigma_t = t ln10 sigma_log. Pair age = inverse-variance mean, as in
  E10b. Ages outside the calibration's stated validity
  (8.62 ≤ log Age ≤ 9.82, i.e. 0.42–6.6 Gyr) are KEPT and counted:
  the two-bin test needs only the ordering that lower [C/N] means
  older, and clipping to the range edge would not move a star across
  the 4.5 Gyr boundary. The count of extrapolated members is reported.
- Per-pair [Fe/H] measurement width from FE_H_ERR (E1b APOGEE file),
  read without touching the E1b selection.

## Model, oracles, decision rule

Identical to E10b Amendment 1: half-normal conatal component with
per-pair width sqrt(e_a² + e_b² + sigma_int²), sigma_int in
[0, 0.05] dex; empirical chance histogram from the C4 controls pooled
by modal age bin; age error marginalised per pair through the bin
posterior masses; decision bins [0, 4.5) and [4.5, 14) Gyr;
descriptive four bins; star-clustered bootstrap ×500 (decision), ×300
(descriptive and parametric); oracle 1 (constant-f simulation
reproduces the observed treatment median within 0.01 dex); oracle 2
(injection, 200 realisations each of f = 0.6 exp(−t/1.5 Gyr) and
f = 0.35: coverage ≥ 0.90, median interval width ≤ 0.6, false-positive
rate ≤ 10%; power reported). Verdict on R = f_old / f_young: DECAY
DETECTED (interval entirely below 1), PERSISTENCE (entirely above
0.5), MILD DECAY (inside (0.5, 1)), UNRESOLVED otherwise;
UNDERPOWERED below 60 pairs with posterior mass > 0.5 in either
decision bin.

Replication criterion (pre-declared): E10c REPLICATES E10b if its
verdict is DECAY DETECTED or MILD DECAY; FAILS TO REPLICATE if
PERSISTENCE; INCONCLUSIVE if UNRESOLVED or UNDERPOWERED. All three
are reported as they fall.

## Pre-declared interpretation

Same lower-bound caveat as E10b (stream siblings in the orbit-matched
template). Giants only, so a different stellar population from
GALAH's dwarfs; agreement would show the purity ordering is not a
population artefact. Disagreement would not by itself decide which
survey is right. No timescale, no survival fraction, no Kamdar
comparison beyond "consistent with simulated age-dependent
dispersal".

## Execution

Disclosure: a synthetic-chemistry smoke run (plumbing and sample
counts only; f = 0.3 synthetic draws replace the treatment [Fe/H])
precedes the freeze and is committed as e10c_results_smoke.json; it
is not a result. Freeze this spec (commit hash), record the script
SHA-256, run e10c_run.py once. Outputs: e10c_results.json,
E10C-RESULTS.md, e10c-results.png. Deviations: none without a dated
amendment appended here.
