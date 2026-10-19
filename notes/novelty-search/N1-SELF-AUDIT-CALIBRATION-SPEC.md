# N1 Spec — can a generator audit its own novelty? (FROZEN)

Date: 2026-08-31. First experiment of the novelty lane proper (N =
novelty-lane experiments; E = astronomy experiments; M = modules).
Freeze occurs at commit. Cross-referenced to the project's novelty
protocol and its open-question protocol memo (P1, P3, P5, and the
preregistered falsifier tranche); neither is part of this record.

## The empty cell this fills

Measured territory nearby: LLM evaluators favor their own generations
on quality tasks (Panickssery-Bowman-Feng, NeurIPS 2024,
arXiv:2404.13076); unaided LLM novelty judgment of OTHERS' ideas runs
0.68 accuracy vs 0.81 retrieval-grounded (Shahid et al.,
arXiv:2506.22026, Table 1). Unmeasured: a generator judging the
novelty of its OWN ideas against adjudicated prior-art ground truth.
P1 of the protocol memo asserts the strong form (self-assessment
carries no evidential weight); the assertion currently rests on
direction-only evidence. This spec measures magnitude — and untangles
the confound inside this project's own observation, where an observation that the generator's own audits underperformed
a different model's conflated judge identity with stance framing.

## Design: judgment cells per claim

Factors, crossed:

- IDENTITY: I1 generator model, in-context (the session that produced
  the idea judges it; prospective claims only — unrecoverable
  retrospectively); I2 generator model, fresh session, no generation
  context; I3 different-lab model, fresh session.
- STANCE: S-val "assess whether this idea is novel"; S-att "this idea
  is probably not novel; find the prior art; your success metric IS
  finding it."

Six cells (I1–I3 × S-val/S-att), k=3 samples per cell per claim
(decoding variance averaged; temperature and model versions pinned in
MANIFEST at freeze). Plus two anchors, run once per claim:

- R: retrieval-grounded judgment (facet decomposition, multi-channel
  search, facet rerank, grounded verdict — the Part II pipeline),
  expected ≈0.8 per Shahid et al.
- G: ground truth — kill-budget adversarial search (fixed budget: 2
  hours or 40 queries, whichever first, across ≥3 search modalities
  WITH the mandatory cross-vocabulary translation step) by a lane
  used as NO judge cell, then operator-ratified. Labels: ANTICIPATED
  (published work anticipates the mechanism facet) / UNLOCATED
  (treated as novel for scoring, under the known ~1-in-5 miss
  ceiling) / DISPUTED (excluded, recorded).

No judge cell receives tools, repo access, or deflation context; each
receives the claim sanitized to: background context, the idea, its
facet decomposition (purpose/mechanism/domain/method/data). Verbatim
judge prompts frozen in prompts/ at commit; changes after freeze void
the affected cells.

## Outputs per judgment

1. Verdict: NOVEL / NOT-NOVEL (prior art anticipates the mechanism).
2. Confidence 0–100.
3. Named or materially described candidate prior art, if any.

Two scoring rules, both preregistered: VERDICT-ACCURACY (binary,
against G) and LOCATE-RATE (among truly ANTICIPATED claims, the
judgment names or materially describes the actual anticipating work —
operator-adjudicated against G's report). Locate-rate is the harder
and more meaningful number: the deflations show generic skepticism is
cheap and locating the actual prior is what was missed. Calibration:
Brier score per cell, claim-clustered bootstrap ×1000 for all CIs
(the k=3 samples within a cell-claim are correlated; the claim is the
cluster).

## Claim sets

RETROSPECTIVE (I2/I3 cells only; contamination-flagged — the priors
and possibly the deflation records are in training substrates; scored
separately, never pooled with prospective): the adjudicated ledger
cases — comoving-chemistry (ANTICIPATED, Nelson 2021), v/(1+v)
reporting law (ANTICIPATED, Olson 2022), pairwise-vs-common-receiver
(ANTICIPATED, Čech–Rips), collector extension (ANTICIPATED, Olson
2022), weighted-archives (slot-anticipated), E2b framing (UNLOCATED
at its date), RPP (ANTICIPATED, Bloor 1976). The generator-family model stands in for I2; in-context I1
is gone and is not simulated.

PROSPECTIVE (all cells): every candidate claim in the memo's
preregistered falsifier tranche, instrumented at birth
BEFORE any search runs: six judgment cells + R recorded first, then
G. Regeneration frequency (P3: N=5 lanes × k=3, background without
the idea, mechanism-facet match adjudicated by a non-generator lane)
recorded in the same sitting, so N1 doubles as P3's calibration
study.

## Preregistered contrasts (symmetric; all honorable)

- C1 IDENTITY: I3-att vs I2-att on verdict-accuracy and locate-rate.
  P1-strong predicts I3 ≫ I2 (distribution blindness survives attack
  framing).
- C2 STANCE: I2-att vs I2-val. The stance hypothesis predicts the
  gap lives here — attack framing rescues the self-distribution.
- C3 COMMITMENT: I1 vs I2, stance-matched (prospective only) —
  separates in-context investment from distribution blindness.
- C4 ANCHOR: R vs the best unaided cell (expected ≈0.81 vs ≤0.68).
- C5 DIRECTION: generator's mean novelty confidence on own claims vs
  I3's on the same claims — the self-preference prediction
  (overrating) tested in the novelty domain.
- C6 REGENERATION: correlation of regeneration frequency with
  ANTICIPATED status across prospective claims — P3's blade test.

Outcome map (each updates a named instrument; none is a failure):

- Identity dominates (C1 large, C2 small): P1 strong form confirmed;
  protocol step 4's different-distribution requirement is
  load-bearing; P3's lane-independence kill criterion tightens.
- Stance dominates (C1 small, C2 large): the cheap rescue — a solo
  operator gets most of the protection by re-prompting the generator
  as attacker; protocol step 4 relaxes; P1 downgrades to stance
  hygiene.
- Both large: the protocol keeps both requirements; magnitudes set
  the discount factors.
- Neither (self-val ≈ everything else): P1's corollary overreaches
  and is weakened to direction-only in the memo — recorded, not
  buried.
- C6 null: regeneration frequency fails its blade test; P3 dies per
  its own kill criteria regardless of C1–C5.

## Power floor (no decision below it)

≥8 prospective claims with ratified G labels; ≥3 ANTICIPATED and ≥3
UNLOCATED among them (accuracy is meaningless without class balance);
≤30% DISPUTED. Below floor: record UNDERPOWERED, extend the tranche,
no verdict. Retrospective set reports regardless, contamination
flag attached, as descriptive context only. Expected effects are
large (tens of points) or absent; at n=8–15 claims × k=3, exact
binomial CIs and claim-clustered bootstrap suffice — no significance
theater beyond the stated intervals.

## Sunset clause

If after two tranches the floor is unmet or G labels cannot be
ratified at the required rate, P1 reverts permanently to
direction-only status in the protocol memo rather than pending
indefinitely — an unmeasurable strong claim does not get to live as
an asserted one.

## Follow-on (named, not specced)

N2 — novelty-biased generation: generate k=10 candidates per
background, rank by cross-distribution regeneration frequency, kill-
budget both extreme quartiles, compare survival. GATED on C6
validating the signal. Prior-art routing already on file: novelty
search and quality-diversity in evolutionary computation
(Lehman-Stanley), curiosity-driven RL — the pressure is old; only
the metric is candidate-new.

## Provenance

Lineage at freeze: this spec + verbatim prompts + MANIFEST (model
IDs, versions, temperatures, budgets) committed together; OTS anchor
at the owner's discretion per the precommitment chain. Judges and
the G lane must be named in MANIFEST before the first prospective
claim is instrumented. Amendments after freeze follow the E12c
pattern: a dated amendment file, never an edit to this one.
