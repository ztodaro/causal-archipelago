# E1b Results — chemical genealogy at kiloparsec scale: CONFIRMED

Date: 2026-08-30. Spec: E1B-SPEC.md frozen at `ec12d01` before data
retrieval. Intake: `83b59c4` (GALAH 318,005 rows; APOGEE 233,205 rows;
CG members 55,466). Pipeline: `e1b_run.py`; raw output
`e1b_results.json`; figure `e1b-results.png`.

## Frozen decision rule (restated)

Per survey: CONFIRMED requires the star-clustered bootstrap CI on the
median |Δ[Fe/H]| difference (treatment − matched controls) to exclude
zero, with ≥ 30 effective treatment clusters (power floor). Both surveys
CONFIRMED → **confirmed**; one → suggestive; neither at power → kill for
the kpc regime.

## Result

| | GALAH | APOGEE |
|---|---|---|
| clean unmasked stars | 316,016 | 198,007 |
| treatment pairs (matched) | 1,288 | 4,461 |
| control pairs | 12,877 | 42,952 |
| effective treatment clusters | 1,058 | 1,605 |
| median \|Δ[Fe/H]\| treatment | 0.100 | 0.084 |
| median \|Δ[Fe/H]\| controls | 0.201 | 0.188 |
| difference (dex) | **−0.101** | **−0.103** |
| clustered-bootstrap 95% CI | [−0.120, −0.083] | [−0.119, −0.088] |
| p | 2.5×10⁻⁸⁵ | < 10⁻³⁰⁰ |
| verdict | CONFIRMED | CONFIRMED |

**E1b verdict: CONFIRMED.** Both surveys, independently — different
instruments, different wavelength regimes (optical vs near-IR), different
abundance pipelines, largely different stars — find that pairs linked by
the kinematic method are about **twice as chemically alike** as controls
matched on Teff, log g, angular separation, and distance. The effect
size is the same in both (−0.10 dex) and the CIs overlap almost exactly.

## Why this is the strong form of the validation

- The chemistry never entered the pair selection; it is an independent
  witness channel.
- Matched controls remove the boring explanations: the effect is not
  "similar stars have similar chemistry" (controls are equally similar
  in Teff/log g), not a distance or separation artifact (matched), and
  not survey selection (reproduced in two surveys).
- Star-clustered bootstrap means no single rich structure carries the
  result: >1,000 effective clusters in each survey.
- Preregistered: spec, decision rule, and power floor frozen at
  `ec12d01` before the data were pulled; deviations: none.

## Interpretation and bounds

The −0.10 dex twin excess at kiloparsec scale says the method's linked
pairs retain birth-cloud chemical memory far outside the 100 pc pilot
volume — the dissolved-structure signal generalizes in the regime where
most future candidates live. It does not by itself certify any individual
pair (a pair-level posterior would need the full abundance vector), and
RAVE remains barred from these metrics (internal inconsistency,
documented in E1-RESULTS.md). Residual caveat: control matching is on
four covariates; an unmodeled fifth variable correlating with both
kinematic linkage and chemistry cannot be fully excluded, though age —
the obvious such variable — is itself part of the co-natal hypothesis
rather than a confound against it.
