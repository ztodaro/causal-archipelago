# E10c feasibility — the APOGEE [C/N] replication cannot be powered (recorded 2026-09-01)

Outcome: **INFEASIBLE**; no
spec frozen, no run.

## What was checked (availability and kinematics only; no chemistry
outcome was read)

The Spoo et al. 2022 [C/N] clock applies to giants (log g < 3.3,
−0.53 ≤ [Fe/H] ≤ 0.31). Counts, from the committed E1b APOGEE inputs
and the E8 APOGEE abundance table (b3ee7b2), using the ASPCAP bad-bit
mask (bits 0–4, 6) rather than flag = 0:

| set | count |
|---|---|
| E8 APOGEE table stars in the clock domain with clean C, N | 23,571 |
| E1b APOGEE treatment pairs (dx < 20 pc, dv < 3 km/s) | 4,521 |
| … with both members log g < 3.3 | 30 |
| … with both members in the clock domain with clean C, N | 17 |
| … among E1c's C4 (full-orbit-controlled) pairs | 2 |

The E10b power floor is 60 pairs with age-posterior mass > 0.5 in
each decision bin. The APOGEE giant-pair sample is short of that by
more than an order of magnitude before any age split. The reason is
structural, not a flag choice: comoving pairs within 20 pc of each
other are a nearby-star phenomenon, and APOGEE's giants are distant
and sparse, so giant–giant comoving pairs barely exist in the
selection. Loosening the flag mask further, or widening the
metallicity domain, cannot recover a factor of thirty.

## Disposition

The replication recommended by the Deep Check (union report §B) is
not available in the data in hand. The design is preserved
(E10C-SPEC.md, e10c_run.py, and the synthetic smoke output) for a
survey that does contain comoving giant pairs, or for a dwarf-
applicable APOGEE age source under its own calibration spec (which
would be a new intake, not a rerun). E10b therefore stands as a
single-survey (GALAH) purity result, and its licensed claim carries
the "one survey" qualifier explicitly. This also corrects the recommendation of an hour earlier: the "cheap replication" does not
exist here; it was cheap only if the pairs existed, and the count
was never checked before the recommendation was made.

## Reproduction

The counts above come from replaying the E1b APOGEE loading and
treatment selection (e1c_diag.py's loaders, verbatim) and joining the
E8 abundance table on exact integer-string GAIAEDR3_SOURCE_ID; the
smoke log e10c_smoke.log shows the 2-of-919 figure for the C4 subset.
