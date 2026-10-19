# E10b — age-resolved conatal fraction of comoving pairs by mixture likelihood (frozen before execution)

Dated 2026-09-01; run only if E1c reports SURVIVES or SHRINKS in the
project verdict. The mixture-likelihood design and its oracle validation
adapt Boufourou (arXiv:2608.24556). Supersedes nothing: E10's frozen verdict
and its honest reading stand as history.

## Question and published target

Kamdar et al. 2019 (arXiv:1904.02159, Fig. 4) state that the clusters
giving birth to conatal comoving pairs are mostly younger than 1 Gyr,
so the conatal fraction of comoving pairs should fall steeply with
age. E10's point estimates persisted through 8 Gyr, but E10 used
per-bin medians against non-orbit-matched, non-age-selected controls,
with clock errors comparable to its bin widths. E10b measures f(age),
the conatal fraction of E1b's kinematically linked pairs, with the
orbit-matched chance template from E1c and the age error carried
inside the likelihood.

## Inputs (all in hand; no new retrieval)

- Treatment pairs: E1b GALAH treatment pairs (dx < 20 pc, dv < 3 km/s)
  that received C4 orbit-matched controls in E1c (S_min = 300 pc), with
  their C4 control pairs. Chemistry channel: |d[Fe/H]| as in E1b.
- Ages: the frozen [Y/Mg] clock, t = (0.170 - [Y/Mg]) / 0.0371 Gyr
  (Nissen 2016, as used in E8/E10), from solar-siblings/data/
  e8_galah_abund.csv.gz (b3ee7b2) joined on exact integer-string
  gaiadr3_source_id; both members must have flag_y_fe = 0 and
  flag_mg_fe = 0. Per-star age error sigma_t = sqrt(e_y_fe^2 +
  e_mg_fe^2) / 0.0371. Pair age t_i = inverse-variance mean of the
  members' ages, sigma_i accordingly. NO consistency cut on |dt|
  (E10's circularity): every pair with two valid clocks enters.
  Ages are clipped to [0, 14] Gyr for binning only.
- APOGEE is not used for ages here (no [Y/Mg]); an APOGEE [C/N]
  giant-clock lane would need its own calibration spec and is
  registered as a future amendment, not run.

## Model

For pair i with d_i = |d[Fe/H]|:
  L_i = f_i * h(d_i | sigma_c) + (1 - f_i) * g_b(i)(d_i)
- h: half-normal on d >= 0 with width sigma_c (one free parameter,
  common to all ages; absorbs intrinsic conatal scatter and
  measurement error).
- g_b: the chance density, an empirical histogram (0.02 dex bins, 0 to
  1.0 dex, floor 1e-3) of the C4 control-pair |d[Fe/H]| values pooled
  over all treatment pairs whose age posterior mass is mostly in age
  bin b. DECISION bins: two, b = [0, 4.5) "young" and [4.5, 14) "old".
  DESCRIPTIVE bins: four, [0, 2), [2, 4.5), [4.5, 8), [8, 14), fitted
  separately and reported without a verdict. (Pre-freeze design note:
  the smoke run showed a median pair-age error of ~2.7 Gyr and only
  49 pairs with posterior mass > 0.5 in [4.5, 8); the E10 three-bin
  layout would have been underpowered by the floor below, so the
  decision uses a young/old split at 4.5 Gyr — the boundary E10 used
  between its mid and old bins — chosen from sample sizes and errors
  alone, before any real chemistry-age fit was seen.) This keeps the
  chance template orbit-matched (E1c) and age-matched (by pooling).
- f_i = sum_b P(b | t_i, sigma_i) * f_b, with P the Gaussian
  posterior mass of the pair's age in bin b. This marginalises the
  age error instead of assigning pairs to bins, which is the
  deconvolution E10 lacked.
- Parameters (decision fit): f_young, f_old, sigma_c. Fit by maximum
  likelihood (bounded, multistart); 95% intervals by star-clustered
  bootstrap (x500, resampling stars as in E1b and refitting). The
  four-bin descriptive fit adds f per bin with x300 bootstrap.
- Secondary parametric fit: f(t) = f0 * exp(-t / tau), reported with
  tau's bootstrap interval; and a constant-f fit for comparison by
  log-likelihood difference.

## Oracle validation (must pass before any age-resolved number is read)

1. Constant-f fit reproduces E1c's C4 GALAH medians: simulate d from
   the fitted constant-f mixture (using the pooled chance histogram)
   and require the simulated treatment median to fall within +/-0.01
   dex of the observed C4 treatment median on the same pairs.
2. Injection: with the real ages, errors and control histograms,
   inject f(t) = 0.6 * exp(-t / 1.5) and f(t) = 0.35 constant, 200
   realisations each; the fitter must recover the two decision-bin f
   values within its own 95% intervals in >= 90% of realisations. Failure on either oracle
   stops the run with an UNVALIDATED report.

## Decision rule (frozen)

Ratio R = f_old / f_young = f_[4.5,14) / f_[0,4.5) (bootstrap
interval), read against Kamdar 2019's prediction of concentration
below ~1 Gyr:
- DECAY DETECTED: R's 95% interval lies entirely below 1.
- PERSISTENCE: R's 95% interval lies entirely above 0.5.
- UNRESOLVED: otherwise — reported as a bound on R, not as a null.
Both DECAY and PERSISTENCE can hold simultaneously only if the
interval sits inside (0.5, 1); that case is reported as
"MILD DECAY". Power floor: >= 60 pairs with age posterior mass > 0.5
in each of the two decision bins; below it the verdict is
UNDERPOWERED and the f table is descriptive.

## Pre-declared interpretation

- E1c's stream-sibling caveat carries over: orbit-matched controls
  may contain dispersed siblings, so f_b are lower bounds on the
  conatal fraction at every age; R is less affected because the bias
  applies to all bins.
- The [Y/Mg] clock is calibrated on solar-type dwarfs; pairs outside
  its validity (giants, very cool dwarfs) are not excluded here beyond
  the GALAH flags, and this is a recorded limitation, not tuned
  post hoc.
- DECAY at Kamdar's steepness would reconcile E10 and the simulation;
  PERSISTENCE would put the birth-memory timescale of the disc in
  tension with the simulated origin picture and would be the result
  to take to a Deep Check before any external statement.

## Execution

Disclosure: before the freeze, e10b_run.py was exercised once in
`smoke` mode, which replaces the treatment chemistry with synthetic
draws (f = 0.3, sigma = 0.06) so that plumbing and timing could be
checked without seeing any real age-resolved number; the smoke output
is kept as e10b_results_smoke.json and is not a result.

Freeze this spec (commit hash) before running e10b_run.py once in the
container holding the E1c outputs. Record script SHA-256. Outputs:
e10b_results.json, E10B-RESULTS.md, e10b-results.png. Deviations:
none without a dated amendment appended here.
