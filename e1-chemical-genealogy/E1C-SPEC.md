# E1c — Orbit-matched control amendment to E1b (frozen before execution)

Dated 2026-09-01. Nothing in E1b is edited; this is an amendment with
its own inputs-identical rerun.

## Question

E1b's controls (pairs with dv > 6 km/s, matched on Teff, log g,
separation and distance) are not matched on Galactic orbit. Comoving
pairs share an orbit by construction; same-orbit stars are chemically
similar without common birth (guiding-radius gradient; disc-population
coherence). How much of E1b's twin excess survives against controls
that share the treatment pair's orbit but are not comoving?

## Inputs (identical to E1b, no exceptions)

- e1-chemical-genealogy/data/e1b_galah.csv, e1b_apogee.csv,
  e1b_cg_members.csv (intake 83b59c4); the same masking catalogues;
  the same clean/unique-star selection; the same treatment definition
  (tree pairs within 25 pc; dx < 20 pc and dv < 3 km/s).
- Phase-space transform and constants as e1b_run.py.
- Actions: the E8 axisymmetric epicyclic function (e8_sieve.actions)
  with its frozen constants R0 = 8.2 kpc, VC = 233.1 km/s, solar
  motion (11.1, 12.24, 7.25) km/s, nu = 73.5 and kappa = 40.2
  km/s/kpc. Approximate, and applied identically to every star.

## Reproduce-first gate (C0)

The script first re-executes E1b's control construction and
statistics verbatim with E1b's seed (17). It must reproduce
e1b_results.json exactly (GALAH -0.1011 [-0.1203, -0.0825]; APOGEE
-0.1034 [-0.1186, -0.0883]; matched counts 1,288 / 4,461; controls
12,877 / 42,952; clusters 1,058 / 1,605). If C0 does not reproduce,
the run stops and nothing below is reported.

## Orbit tolerances (set from kinematics, before any chemistry is read)

tau_Lz, tau_Jz, tau_Jr = the 90th percentiles of |dLz|, |dJz|, |dJr|
over that survey's treatment pairs. Controls are therefore required to
be as orbit-similar to the treatment pair as the treatment pair's own
members are to each other. Values are recorded in the results and are
not adjusted after the run.

## Graded control tiers (new rng seed 1701; all tiers use the same
Teff +/-150 K and log g +/-0.3 per-star matching as E1b, and each
control star's heliocentric distance within 150 pc of the treatment
pair's mean distance; at most 10 control pairs per treatment pair)

- C1 — far, orbit-free: two stars each > S_min from the other and from
  both treatment stars; no action constraint. Tests whether spatial
  proximity alone (E1b's controls were within 25 pc of each other)
  carries chemical information.
- C2 — + |Lz - Lz_pair| <= tau_Lz for both control stars (guiding
  radius / gradient term).
- C3 — + |Jz - Jz_pair| <= tau_Jz (vertical action / disc-population
  term).
- C4 — + |Jr - Jr_pair| <= tau_Jr. **PRIMARY.** Full orbit match.

Lz_pair, Jz_pair, Jr_pair are the treatment pair's mean actions.
S_min = 300 pc for all decision-bearing quantities. C4 is additionally
reported at S_min = 100 pc and 1,000 pc as a sensitivity check only.

## Statistic, bootstrap, power

Exactly E1b's: median |d[Fe/H]| of matched treatment pairs minus
median of their control pairs; star-clustered bootstrap x1000 over the
union of stars in treatment and control pairs; Mann–Whitney one-sided
p. Power floor per survey per tier: >= 200 matched treatment pairs and
>= 30 effective treatment clusters; below the floor the tier is
reported descriptively and marked UNDERPOWERED. Tolerances are not
loosened post hoc; a relaxed rerun requires a new dated amendment.

## Decision rule (frozen; on C4 at S_min = 300 pc, per survey)

- SURVIVES: bootstrap 95% CI excludes zero AND the point estimate is
  at or below E1b's CI upper bound for that survey (GALAH <= -0.0825;
  APOGEE <= -0.0883).
- SHRINKS: CI excludes zero AND the point estimate is above that bound
  (a real but smaller excess).
- VANISHES: CI includes zero.

Project verdict = the weaker of the two surveys' tiers
(VANISHES < SHRINKS < SURVIVES). Both surveys and all tiers are
reported whatever the verdict.

## Pre-declared interpretation

- Members of one dissolved cluster spread along their orbit and would
  enter orbit-matched controls as true siblings. This biases C4 toward
  VANISHES, i.e. it is conservative against E1b. The orbit term
  inferred from C0 -> C4 is therefore an upper bound on orbit
  coherence in E1b's excess; the C4 excess is a lower bound on birth
  memory.
- SURVIVES: E1b's interpretation stands against the correct null.
  SHRINKS: birth memory is real; the E1b/Kamdar/Nelson magnitudes
  need an orbit-controlled restatement. VANISHES: E1b's interpretation
  is withdrawn and E10b is cancelled. Every outcome is reported in full.
- No external statement follows from this run until an independent
  literature check has completed.

## Execution

Run once, in the environment that holds the staged E1b inputs
(Python 3 + numpy/scipy). The script's
SHA-256 is recorded in the results. Outputs: e1c_results.json,
E1C-RESULTS.md, e1c-results.png. Deviations: none permitted without a
dated amendment appended to this file.
