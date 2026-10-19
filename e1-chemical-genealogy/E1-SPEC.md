# E1 spec — chemical genealogy of the diffuse coherent field (FROZEN)

Date frozen: 2026-08-30, before any abundance data for this test has been
retrieved. This file's commit hash is the preregistration anchor.

## Hypothesis

H1: Star pairs that are mutually cheap-transfer neighbors (|Δx| < 20 pc,
|Δv| < 3 km/s) OUTSIDE all known catalog groups are more chemically similar
than matched control pairs. If true, the diffuse coherent field (the ~91%
of top-decile excess stars in no large structure) is substantially
composed of dissolved birth families, not chance velocity coincidence.

H0: abundance similarity of cheap-transfer pairs is indistinguishable from
matched controls once stellar-parameter systematics are controlled.

## Data (public; to be retrieved AFTER this freeze, with provenance files)

- GALAH DR4 (fallback DR3): [Fe/H], [α/Fe], and up to ~30 element
  abundances; keyed to Gaia DR3 (DR4) ids.
- APOGEE DR17 allStar: FE_H, ALPHA_M, element grid; GAIAEDR3_SOURCE_ID.
- Join by exact integer source_id to the frozen 133,468-star sample.
  NEVER compare abundances across surveys — all pair comparisons are
  within-survey.

## Sample construction (frozen)

1. Abundance subsample A_s per survey s: sample stars with a valid
   [Fe/H], survey quality flags clean (GALAH: flag_sp = 0, flag_fe_h = 0;
   APOGEE: ASPCAPFLAG bad bits unset), SNR above the survey's recommended
   floor.
2. Mask ALL members of any catalog group used anywhere in this project
   (crossmatch + vetting catalogs) — the claim is about the DIFFUSE field.
3. Treatment pairs: within A_s, all pairs with |Δx| < 20 pc and
   |Δv| < 3 km/s.
4. Control pairs: for each treatment pair, sample 10 pairs from A_s
   matched on (a) pair separation |Δx| within 5 pc, (b) both stars'
   Teff within 150 K and logg within 0.3 dex of the treatment stars —
   abundance errors correlate with stellar parameters, and this matching
   is the test's load-bearing systematic control — with |Δv| > 6 km/s.

## Metrics and decision rule (frozen)

- Primary: median |Δ[Fe/H]| (treatment) vs (control), per survey;
  Mann-Whitney p; effect size = median difference in dex with bootstrap
  95% CI (1,000 resamples of pairs, clustered by star to respect reuse).
- Secondary: same for [α/Fe]; exploratory for individual elements.
- Positive result: treatment median |Δ[Fe/H]| lower than control in BOTH
  surveys with CIs excluding zero. Mixed or single-survey: reported as
  suggestive, not confirmed.
- Kill: no effect in either survey → the diffuse field is kinematic
  coincidence at current chemical precision; reported as such.

## Guards

Stars contribute to multiple pairs — all inference clustered by star.
Distance to the Sun matched implicitly via Teff/logg/SNR matching; any
residual imbalance reported. No peeking: metrics computed once, after the
full join is committed with hashes. Results reportable as evidence only
if this spec is followed; deviations documented inline.
