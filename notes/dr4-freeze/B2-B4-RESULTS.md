# DR4 bundle items B2 and B4 — results (2026-09-01)

Spec: B2-B4-SPEC.md (frozen at VM-side 1d4f4d4; Amendment 1 appended
before the B2 rerun). Scripts: b2_retention.py (SHA-256 71684031…,
after Amendment 1; the void first run 64a2bf9b… is kept as
b2_retention_run1_idjoin.log) and e2b_perspective.py (SHA-256
cfb446cc…, unchanged). Each run once. Raw outputs: b2_retention.json,
b4_perspective.json, logs. Lane: Fable 5.1 at owner instruction.

## B2 — expected DR4 astrometric retention of the GOLD list

Sanity gate (Amendment 1): with the observation-id join, all 221 GOLD
stars recompute inside the Tier-2 window at DR3 point values, as they
must. Median DR3 parallax error 0.034 mas; median GALAH RV error
0.35 km/s.

| case | mean retention | expected survivors of 221 | 95% interval | stars with P < 0.5 | P < 0.9 |
|---|---|---|---|---|---|
| DR4 (parallax ×0.718, PM ×0.370, RV unchanged) | 0.994 | 219.6 | [218, 221] | 0 | 4 |
| DR4, PM errors ×2 (sensitivity) | 0.994 | 219.6 | [218, 221] | 0 | 4 |
| DR3 re-measurement (control) | 0.993 | 219.3 | [217, 221] | 0 | 5 |

**Frozen prediction (B2):** under DR4 astrometry, 218–221 of the 221
GOLD stars remain inside the E8 Tier-2 action window (expectation
219.6). The window is loose relative to the astrometric precision of
these bright nearby stars, so DR4 barely moves membership; the
control row shows membership is already stable at DR3 precision. What
DR4 can still change is the non-single-star screen (B2 action b),
which this calculation does not model and which is the more likely
source of attrition. A DR4 survivor count below 215 would indicate
either DR4 systematics beyond the scaled-noise model or a flaw in
the frozen action computation, and would be reported as such.

## B4 — El-Badry perspective term on the sealed bins

Implementation: correct_perspective() subtracts v_r·theta along the
separation vector; the synthetic self-test recovers injected vectors
to 1.1e-16 km/s. Ready for the DR4 rerun once RVs are joined
(retrieval hand-off in the spec; the E2b input carries no RVs).

Statistical size of the term (sigma_vr = 25 km/s; 20 and 30 in the
JSON), in vtilde units, primary sample:

| bin | n | theta P50 (rad) | v_circ P50 (km/s) | PM-noise e_vtp P50 | delta P50 | delta P90 |
|---|---|---|---|---|---|---|
| calibration [10–100] a0 | 6,933 | 3.2e-5 | 0.80 | 0.070 | 0.0006 | 0.0021 |
| decision [0.1–1] a0 | 1,377 | 3.0e-4 | 0.26 | 0.193 | 0.018 | 0.066 |
| flicker [0.1–0.3] a0 | 479 | 4.5e-4 | 0.22 | 0.228 | 0.034 | 0.090 |

For comparison, Boufourou (2026) reports P90|delta| = 0.0016 in his
validation zone and 0.177 in his deep bin; our nearer, tighter sample
sits between, and in every bin the term is well below the per-pair
proper-motion noise (0.07–0.23) that the anchors already carry.

Perspective-inclusive anchors (400 MC draws, seed 2026; the
no-perspective reproduction lands within MC scatter of the frozen
anchors):

| anchor | frozen | reproduction (no perspective) | with perspective, sigma_vr = 25 | shift |
|---|---|---|---|---|
| Newton primary ratio | 1.115 [1.070, 1.160] | 1.117 [1.068, 1.164] | 1.120 [1.072, 1.174] | +0.003 |
| MOND-scale primary ratio | 1.299 [1.238, 1.356] | 1.299 [1.244, 1.356] | 1.299 [1.246, 1.353] | 0.000 |
| Newton flicker median | 0.682 [0.639, 0.726] | 0.682 [0.632, 0.727] | 0.686 [0.640, 0.730] | +0.004 |
| MOND-scale flicker median | 0.788 [0.737, 0.841] | 0.789 [0.740, 0.843] | 0.786 [0.739, 0.840] | −0.003 |

Position of the unsealed data against the perspective-inclusive
anchors: primary 1.104 [1.063, 1.164] lies inside the Newton anchor
and outside the MOND-scale anchor, as before; flicker 0.699
[0.640, 0.733] lies inside the Newton anchor and its upper bound
stays below the MOND-scale anchor's lower bound (0.739), as before.
The shifts are an order of magnitude smaller than the anchor
half-widths (~0.045). The frozen E2b verdict is not re-decided here;
this quantification is appended beside it and answers the systematic
flagged in the Boufourou method-transfer memo: on this sample the
perspective term is subdominant, and the exposed flicker statistic
moves by +0.004.

Caveats: the term's direction was modelled along a fixed sky axis
with uniform velocity phase; sigma_vr is a declared population value,
not measured per pair; sensitivity across 20–30 km/s changes the
Newton primary anchor by < 0.002. With real RVs joined, the DR4 rerun
applies the per-pair correction instead and this statistical
treatment retires.

## Consequences for the bundle

B2 and B4 are closed as pre-tag items. The E2b DR4 rerun (B4 in the
main spec) must call correct_perspective() when RVs are available and
otherwise use the perspective-inclusive anchors above. MANIFEST.sha256
is refreshed to include these files.
