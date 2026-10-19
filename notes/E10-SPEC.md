# E10 Spec — the forgetting curve (FROZEN before any excess computation)

Date: 2026-08-30. Power gate run first (`e10_run.py --power`, output
`e10_power.json`); this spec is committed before the full phase touches
any chemical-excess number. Machinery inherited VERBATIM from E1b
(masking set, phase-space transform, pairing dxp<20 pc & dvp<3 km/s,
Δv>6 control candidates, Teff/log g/separation/distance bucket matching
≤10 controls per pair, star-clustered bootstrap ×1000). Data: the
committed E8 GALAH abundance table (`b3ee7b2`), E1b-style cleaning
(blank IDs skipped, |RV|>400 sentinel guard, best-SNR dedup).

## Concept

Birth chemistry never decays; what decays is the informativeness of
kinematic linkage. The E1b twin excess of kinematically linked pairs,
measured in bins of [Y/Mg] clock age, is the empirical decay curve of
the disk's kinematic memory — chemistry as the fixed ruler.

## Age lane (from E8's frozen clock, unchanged)

Per star: t = (0.170 − [Y/Mg])/0.0371 (Nissen 2016), valid only for
flag_sp=0, flag_fe_h=0, flag_y_fe=0, flag_mg_fe=0, SNR ≥ 30,
Teff ∈ [5200, 6300], log g ≥ 3.5. Pair age = mean(t₁, t₂), assigned
only when both stars have valid clocks AND |t₁ − t₂| < 3 Gyr
(age-consistency precondition for a co-natal reading). GALAH is the
sole decision lane; the APOGEE [C/N] lane is deferred (coarse clock),
documented.

## Bins and power gate (counts recorded pre-freeze)

| bin (Gyr) | aged pairs | clusters | status |
|---|---|---|---|
| [0, 2) | 11 | 10 | **underpowered — descriptive only** (floor: 25 pairs, 15 clusters) |
| [2, 4.5) | 33 | 23 | powered |
| [4.5, 8) | 25 | 25 | powered |

Gate rule (declared in FUTURE-EXTENSIONS §E10): ≥2 powered bins →
proceed. Satisfied.

## Preregistered statistics and decision rules

PRIMARY, per powered bin: median |Δ[Fe/H]| of aged treatment pairs vs
their matched controls; star-clustered bootstrap 95% CI on the
difference. Outcomes:
- **Memory persists**: the [4.5, 8) bin's CI excludes zero (twin excess
  survives at ≥ solar age — kinematic linkage remains informative).
- **Forgetting detected**: [2, 4.5) excludes zero AND [4.5, 8) is
  consistent with zero.
- **Inconclusive**: any other pattern; reported as such.

SECONDARY (descriptive, preregistered): median clock-age disagreement
|Δt| of treatment vs control pairs per bin — co-natal pairs should be
more co-eval than matched chance pairs at every age.

Small-N honesty: per-bin matched counts may fall below the aged counts
above (control availability); a powered bin whose MATCHED count drops
below 25 or clusters below 15 reverts to underpowered, reported.

## Symmetric reporting

All three bins reported with counts and point estimates regardless of
outcome; the underpowered young bin carries no decision weight. One
run; no re-binning, no threshold changes after this commit.
