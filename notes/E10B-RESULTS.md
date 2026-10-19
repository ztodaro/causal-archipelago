# E10b Results — the conatal fraction of comoving pairs falls with age: DECAY DETECTED (Amendment 1); frozen run UNRESOLVED

Date: 2026-09-01. Spec E10B-SPEC.md frozen at `d91ac5f`; frozen-run
script e10b_run.py (SHA-256 3c19814…da4d) run once → UNRESOLVED
(committed 5c78756). Amendment 1 (E10B-AMENDMENT-1.md, frozen at
`33e6723`; script e10b_a1_run.py, SHA-256 9aa642a2…d876) run once →
DECAY DETECTED. Both are reported here; neither replaces the other.
Lane: Fable 5.1 at owner instruction; Codex remains technical owner of
record and is invited to reproduce (deterministic seeds).

## Sample

E1c's GALAH C4 pairs (874 treatment pairs with full-orbit controls;
replay gate PASS: 874 / 7,197 / medians 0.1042 / 0.1589 reproduced
exactly). 473 pairs have two valid [Y/Mg] clocks. Median pair age
4.4 Gyr, median pair-age error 2.7 Gyr. Pairs with age-posterior
mass > 0.5: 242 young (< 4.5 Gyr), 231 old (≥ 4.5 Gyr) — floor of 60
met. Median per-pair [Fe/H] measurement width 0.085 dex (all stars
carry e_fe_h).

## Frozen run (e10b_run.py) — UNRESOLVED, on the record

Oracle 1 pass (observed treatment median 0.1138, simulated 0.1095).
Oracle 2 pass as written (coverage 0.99–1.00). Decision fit:
f_young = 0.56, f_old = 0.02, sigma_c = 0.083; two-bin log-likelihood
407.9 vs constant-f 399.7 (delta 8.2). Bootstrap intervals vacuous
(f_young [0, 1]; f_old [0, 0.32]; R [0, > 10^5]) → **UNRESOLVED**
under the frozen rule. Cause, from the saved draws: sigma_c free with
a 0.5 dex bound ran degenerate in 14% of replicates (10% at the
bound). The frozen oracle's coverage criterion was satisfied by
vacuous intervals — a design flaw disclosed in Amendment 1.

## Amendment 1 (e10b_a1_run.py) — DECAY DETECTED

Change: per-pair conatal width sigma_c,i = sqrt(e_a² + e_b² +
sigma_int²), sigma_int bounded [0, 0.05] dex; oracle 2 adds
interval-width (≤ 0.6) and false-positive (≤ 10%) criteria.

Oracles: 1 pass (0.1138 observed vs 0.1107 simulated; constant-f fit
0.29). 2 pass: coverage 0.99/0.995 (exponential injection) and
0.995/1.00 (constant); median interval widths 0.52/0.23 and
0.54/0.50; false-positive rate 0.5%; power against the steep
injection (f0 = 0.6, tau = 1.5 Gyr) 35% — the test is conservative.

| quantity | estimate | 95% (star-clustered bootstrap ×500) |
|---|---|---|
| f_young, pairs < 4.5 Gyr | **0.58** | [0.29, 0.84] |
| f_old, pairs ≥ 4.5 Gyr | **0.02** | [0.00, 0.32] |
| R = f_old / f_young | **0.03** | [0.00, 0.73] |
| sigma_int (intrinsic conatal scatter) | 0.00 | [0.00, 0.05] |
| log-likelihood, two-bin vs constant-f | 408.7 vs 400.1 | delta 8.6 |
| parametric f0 · exp(−t/tau): f0, tau | 0.61, 5.5 Gyr | tau [2.3, 26.4] |
| descriptive four bins f_[0,2), f_[2,4.5), f_[4.5,8), f_[8,14) | 0.55, 0.55, 0.09, 0.00 | wide; see e10b_a1_results.json |

R's interval lies entirely below 1 and does not lie entirely above
0.5 → **DECAY DETECTED**.

## Reading, both directions

- The conatal fraction of kinematically linked pairs is not constant
  in age. Pairs younger than ~4.5 Gyr are, at the lower bound the
  orbit-matched template provides, mostly siblings (0.58, interval
  0.29–0.84); pairs older than that are consistent with almost none
  (point 0.02, upper bound 0.32). The constant-fraction model is
  disfavoured by 8.6 in log-likelihood.
- This overturns E10's "persistence in point estimate through 8 Gyr"
  reading, and does so for the reasons flagged before the run: E10
  compared age-selected treatment pairs with unselected, non-orbit-
  matched controls, and its 2.4–2.7 Gyr clock errors leaked young
  pairs into the old bin. E10's frozen verdict ("FORGETTING
  DETECTED") was right; its honest-reading caveat was the artefact.
- Against the published target: Kamdar 2019 Fig. 4 has conatal
  comoving pairs originating from clusters mostly younger than 1 Gyr.
  The direction agrees; the timescale is not resolved here (tau
  between ~2 and ~26 Gyr at 95%; the four descriptive bins put the
  drop between 4.5 and 8 Gyr, but with 2.7 Gyr age errors a
  concentration below 1 Gyr is only detected 35% of the time). So:
  consistent with Kamdar, not a sharp test of his steepness.
- sigma_int = 0 means the conatal pairs' [Fe/H] differences are
  fully explained by the catalogue errors — intrinsic sibling
  homogeneity is below GALAH's ~0.06 dex per-star precision, as
  open-cluster and wide-binary studies report.
- Caveats in force: lower-bound nature of f (stream siblings in the
  orbit-matched template); one survey (GALAH), 473 pairs; the [Y/Mg]
  clock applied without a Teff/log g validity cut beyond GALAH flags;
  ages beyond ~8 Gyr from this clock are unreliable and were pooled
  into the old bin; the amended width model is bounded, not fitted
  free (the bound is what makes f identifiable).

## Licensed and not licensed

Licensed: the table above with its intervals; "the conatal fraction
of Gaia comoving pairs at 20 pc / 3 km/s declines with age, from
~0.6 below 4.5 Gyr to < 0.32 above, against an orbit-matched chance
template"; the retraction of E10's persistence reading. Not licensed:
a decay timescale (tau's interval spans an order of magnitude); any
statement about Kamdar's < 1 Gyr steepness; any external statement
before the Atlas Deep Check on ST-20260901-002 (two blind lanes)
and, ideally, an APOGEE [C/N] lane under its own calibration spec.

## Consequences

E10-RESULTS.md receives an appended correction pointing here (the
frozen E10 text is unchanged). Paper II's chemistry section: the E1c
C4 excess and the age-resolved conatal fraction together replace the
E1b/E10 magnitudes for forward use. DR4 bundle item B3 takes
f = 0.29 (constant-f, all ages) and f_young = 0.58 as its inputs.
Deviations from the frozen spec: none in either run; Amendment 1
was filed, committed and hashed before its run.

## Correction appended 2026-09-01 (Frontier Atlas Deep Check, two blind lanes; union report frontier-atlas/intake/DEEP-CHECK-2026-09-01-AGE-CONATAL-DECAY-UNION.md)

Two corrections to this memo's framing; the numbers stand.
1. E10b measures purity, P(conatal | selected as comoving, age), not
   survival, P(selected | conatal, age). Only the second is a
   disc-scrambling clock, and the two differ through age-dependent
   birth rates, chance-pair population, cluster-mass weighting,
   survey selection and siblings already scattered out of the
   sample. The parametric tau = 5.5 Gyr is therefore not a physical
   timescale and must not be described as one; the "Reading" above
   that called this a handle on how fast the disc scrambles pairs is
   withdrawn. The bridge, if wanted, is a truth-labelled clustered-
   disc simulation pushed through the identical GALAH cuts, actions,
   chemistry/error and age-error model, with both quantities computed
   and the observable fitted by this same estimator (union report
   §A).
2. Kamdar 2019 Fig. 4 is the age distribution of simulated pairs
   already known to be conatal and selected, not a conatal-fraction-
   versus-age curve; it supports the qualitative young-skew and
   cannot be compared with the two-bin fraction without reprocessing
   the simulation through the same observable. "Consistent with
   simulated age-dependent dispersal" is the licensed phrase; "test
   of Kamdar's prediction" is not.
Classification: broad mechanism ANTICIPATED; E10b (and an APOGEE
[C/N] replication, e.g. under a frozen Spoo et al. 2022 calibration
with C and N kept out of the chemistry outcome) AS-APPLICATION,
exact implementation unlocated; physical survival curve
SUBSTRATE-IMPLIED. Externally defensible claim, adopted: "Within the
frozen GALAH comoving-pair selection and stated age/chemical model,
the inferred conatal mixture weight is centred lower above 4.5 Gyr
than below it, consistent with simulated age-dependent dispersal of
birth associations; it does not estimate a survival fraction or a
scrambling timescale." No new Atlas question; stays under OQ-0005.
