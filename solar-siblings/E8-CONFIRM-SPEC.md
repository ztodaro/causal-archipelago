# E8-CONFIRM Spec — differential confirmation of sibling candidates (FROZEN)

Date frozen: 2026-08-30, BEFORE the archival census (96d4fa3) has
returned — i.e., blind not only to any spectrum's content but to whether
usable spectra exist at all. This is deliberate: the confirmation
criteria cannot be shaped by which candidates happen to have data.
Inherits all house rules. Applies to any candidate from
e8_gold_ranked.csv analyzed with R ≥ 40,000 spectra, archival or newly
proposed, by us or by collaborators acting under this protocol.

## Method (line-by-line differential, strictly relative to the Sun)

1. Solar reference: a reflected-sunlight spectrum (asteroid/Moon) from
   the SAME instrument and comparable epoch/setting; never a synthetic
   solar spectrum, never a different instrument.
2. Line list: the Meléndez et al. (2014) / Ramírez et al. (2014)
   solar-twin differential list (Fe I, Fe II + light, alpha, Fe-peak,
   and s-process species), restricted to lines with EW 5–120 mÅ in both
   spectra, measured identically (same continuum windows) in candidate
   and solar reference.
3. Stellar parameters by differential excitation/ionization balance
   (ΔTeff, Δlog g, Δξ solved simultaneously); abundances line-by-line
   differential (Δ[X/H] per line, averaged per species; internal error
   = line-to-line scatter / √N plus parameter covariance).
4. Age and mixing indicators measured alongside: Li 6708 Å abundance;
   [Y/Mg] and [Ba/Fe] at differential precision; differential
   isochrone age from (ΔTeff, Δlog g, Δ[Fe/H]).

## Verdict tiers (frozen; per candidate)

- **CONFIRMED SIBLING** requires ALL of:
  (a) ≥ 15 species measured; weighted-mean |Δ[X/H]| consistent with 0
      within 2σ, AND rms(Δ[X/H]) ≤ 0.025 dex across all species with no
      single species deviating > 3σ (condensation-temperature slope
      |dΔ[X/H]/dTc| < 2×10⁻⁵ dex/K, the solar-twin envelope);
  (b) differential isochrone age within 1 Gyr of 4.568 Gyr AND Li
      abundance consistent with the age–Li envelope for solar analogs
      (A(Li) < 1.5 for Teff within 100 K of solar; wider Teff → the
      envelope of Carlos et al.);
  (c) [Y/Mg] age within 1.5 Gyr of solar at the improved precision;
  (d) kinematic Tier-2 windows still satisfied with any improved RV.
- **CONSISTENT (unresolved)**: passes (a) but fails a non-chemical
  criterion at < 3σ, or ≥ 8 but < 15 species available. Remains a
  candidate; stated as such.
- **REJECTED**: fails (a) at ≥ 3σ (chemistry is decisive — a star that
  is not a chemical twin at 0.025 dex rms is not a birth sibling
  regardless of orbit), or Li/age indicators exclude solar age at ≥ 3σ.

## Reporting

Symmetric, per candidate, in E8-CONFIRM-RESULTS.md: all Δ[X/H] with
errors, the Tc slope, ages, and the tier — including every REJECTED
star. A single CONFIRMED SIBLING is reportable alone; claim language
remains capped ("a candidate solar sibling satisfying the preregistered
confirmation criteria") until independent replication.

## Contamination and honesty clauses

- Analysis order for multiple candidates: by frozen rank (WMAD), so
  early stopping cannot select on outcome.
- No criterion may be loosened post-hoc; a candidate failing (a) by an
  instrumental artifact (verified on the solar reference) may be
  re-observed, never re-thresholded.
- Binary/blended spectra: visible secondary light → analysis aborted
  for that dataset, documented, not counted as REJECTED.
