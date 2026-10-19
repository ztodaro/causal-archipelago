# E2b Unsealed Results — Newtonian; MOND-scale boost excluded

Date unsealed: 2026-08-30, on owner instruction, after verification of the
public anchor. Spec `d0cf4a7` → intake `e9f60cd` → calibration freeze
`953e527b256ad2f4b8cd567a25b92295988c196b` (tag `pre-unseal-e2b`) →
GitHub release `pre-unseal-e2b-anchor` published 2026-08-30T10:10:44Z
(git bundle + archive, SHA-256
`165a7e7537869acb07dd65110298f68b4d1512c3ca29c4d95f7a6aae88960e82`,
OpenTimestamps proof; Bitcoin upgrade scheduled) → sealed computation run
once (`e2b_unseal.py`, byte-identical to the anchored copy, verified
before execution). Raw output: `e2b_UNSEALED.json`; figure:
`e2b-unsealed.png`.

## Verdict

**The sealed low-acceleration bin is consistent with Newtonian gravity,
and the MOND-scale anchor is excluded — in the primary statistic, the
preregistered secondary, and both labeled variants.**

| statistic | n_low | measured [95% CI] | Newton anchor | MOND anchor | outcome |
|---|---|---|---|---|---|
| PRIMARY ratio [0.1–1]/[10–100] a₀ | 1,377 | **1.104 [1.063, 1.164]** | 1.115 [1.070, 1.160] | 1.299 [1.238, 1.356] | Newton not excluded; **MOND excluded** |
| SECONDARY flicker-bin median [0.1–0.3] a₀ | 479 | 0.699 [0.640, 0.733] | 0.682 [0.639, 0.726] | 0.788 [0.737, 0.841] | Newton not excluded; **MOND excluded** |
| Variant: R < 0.1 | 1,395 | 1.103 [1.062, 1.163] | 1.115 [1.070, 1.160] | 1.299 [1.238, 1.356] | Newton not excluded; **MOND excluded** |
| Variant: precision-trimmed σ_ṽ < 0.15 | 506 | 1.035 [0.968, 1.108] | 1.009 [0.942, 1.075] | 1.198 [1.129, 1.274] | Newton not excluded; **MOND excluded** |

No reduced-power flag (n_low = 1,377 ≥ 500). Median ṽ: 0.642 (decision
bin) vs 0.582 (calibration bin) — the deep-bin elevation is fully
accounted for by the noise-adjusted Newtonian prediction.

## The flicker is resolved

E2's hypothesis-generating anecdote (18 pairs, median 0.73) motivated the
preregistered secondary. With 479 pairs the flicker bin measures 0.699
[0.640, 0.733] against a Newtonian noise-adjusted expectation of 0.682
[0.639, 0.726]: **the flicker was PM-noise inflation, as the calibration
forward model predicted.** The MOND expectation for that bin (0.788) is
excluded.

## The one distinction that matters

The raw ratio 1.104 sits *above* the naive Newtonian value of 1.0 — a
reader who skipped the calibration would see a "10% MOND-ward signal."
The noise MC (frozen and anchored before unsealing) shows that Newtonian
gravity *plus real Gaia PM errors* predicts exactly this inflation
(1.115 ± 0.045). The precision-trimmed variant, where noise is small and
the anchors are near-textbook (1.009 vs 1.198), lands at 1.035 [0.968,
1.108] — right on Newton. The apparent boost tracks the noise, not the
acceleration. This is the same failure mode E2's projected-separation
correction addressed, and it is the reason the anchors were preregistered.

## Standing of the result

Preregistered, publicly anchored (GitHub release + OpenTimestamps before
the sealed computation), symmetric-reporting test of gravity in the
low-acceleration regime using 13,233 El-Badry wide binaries within
200 pc, PM-only observables, real per-star errors, and triple-injection
contamination bounds (f ≈ 3.6%, bias +0.006, an order of magnitude below
the anchor separation). It lands on the Newtonian side of the live
wide-binary dispute (with Banik et al. 2024's conclusion; against a
MOND-scale boost of the Chae type), with a decision-bin sample ~6× E2's
and the flicker anecdote laid to rest. Deviations from the frozen spec:
none. Drawer status: opened once; closed.
