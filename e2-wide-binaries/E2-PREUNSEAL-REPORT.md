# E2 pre-unseal report — calibration complete, seal intact

Date: 2026-08-30. Code: `e2_calibration.py` (corrected), `e2_cal2.py`,
`e2_preunseal.py`. Data: `e2_calibration.json`, `e2_cal_perp.json`,
`e2_preunseal.json`, `e2_cal_pairs.npz`. The sealed region (g_N < 10 a₀)
remains uncounted and unexamined.

## The catch the calibration phase existed for

The first build computed **3D separations — a deviation from the frozen
spec, which says projected.** At these distances the radial component of a
~1,000 AU pair is parallax-noise (σ ~ 10⁴ AU), so 3D separations were
noise-dominated: only 112 calibration pairs survived, with a spurious 14%
tail above the bound-orbit ceiling. Corrected to projected separation
(angular × mean distance) per spec: **735 calibration pairs**, and the
distribution snapped onto the literature's bound-orbit shape. Both runs
are preserved; the correction was found and fixed entirely inside the open
calibration region.

## Calibration results (corrected)

- **ṽ_perp: median 0.548, IQR 0.35–0.76, 1.9% above √2, none above 2** —
  textbook bound-Newtonian, matching published wide-binary distributions.
- **El-Badry cross-check: 650/735 (88%).** The 85 non-overlaps are
  characterized as a class: 14 involve bright (G<8) stars El-Badry's cuts
  exclude; the subset runs slightly hot (ṽ median 0.68, tail 11%) —
  consistent with a mix of legitimately-excluded bright pairs plus some
  chance alignments/triples their R_chance cut removed.
- **Triple injection: the screens kill 93% of synthetic hierarchical
  triples.** Survivors would show a 36% tail; the observed 1.9% tail
  equals the pure-noise expectation (1.8% ± 0.2%), implying residual
  contamination **f ≈ 0, bounded ≲ 3%**. Sensitivity table: even f = 0.15
  would inflate the median only 0.548 → 0.62 — surviving contamination at
  any plausible rate CANNOT manufacture a 20% median boost. This is the
  preregistered defense against the debate's central objection.
- **Noise MC (12 realizations): median 0.545 ± 0.004, tail 1.8% ± 0.2%.**
  The statistic is measurement-stable.

## Pre-unseal amendments (frozen with this commit, before any seal access)

1. Primary unsealed analysis runs on the **El-Badry-intersected subset**
   (maximum purity); the full own-selection set is the labeled sensitivity
   variant. Both reported.
2. Decision statistic as spec'd: ratio of median ṽ_perp in [0.1 a₀, a₀]
   to median in [10 a₀, 100 a₀], bootstrap CI clustered by pair, published
   symmetrically wherever it lands. Newtonian expectation ≈ 1.0; MOND-type
   ≈ 1.2. Small-N contraction clause remains live.

## Status

Every pre-unseal requirement in the frozen spec is now executed and
committed. The seal is unbroken. Remaining: the owner's decision — unseal
now, or first run the adversarial-collaboration window.
