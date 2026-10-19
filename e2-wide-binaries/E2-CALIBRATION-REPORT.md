# E2 calibration-region report — seal intact

Date: 2026-08-30. Spec: E2-SPEC.md (a82ea9c). Code: `e2_calibration.py`,
`e2_cal2.py`. Data: `e2_calibration.json`, `e2_cal_perp.json`,
`e2_cal_pairs.npz`. SEAL STATUS: pairs with g_N < 10 a₀ were filtered and
discarded before any counting, printing, or storage. Nothing about the
sealed region — including how many pairs it contains — is known to this
analysis.

## Selection (per frozen spec)

From the 133,468-star sample: 3D separation 500–30,000 AU, distance
consistency < 0.5 pc, |Δv_3D| < 2 v_circ (selection bound only),
RV errors < 1.5 km/s, resolved-triple screen (no third sample star within
10,000 AU). Masses: Mamajek v2022.04.16 M_G→mass interpolation, fixed
before any velocity statistic. Result: 406 pairs pre-seal → **112
calibration pairs** (g_N > 10 a₀).

## Validation results

1. **El-Badry cross-check: 109/112 (97%) of our calibration pairs appear
   in the independent public catalog.** The 3 non-overlaps are flagged for
   inspection before unsealing (spec requirement).
2. **The primary observable behaves:** PM-based ṽ_perp (the spec's primary;
   proper-motion precision ~0.02 km/s) has median 0.773, IQR 0.49–1.09,
   14.3% above √2, none above 2 — consistent with a mostly-bound Newtonian
   population plus a ~14% contamination/noise tail, squarely in the range
   published contamination estimates predict for comparable samples.
3. **Diagnostic lesson recorded:** the RV-based 3D ṽ is noise-dominated
   (RV errors ~ v_circ at these separations; median 1.22, 38% above √2)
   and is demoted to a binarity diagnostic — our RV completeness screens
   companions; it cannot measure orbital velocity at km/s-scale precision.
   This mirrors why the professional analyses are PM-based, and our RVs
   remain an *additional screen* they typically lack.

## Small-N status

112 calibration pairs implies the sealed region likely holds fewer (wider
pairs are rarer and RV-complete-both-members is a strong cut). The spec's
contraction clause (sealed N < 50 → deliverable becomes method +
contamination audit + forecast) is live and will be honored as written.

## Remaining before unsealing (in order)

1. Inspect the 3 El-Badry non-overlap pairs.
2. Synthetic hierarchical-triple injection: measure velocity inflation in
   the calibration region; propagate to a contamination model.
3. PM/RV noise Monte Carlo (house method, 12 realizations).
4. Commit the full calibration analysis; then — owner's call — the
   adversarial-collaboration window (share frozen protocol with both
   camps) before the seal is broken.
