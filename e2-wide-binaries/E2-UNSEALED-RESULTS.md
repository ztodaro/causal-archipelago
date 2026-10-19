# E2 unsealed results — computed once, reported symmetrically

Date: 2026-08-30. Protocol: E2-SPEC.md (a82ea9c) + pre-unseal amendments
(7e75a61), publicly anchored BEFORE this computation: GitHub push
2026-08-30T09:05:35Z (tag pre-unseal-v1 → 7e75a61…5017; tree SHA
823a62b9…a3fa), OpenTimestamps proof committed (Bitcoin upgrade pending).
Code: `e2_unseal.py`. Data: `e2_UNSEALED.json`, `e2_unsealed_pairs.npz`.
Figure: `e2-unsealed.png`.

## The sealed bin

270 pairs below 10 a₀ (219 El-Badry-intersected). The small-N contraction
clause (< 50) did NOT trigger; the frozen decision statistic is reported.

## Decision statistic (frozen: median ṽ ratio, [0.1–1] a₀ over [10–100] a₀)

| sample | n_low | n_high | ratio | 95% CI |
|---|---|---|---|---|
| **El-Badry-intersected (PRIMARY)** | 53 | 388 | **1.070** | **[0.849, 1.252]** |
| full own-selection (variant) | 69 | 448 | 1.123 | [0.942, 1.256] |

Reference points: Newtonian ≈ 1.0; MOND-type ≈ 1.2.

## Verdict, symmetric as committed

**The measurement is consistent with Newtonian gravity and cannot exclude
the MOND-type boost.** The primary CI contains both hypotheses; the point
estimate (1.07) sits between them. No detection is claimed in either
direction. Descriptive note, explicitly NOT a claim: the deepest bin
(0.1–0.3 a₀, 18 primary pairs) has median ṽ ≈ 0.73 vs the Newtonian
baseline 0.58 — visually suggestive, statistically empty at this n, and
the frozen decision statistic (which is the only preregistered inference)
is inconclusive.

## What this measurement is worth

It is, to our knowledge, the only entry in this debate whose complete
analysis chain — selection, contamination model (residual f ≲ 3% after
screens that kill 93% of injected triples), noise MC, and decision rule —
was frozen and publicly timestamped before the test region was computed.
It is also RV-complete (both components), which the PM-only literature
samples are not. Its limitation is pure statistics: 53 primary decision
pairs cannot separate 1.0 from 1.2.

## The forecast (the honest deliverable)

CI half-width scales ~1/√n: separating Newton from MOND at ~95% confidence
needs roughly 4× the decision-bin pairs (n_low ≈ 200+). Dropping the
RV-complete requirement and extending to ~200 pc (PM-only, like the
published analyses, but under this frozen-and-anchored protocol and with
our screens re-derived for PM-only data) plausibly reaches that. That is
a NEW spec freeze (E2b), not a widening of this one — per the frozen
scope clause.

## Status of the seal

Broken 2026-08-30, once, on the owner's instruction, after public
anchoring. Every prior state is verifiable via the anchored tag.
