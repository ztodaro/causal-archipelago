# E1b spec — chemical genealogy at kiloparsec scale, survey-native (FROZEN)

Date frozen: 2026-08-30, before any E1b data retrieval. Supersedes nothing:
E1 stands as run (underpowered-inconclusive); E1b is the powered version
its results doc prescribed. All E1 calibration notes inherit (RAVE
metallicities excluded; star-clustered inference mandatory).

## Design change from E1, and nothing else

The pair test, hypotheses, treatment/control definitions, metrics, and
decision rule are E1's verbatim, with three frozen amendments:

1. **Sample = the surveys' own catalogs, not the 100 pc project sample.**
   Per survey: stars with valid [Fe/H] and clean flags (GALAH: flag_sp=0,
   flag_fe_h=0, snr>30; APOGEE: ASPCAP_STAR_BAD=0, SNR>70), catalog-native
   Gaia astrometry with parallax ≥ 1 mas (d ≤ 1 kpc) and
   parallax_over_error ≥ 10, survey RV present. Phase space via the
   validated numpy transform (d40_full_standalone.py), survey RV + Gaia
   proper motions.
2. **Controls additionally distance-matched:** control pair's mean
   heliocentric distance within 150 pc of the treatment pair's, and both
   control stars within the same survey (as before) — survey systematics
   vary with distance and this match is load-bearing at kpc scale.
3. **Power floor and effective-N reporting (the E1 lesson):** treatment
   pairs form a graph; connected components are the independent units.
   The frozen decision rule adds: a survey's result counts as CONFIRMED
   only if the clustered-bootstrap CI excludes zero AND the treatment
   graph has ≥ 30 connected components. Below 30, that survey reports
   as underpowered regardless of CI.

## Group masking at 1 kpc (frozen list)

Mask exact-ID members of: Theia (full clustered_sources, all distances —
already held), Cantat-Gaudin open-cluster members with parallax ≥ 1 mas
(NEW intake item), Bertolotto/Lee/Moranta/Jerabkova/SPYGLASS (held),
BANYAN (held; sky fallback as before). Unmasked known clusters are a
declared contamination risk, reported, not silently fixed.

## Decision rule (restated)

Both surveys CONFIRMED → chemical co-natality of the diffuse transfer
field is confirmed. One survey → suggestive. Neither, with both at power
(≥30 components) → the kill condition fires for the kpc regime.

## Intake required (agent; provenance per file, IDs as integer strings)

- GALAH DR4 full-catalog rows passing the server-side cuts above; columns:
  sobject_id, gaiadr3_source_id, ra, dec, parallax, parallax_error, pmra,
  pmdec, rv, e_rv, snr, teff, logg, fe_h, e_fe_h, flag_sp, flag_fe_h.
- APOGEE DR17 allStar rows passing cuts; columns: APOGEE_ID,
  GAIAEDR3_SOURCE_ID, GAIAEDR3_RA/DEC/PARALLAX/PMRA/PMDEC, VHELIO_AVG,
  VSCATTER, NVISITS, SNR, TEFF, LOGG, FE_H, FE_H_ERR, ALPHA_M,
  ASPCAP_STAR_BAD.
- Cantat-Gaudin 2020 cluster members, parallax ≥ 1 mas: GaiaDR2 id,
  cluster, RA/DE, plx, proba ≥ 0.7.
