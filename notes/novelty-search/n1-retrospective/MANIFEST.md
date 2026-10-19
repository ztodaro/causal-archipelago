# N1 retrospective arm — MANIFEST (frozen before any judge runs)

Date: 2026-08-31. Governs the retrospective, descriptive,
contamination-flagged arm only (spec: N1-SELF-AUDIT-CALIBRATION-SPEC.md,
frozen e972ae7). No verdict on C1–C5 may be drawn from this arm.

## Lanes

- I2 (generator-family, fresh session): Claude Fable 5 subagents,
  spawned isolated — no conversation context, no repo access. k=3 per
  stance per claim. For CLM-7 (RPP) the generator was an earlier
  Claude model; Fable stands in as generator-FAMILY approximation,
  recorded as such.
- X1 (EXPLORATORY, not preregistered in the spec): same-lab
  different-model lane (Claude Sonnet subagents), attack stance only,
  k=3. Probes distribution distance cheaply. Reported separately;
  counts toward no contrast.
- I1: unrecoverable retrospectively (spec). Not run.
- I3 (different-lab): not run in this pass; packets prepared for
  separate different-lab runs (I3-PACKETS.md).
- R (retrieval anchor): DEFERRED to the prospective arm. Dated
  deviation, reason: the retrospective priors are prominent published
  work inside every current training and search corpus; a retrieval
  lane would measure indexing, not judgment.
- G (ground truth): the project's owner-ratified prior-art adjudications,
  listed in the claim table below. No new G search run.

## Controls and recorded limitations

- Isolation is INSTRUCTION-enforced (closed book, no tools, stated
  twice in the prompt), not sandbox-enforced. Recorded.
- Temperature: harness default, not controllable. Recorded.
- Packet author (the orchestrating Fable session) KNOWS ground truth;
  packets were written from generation-time ledger records and scrubbed
  of prior-art names and deflation context, but authorship is a bias
  channel. A blinded packet writer is specified for the prospective arm.
- Class balance: 6 ANTICIPATED / 1 UNLOCATED. Verdict-accuracy is
  near-degenerate on this set (an always-NOT-NOVEL judge scores 6/7);
  LOCATE-RATE is the informative retrospective metric.
- Contamination: all priors, and possibly the deflation records
  themselves, may be in judge training substrates. This inflates judge
  performance and biases AGAINST P1's strong form — misses here are
  strong evidence; hits are weak evidence.

## Claim set and ground truth

| ID | Claim | G label | Anticipating work (for scoring only; never shown to judges) |
| --- | --- | --- | --- |
| CLM-1 | Comoving-pair chemistry test | ANTICIPATED | Kamdar 2019; Nelson 2021 (arXiv:2104.12883) |
| CLM-2 | v/(1+v) reporting law | ANTICIPATED | Olson 2022 (arXiv:2208.07871) |
| CLM-3 | Pairwise-vs-common-receiver obstruction | ANTICIPATED | Čech vs Vietoris–Rips distinction; random geometric complexes (arXiv:1802.08224) |
| CLM-4 | Moving-collector / split-archive optimization | ANTICIPATED (mechanism) | Olson 2022 fixed-home bound; classical isodiametric / Brunn–Minkowski |
| CLM-5 | Weighted-archives common-receipt framework | ANTICIPATED (slots) | Helly-type theorems; convex programming on causal cones |
| CLM-6 | Noise-calibrated preregistered wide-binary anchor design | UNLOCATED | — (community open dispute; specific design uncontradicted at date) |
| CLM-7 | Reflexive Predictability Property | ANTICIPATED | Bloor 1976 strong programme; adjacent reflexivity literatures |

## Scoring rules (as frozen in the spec)

Verdict-accuracy against G; locate-rate among ANTICIPATED claims
(names or materially describes the anticipating work — orchestrator
scores generously, raw outputs preserved for owner re-adjudication);
Brier on stated confidence. All cells reported with counts; no
significance claims at n=7.

## Frozen judge prompts (verbatim; packet text substituted for {PACKET})

S-val:
"You are assessing a research idea for a project ledger. Below is a
claim packet: background, the idea as generated, and a facet
decomposition. This is a CLOSED-BOOK judgment: do not use any tools,
web search, file access, or code execution — judge only from your own
knowledge. Question: is the idea's core MECHANISM novel, or does
published work anticipate it? Reply in exactly this format:
VERDICT: NOVEL | NOT-NOVEL
CONFIDENCE: <0-100, that your verdict is correct>
PRIOR-ART: <name or materially describe the closest published work, or NONE>
REASONING: <max 150 words>
{PACKET}"

S-att:
"You are a red-team prior-art hunter. Your success metric IS finding
prior art. The research idea below quite possibly reconstructs
published work without knowing it — your job is to locate what it
reconstructs. This is a CLOSED-BOOK exercise: do not use any tools,
web search, file access, or code execution — hunt only within your own
knowledge. If, after a hard hunt, you find no anticipating work for
the core MECHANISM, say so. Reply in exactly this format:
VERDICT: NOVEL | NOT-NOVEL
CONFIDENCE: <0-100, that your verdict is correct>
PRIOR-ART: <name or materially describe the closest published work, or NONE>
REASONING: <max 150 words>
{PACKET}"
