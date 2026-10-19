# E10b — Amendment 1 (dated 2026-09-01; appended, the frozen spec and its run are unchanged)

Lane: Fable 5.1 at owner instruction. Filed after the frozen run at
d91ac5f (script 3c19814…) completed and reported UNRESOLVED.

## What the frozen run found, and why it could not decide

Both oracles passed as written. The decision fit gave f_young = 0.56
(pairs younger than 4.5 Gyr) and f_old = 0.02, with the two-bin model
preferred over a constant conatal fraction by 8.2 in log-likelihood
(two-bin 407.9 vs constant 399.7; parametric tau = 5.5 Gyr). The
star-clustered bootstrap, however, returned vacuous intervals
(f_young [0, 1], f_old [0, 0.32], R [0, >10^5]), so the frozen rule
returns **UNRESOLVED**, and that verdict stands on the record.

Diagnosis, from the saved bootstrap draws: the conatal width sigma_c
was a free parameter with an upper bound of 0.5 dex. In 14% of
replicates the optimiser ran sigma_c to >= 0.2 dex (10% to the
bound), where a wide "conatal" half-normal mimics the chance template
and f becomes unidentifiable; those replicates alone produce the
vacuous intervals. Conditioning post hoc on sigma_c < 0.2 would give
R's 97.5th percentile at 0.71 — but that conditioning is not
licensed by the frozen rule and is reported here only as the reason
for this amendment. A second, disclosed flaw: the frozen oracle 2
tested only interval coverage, which vacuous intervals satisfy
trivially (coverage 1.00 was the warning sign, not the reassurance).

## Changes (pre-declared before the amended run)

1. **Conatal width anchored to the catalogue errors.** For pair i,
   sigma_c,i = sqrt(e_a^2 + e_b^2 + sigma_int^2), where e are the
   GALAH e_fe_h values of the two members (read separately from the
   E1b file so the E1b selection is untouched; a missing value falls
   back to the survey median) and sigma_int is one free parameter
   bounded to [0, 0.05] dex — the intrinsic chemical scatter of
   conatal pairs, bounded at the level published open-cluster and
   wide-binary homogeneity studies report (<= 0.03–0.05 dex). The
   bound is the identifiability constraint; it is declared here, not
   tuned.
2. **Oracle 2 gains three criteria** (injection with true
   sigma_int = 0.03 dex): coverage >= 0.90 as before; median bootstrap
   interval width for f_young and f_old <= 0.6 (non-vacuous); and the
   false-positive rate — DECAY or MILD DECAY declared under the
   constant-f injection — <= 10%. Power under the exponential
   injection (f0 = 0.6, tau = 1.5 Gyr) is reported, not gated.
3. Everything else — inputs, bins, decision rule, power floor,
   bootstrap sizes, seeds — is unchanged. Script: e10b_a1_run.py
   (differences from e10b_run.py marked "A1"). A synthetic smoke run
   precedes the freeze, as before, and is committed as plumbing
   evidence only.

## Reporting rule

The frozen run (UNRESOLVED) and the amended run are reported side by
side in E10B-RESULTS.md; neither replaces the other. If the amended
run also fails its oracles, E10b is reported UNVALIDATED at this
sample size and stops.
