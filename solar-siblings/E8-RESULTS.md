# E8 Results — the solar-sibling sieve

Date: 2026-08-30. Spec frozen `28d308e` (verified pre-run); intake
`b3ee7b2` (GALAH 349,899 rows SHA `5b50329e…35da4`; APOGEE 331,088 rows
SHA `ced72502…9c040`; both verified byte-identical after staging). Sieve
`e8_sieve.py` as committed; single pass; kill condition NOT triggered.

## Counts

| tier | GALAH (decision lane) | APOGEE (exploratory) |
|---|---|---|
| Tier 1 — CANDIDATE (chemistry + age) | 1,439 | 639 |
| Tier 2 — KINEMATIC-CONSISTENT | 852 | 259 |
| Tier 3 — GOLD (13-element vector) | **221** | — (spec: no GOLD from survey data) |

GOLD properties: WMAD 0.018–0.040 dex (median element count 13/13),
clock ages 3.1–6.1 Gyr, distances median 397 pc (p90 635 pc) — well
beyond the 100 pc pilot volume. LINKED flags: 0 (expected: the M3
structures are young; solar siblings are not). Overall field→GOLD rate:
6.3×10⁻⁴.

## Top of the ranked list (by WMAD; full list in e8_gold_ranked.csv)

| Gaia DR3 | WMAD | age (Gyr) | Lz | d (pc) |
|---|---|---|---|---|
| 6379813798086252160 | 0.0177 | 5.8 | 1905 | 563 |
| 5377439590220801920 | 0.0180 | 3.7 | 2013 | 687 |
| 4704616882942264320 | 0.0183 | 5.9 | 1855 | 379 |
| 6716036271949014400 | 0.0192 | 3.3 | 1710 | 549 |
| 6086357992929479296 | 0.0193 | 4.7 | 1692 | 571 |

## The honest arithmetic (read before celebrating)

Completeness, measured by injection (10,000 synthetic solar clones with
real survey errors): **C = 5.9%** conditional on the clean Teff/log g
box. The frozen windows are narrow relative to survey precision, so even
a true sibling passes Tier 1 only ~1 time in 17 — mostly scattered out
by [Fe/H] and [Y/Mg] measurement noise.

Expected TRUE siblings in the GOLD list: published dispersal models put
~1–10 siblings within ~1 kpc; the GALAH footprint and clean box sample
perhaps 10–30% of solar-type stars in that volume; times C = 0.059 →
**0.02–0.2 expected true siblings among the 221 GOLD stars.** The
complementary statement: ≥220 of the 221 are solar *analogs* — stars
chemically indistinguishable from the Sun at ~0.05 dex/element survey
precision, solar-age on the clock, orbit-compatible — but not siblings.

Both directions of the symmetric verdict, therefore:
- This is NOT a detection, and the spec's claim caps hold: every GOLD
  star is a candidate only.
- This is also NOT a null: with C = 5.9%, the search excludes nothing.
  What it produces is the intended instrument — a **ranked follow-up
  shortlist**, the best-ordered haystack available, in exactly the form
  that confirmed HD 162826: 0.01-dex differential high-resolution
  spectroscopy of the top handful, where a true sibling separates from
  a mere analog.

## What would change the odds

At survey precision the sieve cannot pass ~10⁻⁴-level purity; the
discrimination lives in follow-up. Concretely: the top ~10 by WMAD are
one observing proposal (differential abundances vs the solar spectrum,
±0.01 dex, plus Li and s-process ratios as birth-cluster discriminants).
A future E8b (new spec, new freeze) could widen completeness with DR4
astrometry, looser windows plus explicit purity modeling, or a
northern-survey lane.

## Deviations from the frozen spec

None. One robustness note (not a deviation): 36,118 GALAH rows carry
blank Gaia DR3 IDs (DR2→DR3 join gaps, disclosed at intake); they
remained eligible for all tiers via survey astrometry and are
identifiable by sobject_id.
