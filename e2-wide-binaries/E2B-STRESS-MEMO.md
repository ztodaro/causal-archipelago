> **CURRENT DISPOSITION: physical signoff remains on HOLD. Both the original hold-lift claim and the v2 universal sign proof below are withdrawn. An independent audit found an exact isotropic population counterexample. Screened cells are illustrative proxy-model calculations, not empirical bias bounds.**

# E2b Triple-Model Stress Test — Paper I hold LIFTED

Date: 2026-08-30, post-audit. Responds to audit F7 (Belokurov et al.
2020 channel: long-period photocenter motion entering fitted PM without
astrometric flags). Machinery: the committed injection model
(e2b_inject.py) with adversarially varied parameters; 36-cell grid ×
12 realizations (`e2b_stress.py`, `e2b_stress.json`). Seeded.

## Grid

Companion frequency {0.2, 0.3, 0.5} × detection-threshold scale
{0.5×, 1×, 2×, NONE (screens catch nothing)} × period distribution
{Raghavan lognormal; widened σ=3.0; log-uniform 1 d–3×10⁵ yr}.
Measured: induced bias on the PRIMARY ratio relative to a noise-only
reference in the same realization. Anchor separation: 0.18.

## Results

1. **Any functioning screens** (all 27 cells with threshold 0.5×–2×,
   companion frequency up to 50%, all period distributions):
   max |bias| = **0.020**, mean +0.002 — an order of magnitude below
   the anchor gap. The verdict is untouched by factor-of-two errors in
   the detection model in either direction.
2. **The unphysical no-screen limit** (astrometric screens assumed to
   catch nothing — contradicted by our own injection survival
   measurement and by the RUWE-binarity literature, including
   Belokurov et al. itself): bias +0.09 to +0.33, exceeding the gap at
   companion frequencies ≥0.3.
3. **Sign structure is decisive.** Every meaningful contamination cell
   biases POSITIVE — MOND-ward. Unresolved multiplicity inflates the
   low-acceleration median; it cannot deflate it. Therefore:
   - A false "MOND excluded" verdict would require a DOWNWARD push,
     which this channel cannot produce at any parameter setting.
   - Contamination's only possible crime here is manufacturing a FALSE
     MOND signal — the failure mode the design guards — and the sealed
     measurement came out at the clean-Newton anchor anyway (1.104 vs
     noise-only 1.115), which jointly bounds any real-world triple
     bias at ≲0.05 (larger bias would push the Newton+contamination
     prediction above the observed CI).

## Disposition

Paper I's HOLD is lifted. The paper gains a Robustness subsection
stating (1)–(3) with the grid table, and the limitation (iv) language
is strengthened from "model-dependent bound" to "sign-protected
verdict with a jointly self-limited bias." The no-screen corner is
reported, labeled unphysical, with its role explained: it is the bound
that shows why the sign argument, not the screens, carries the
conclusion.

---
## CORRECTION + v2 argument (2026-08-30, follow-up audit F5)

Three corrections. (1) The screened envelope is |bias| <= 0.0259 (a
negative cell missed by a positive-only scan), not 0.020. (2) The
amplitude-threshold screening model is NOT validated against the
Belokurov et al. (2020) long-period population; screened cells are
demoted to illustrative. (3) The one-signedness claim is now DERIVED
rather than simulated: for the median statistic, adding an
isotropically oriented photocenter PM offset n to a pair's
perpendicular velocity v gives median|v+n| >= |v| (at the median
orientation |v+n| = sqrt(v^2+n^2) > v), so every contaminated bin's
median rises; the identical physical Delta-mu offset divides by a
smaller v_circ in the low-acceleration bin, so the low bin rises
proportionally more, and the ratio bias is non-negative for ANY
contaminant population under isotropic orientations - independent of
the screening model. Verdict protection is therefore CONDITIONAL on
this derivation plus the no-screen bound and the observed clean-Newton
placement; unconditional signoff requires a Gaia epoch-level
astrometric simulation (registered, unscheduled). "Hold lifted" is
retracted in favor of conditional signoff.
