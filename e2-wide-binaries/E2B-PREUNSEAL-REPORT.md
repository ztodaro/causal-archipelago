# E2b Pre-Unseal Declaration — analysis frozen

Date: 2026-08-30. This document freezes the E2b analysis before any sealed
computation, per the ritual in E2B-SPEC.md (`d0cf4a7`). The unseal code
`e2b_unseal.py` is committed with this declaration and will not be edited
afterward. The drawer opens once, on owner instruction, after public
anchoring.

## Chain of custody

1. Spec frozen `d0cf4a7` — before any E2b data existed.
2. Intake `e9f60cd` — El-Badry ≤200 pc powered sample, 125,713 rows,
   SHA-256 `4a8d9cd8…4dd9a0`, verified before analysis.
3. Calibration executed in the open region only (g_N > 10 a₀):
   E2B-CALIBRATION-REPORT.md, `e2b_cal.py`, `e2b_inject.py`,
   `e2b_cal.json`, `e2b_inject.json`, `e2b_secondary_anchors.json`.
4. This declaration + `e2b_unseal.py` committed. → PUBLIC ANCHORING
   (tag `pre-unseal-e2b`, GitHub push, OpenTimestamps) happens NEXT,
   before any sealed number exists anywhere.

## Frozen analysis (verbatim from e2b_unseal.py)

- Sample: selection cascade of E2B-CALIBRATION-REPORT.md (13,233 primary
  pairs; MSMS clarification included).
- PRIMARY: median ṽ_perp ratio [0.1–1] a₀ / [10–100] a₀, R < 0.01
  sample, 10,000 pair-bootstrap CI.
  Anchors: Newton 1.115 [1.070, 1.160]; MOND 1.299 [1.238, 1.356].
- SECONDARY (preregistered in the spec): median ṽ_perp in [0.1–0.3] a₀
  with bootstrap CI. Anchors: Newton 0.682 [0.639, 0.726];
  MOND 0.788 [0.737, 0.841].
- Labeled variants (robustness, not decisive):
  (a) R < 0.1 sample, primary anchors;
  (b) precision-trimmed σ_ṽ < 0.15, anchors Newton 1.009 [0.942, 1.075],
      MOND 1.198 [1.129, 1.274].
- Verdict rule: symmetric. Report point estimates + CIs; state which
  anchor each CI excludes. The PRIMARY decides; variants qualify
  robustness. No re-runs, no post-hoc cuts, no alternative bins.
- Small-N clause: primary n_low < 500 → reduced-power flag
  (counts already known: n_low = 1,377 — clause will not trigger).

## What is sealed

All ṽ_perp statistics at g_N < 10 a₀: 5,093 primary pairs, of which
1,377 in the decision bin and 479 in the flicker bin. Their individual
ṽ values exist only inside the committed arrays and have never been
aggregated, printed, plotted, or inspected. Only counts and error
distributions (σ_ṽ, computable blind from PM errors) were used in
calibration.

## Power statement (declared before looking)

With n_low = 1,377 the expected bootstrap CI half-width on the primary
ratio is ≈ ±0.04–0.05 (from the calibration-region variance). The
Newton and MOND anchors are 0.18 apart. If the universe is Newtonian in
the sealed bin, the MOND anchor should be excluded with high confidence,
and vice versa. An intermediate result excluding neither will be
reported as such — symmetric reporting is the point of the ritual.

## Anchoring checklist (owner)

1. `git tag pre-unseal-e2b && git push origin main --tags`
2. `git archive pre-unseal-e2b | sha256sum` → record tree hash.
3. OpenTimestamps-stamp the tag/commit hash (as done for pre-unseal-v1).
4. Reply "unseal e2b" — the sealed computation then runs exactly once.
