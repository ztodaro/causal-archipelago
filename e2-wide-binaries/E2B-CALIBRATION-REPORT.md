# E2b Calibration Report — open region (g_N > 10 a₀) only

Date: 2026-08-30. Spec: E2B-SPEC.md frozen at `d0cf4a7` (before retrieval).
Intake: `e9f60cd`, `e2b_elbadry_200pc.csv`, 125,713 rows, SHA-256
`4a8d9cd8017aa7178c9b5acaf8e9f34dce450d3cd96ee40ba0c430134c4dd9a0`
(verified byte-identical before analysis). Pipeline: `e2b_cal.py`,
`e2b_inject.py` (this folder). No statistic of the sealed region
(g_N < 10 a₀) has been computed; sealed pairs are counted only.

## Selection cascade (spec cuts, in order)

| step | pairs |
|---|---|
| intake (either Plx ≥ 5, R < 0.1) | 125,713 |
| both components Plx ≥ 5 mas | 113,574 |
| per-component quality (RUWE < 1.4, IPDfmp ≤ 2, sepsi < 2, RPlx ≥ 20) | 20,024 |
| parallaxes consistent within 3σ | 19,910 |
| projected separation 500–50,000 AU | 15,403 |
| both components main-sequence (BinType = MSMS) | 13,634 |
| duplicate-component screen (within intake) | 13,634 (0 dropped) |
| bound-pair screen ṽ_perp < 2 (carried over from E2) | 13,356 |
| → PRIMARY (R_chance_align < 0.01) | **13,233** |

Clarification made in the open phase, pre-anchoring: the frozen mass
prescription (Mamajek v2022.04.16 M_G→mass) is defined only for
main-sequence stars, so pairs with a white-dwarf or unclassified component
(WDMS/WDWD/MS??/etc.) are excluded via the catalog BinType. This is
spec-implied, not a new degree of freedom; it is recorded here before
anchoring. The duplicate-component screen is applied within the frozen
intake (every catalog pair containing a ≤200 pc component and R < 0.1 is
in the intake by construction; pairs sharing a component with R ≥ 0.1
are outside it — noted as a bounded purity caveat).

## Data-integrity checks (El-Badry-internal)

The VizieR `theta` column is in degrees; catalog `sepAU` reproduces
θ×3600×(1000/Plx1) to machine precision (median relative error 0.0).
Median pair distance 161 pc (p90 192 pc). Median ΔPM error 0.072 mas/yr
(p90 0.180). M_G span 2.45–16.05, inside the Mamajek grid. Median total
mass 0.74 M☉.

## Calibration-region statistics (PRIMARY sample)

| bin | n | median ṽ | IQR | median σ_ṽ |
|---|---|---|---|---|
| [10–100] a₀ | 6,933 | 0.582 | 0.370–0.828 | 0.070 |
| > 100 a₀ | 1,207 | 0.573 | 0.347–0.804 | 0.033 |

Scale-free to 1.6% across a decade of acceleration — the Newtonian
expectation, and consistent with E2's 100 pc calibration (0.58). The
bound screen removes only 1.0% of calibration pairs. R < 0.1 variant is
statistically indistinguishable in the open region.

## Noise MC — the central calibration result

Real per-pair ṽ errors (four catalog PM errors propagated through each
pair's distance and v_circ) are ~3× larger in the sealed decision bin
(median σ_ṽ = 0.19) than in the calibration bin (0.07), because v_circ
falls with separation while PM noise does not. Forward-modeling the
PRIMARY statistic (true-ṽ template = open-region empirical distribution;
2-D Gaussian PM noise per pair; 400 realizations):

| hypothesis | predicted ratio (mean, 95% MC) |
|---|---|
| Newton (B = 1.0) | **1.115** [1.070, 1.160] |
| MOND-scale (B = 1.2) | **1.299** [1.238, 1.356] |

The naive anchors (1.0 / 1.2) are therefore replaced by noise-adjusted
anchors. The hypotheses remain separated (gap ≈ 0.08 between CI edges).

Flicker-bin SECONDARY ([0.1–0.3] a₀, median σ_ṽ = 0.23): predicted median
ṽ = 0.682 [0.639, 0.726] under Newton, 0.788 [0.737, 0.841] under MOND.
Note what this does to E2's anecdote: the 18-pair median of 0.73 sits at
the edge of the Newtonian noise expectation — the "flicker" was plausibly
noise inflation. E2b tests it with ~479 pairs.

## Precision-trimmed variant (preregistered here)

Cutting on σ_ṽ < 0.15 (computable blind — PM errors only, never the
observable) restores near-textbook anchors with adequate power:
n_low = 506, n_high = 5,776; Newton 1.009 [0.942, 1.075], MOND 1.198
[1.129, 1.274]. Frozen as labeled robustness variant (b).

## PM-reflex triple injection

Assumptions: 30% companion frequency per component; q ~ U(0.1,1);
Raghavan lognormal periods (μ = 5.03, σ = 2.28 in log₁₀ days); photocenter
a_ph = a·(q/(1+q) − ℓ/(1+ℓ)) with ℓ = q⁴; Gaia baseline 2.83 yr;
period-averaged PM-offset envelope 2πa_ph/P (P ≥ T), (2πa_ph/T)(P/T)
(P < T); wobble-detection threshold σ_det(G) = 0.08/0.15/0.40/0.80 mas at
G = 13/15/17/19 (RUWE/ipd/aen proxy). Results (20 realizations): screens
flag 47% of injected triples; **3.6%** of pairs carry a surviving triple;
ratio bias on the PRIMARY statistic **+0.006** — an order of magnitude
below the Newton–MOND gap. Consistent with E2's f ≲ 3%.

## Sealed-region counts (counts only — no statistics computed)

PRIMARY sample: 5,093 sealed pairs; decision bin [0.1–1] a₀: **1,377**
(no reduced-power flag; threshold 500); flicker bin [0.1–0.3] a₀: 479.
Precision-trimmed variant decision bin: 506.
