# DR4 freeze bundle — predictions to be timestamped before Gaia DR4 (2 December 2026)

Status: DRAFT for owner freeze (committed as a draft; the tag is the freeze). Nothing here is frozen until
the owner tags, releases and OpenTimestamps it; the external actions
(tag, GitHub release, OTS, any contact with other groups) are the
owner's alone. Target: tag `pre-dr4-freeze` by 2026-11-15; no edits to
the bundle after the tag except dated amendments appended below.

## Why this exists

Gaia DR4 (ESA: "Coming up: 2 December 2026") delivers the 66-month
solution with proper motions several times more precise than DR3,
epoch astrometry and epoch RVs for all sources, and non-single-star
solutions. Every prediction below can be written today from data in
hand and cannot be written after 2 December without losing its value.
This is protocol rule 3 (old open question x newly arrived data) and
replication needs no novelty licence. What we keep either way is the
timestamp.

## B1 — R3 cohort radial-velocity predictions (Crius 227 anchors)

Frozen object: notes/novelty-search/r3-predictions.csv (predicted
line-of-sight velocities for the 22 R3 candidates from the 13 external
Crius 227 anchors, which exclude every candidate) and the lead star
Gaia DR3 4595936858688035968 at -24.24 km/s. File hash recorded at
tag time.

Honesty note: r3-predictions.csv already carries each candidate's
DR3 radial_velocity, and the 2026-08-30 pass found no large
discrepancies, so DR4 does not deliver a first independent RV here.
What DR4 adds is (a) higher-precision RVs (the DR3 errors are 0.2–1.8
km/s on these stars), (b) epoch RV series and non-single-star
solutions, which expose unresolved binaries whose systemic velocity
is not the DR3 value, and (c) RVs for the candidates that lack one.
DR4 test, pre-declared: the number of candidates with
|RV_DR4 - RV_pred| < 3 km/s after removing DR4-flagged binaries,
against the chance rate measured on field stars in the same sky cone,
distance shell and colour range but outside the R3 action window.
Verdict tiers: consistent count above the 95th percentile of chance
(coherence holds at DR4 precision), within chance, or below. A
membership-coherence test, not a birth test; chemistry stays separate.

## B2 — E8b re-sieve of the solar-sibling shortlist

Frozen object: solar-siblings/e8_gold_ranked.csv (221 GOLD, ranked;
frozen 2026-08-30) and E8-CONFIRM-SPEC.md (2809c84), which remains
binding on any analysis of these stars under our name.

DR4 actions: (a) recompute the E8 action window for every Tier-1
candidate with DR4 astrometry and RVs; (b) remove candidates with DR4
non-single-star solutions inconsistent with the sieve's single-star
assumption; (c) add DR4 RVs for Tier-1 stars lacking DR3 RVs.
Pre-declared predictions: the GOLD rank order is frozen and is not
recomputed; we predict the fraction of GOLD stars that remain inside
the action window under DR4 (record the expected fraction from the
injection-completeness machinery before the tag). E8's claim caps hold:
no star becomes a sibling by surviving; the deliverable is a
DR4-cleaned shortlist for the community proposal.

## B3 — Comoving-pair re-selection purity (E1b / E1c)

Frozen object: the E1b treatment pairs (GALAH 1,288; APOGEE 4,461
matched) and E1c's tiered excesses (e1c_results.json).

Physics of the prediction: some fraction of DR3 comoving pairs are
chance alignments admitted by DR3 proper-motion noise. With DR4
proper motions, re-applying the identical selection (dx < 20 pc,
dv < 3 km/s) removes a share of those chance pairs. Pre-declared
prediction: the orbit-matched (C4) twin excess of the DR4-surviving
subset is at least as negative as E1c's C4 value, and the E1b-style
(C0) excess moves toward the C4 value as chance pairs are removed. A
DR4-surviving subset whose C4 excess weakens instead would indicate
that E1c's residual is not birth memory. The numerical prediction
(expected purity gain) follows from the E10b Amendment 1 mixture fit:
if a fraction f of DR3 pairs is conatal and DR4 removes a share q of
the chance pairs, the surviving subset's conatal fraction rises to
f' = f / (f + (1 - f)(1 - q)); the frozen prediction is the sign and
this functional form, with q measured after release and f taken from
the committed E10b results.

## B4 — E2b on DR4, sealed, alongside Boufourou's protocol

Frozen object: E2B-SPEC.md (d0cf4a7) and the anchor machinery
(e2b_cal.py, e2b_inject.py) with their calibration constants.

DR4 plan: apply the identical selection and sealed-bin design to the
DR4 wide-binary sample (the DR4 El-Badry-type catalogue if released;
otherwise our own selection under a spec appended here before the
tag), recompute the pure-Newton and MOND-scale noisy anchors with DR4
per-pair errors, unseal once. Two pre-declared quantitative
predictions under Newtonian gravity: (i) the DR4 pure-Newton anchor
falls below the DR3 anchor (1.115 [1.070, 1.160]) by the amount the
noise model implies for the smaller DR4 proper-motion errors — the
Rice-type bias shrinking is itself a test of the mechanism both we and
Boufourou identified; (ii) the DR4 decision ratio lands inside the DR4
Newton anchor and outside the MOND-scale anchor. The El-Badry
perspective correction flagged after reading Boufourou (arXiv:2608.24556)
must be applied and its effect on the flicker bin quantified before
the tag. Boufourou's Zenodo-timestamped DR4 protocol is the
community's decisive step; ours is a second, methodologically
different preregistered analysis of the same dispute. Whether to
coordinate is the owner's external decision.

## Manifest of frozen inputs (SHA-256 at 33e6723, 2026-09-01)

```
d51ceb1240bea501411e7c2bac6e94e37e159c6871a6e77c60ce22bcf8192bc5  notes/novelty-search/r3-predictions.csv
64576ac5c252623d4bbce029e81b6dc6c1a03c276f4b4c3ca28fcb07b252a93a  notes/novelty-search/r3-prediction-provenance.json
7e98f4004ca216e13801fef97e2693867ec274810ac257dc5c09aa90249c228a  solar-siblings/e8_gold_ranked.csv
1409e5c989c1e951a327a7acc20bd55b12f2ec93fa3a2843e3cc64ae88862afd  solar-siblings/E8-CONFIRM-SPEC.md
36f2c90e552f0ce47b81b19d72bd29caa4bed5121ab56791944e482493271fcc  solar-siblings/e8_sieve.py
af255f205d260ba723b961f0629920db0b47485afba464db5db8d63920520b6d  e1-chemical-genealogy/e1c_results.json
46f6c0ba0a547645cb28d9cd5bf382c88d448fbad2fe4c9a887447ca744d568a  e1-chemical-genealogy/E1C-SPEC.md
d75b330638f8e0675c9e6684541f7f3fb31e888b404e21b5883e99e071d154f7  e2-wide-binaries/E2B-SPEC.md
6aa4611d26da2905cd49f32547133eef6abd14c3a69da875a3423880e5b29330  e2-wide-binaries/e2b_cal.py
cda634a6bb283ea3a9db05ffd581b9567a41e9dc81135a7c2ec693cdb756bf65  e2-wide-binaries/e2b_inject.py
0dfd35a4053bf6dfd921986fd3598d295c705de01709925395769b48c43367ef  e2-wide-binaries/E2B-CALIBRATION-REPORT.md
```

The E10b outputs (frozen run and Amendment 1) join the manifest once
their results memo is committed; B3's numerical prediction is filled
from them before the tag.

## Bundle mechanics

- One directory notes/dr4-freeze/ containing this spec, the frozen
  input files (or their SHA-256 where large), and a MANIFEST.sha256.
- Per-item executable specs and the completeness/mixture
  numbers named above, committed before 2026-11-10.
- Owner: `git tag -a pre-dr4-freeze`, GitHub release with the archive
  hash, OpenTimestamps on the manifest, by 2026-11-15.
- After DR4: each item runs once under its frozen rule; both
  directions of every verdict are reported; retracted numbers are
  appended, never rewritten.

## Amendments (append only, dated)

(none)

- 2026-09-01 (post Deep Check): B3 is a re-selection PURITY
  prediction, P(conatal | selected), and says nothing about physical
  survival; its inputs are the E10b Amendment 1 purity fractions.
  B3's mechanism language must cite Coronado et al. 2020 for the
  orbit–chemistry conditioning it relies on.

- 2026-09-01 (Amendment 2, after the pre-tag audit): (a) An earlier status note said
  the bundle waited only on the tag. That was inaccurate: this document's
  own text names B2 and B4 as pre-tag work, and that stands. (b) Provenance:
  every commit hash cited in this file and in the E1c/E10b memos
  (73ee469, d91ac5f, 33e6723, …) comes from a working copy and is not part of the published history.
  Content SHA-256s, not commit
  hashes, are the anchors this bundle relies on. (c) Hole 4 closed:
  notes/dr4-freeze/MANIFEST.sha256 now exists and lists every frozen
  input, including the E10b files that were placeholders (hole 2
  closed). (d) B2 and B4 remain open, with a hard date of 2026-11-10. Fallback rules, declared now:
  if B2's expected-retention number cannot be produced by that date,
  the number is dropped from the bundle and B2 keeps only the frozen
  ranking and the re-sieve procedure (an un-numbered but still
  timestamped item); B4's perspective correction cannot be dropped —
  it is a correctness requirement of the E2b DR4 rerun and must be
  implemented in the frozen analysis code before any tag. (e) No tag
  of the incomplete draft is requested; one clean operation — tag,
  release, OTS — after B2/B4. The 5.9%
  figure in E8-RESULTS is chemistry completeness under survey
  errors, not DR4 astrometric retention, and must not be reused for
  B2.

- 2026-09-01 (Amendment 3): B2 and B4 executed (B2-B4-SPEC.md, B2-B4-RESULTS.md, scripts and
  JSON beside them). B2 frozen prediction: 218–221 of 221 GOLD stars
  remain inside the Tier-2 action window under DR4 astrometry
  (expectation 219.6; the non-single-star screen is the likelier
  source of attrition and is not modelled). B4: per-pair perspective
  correction implemented and self-tested (1e-16 km/s); on the sealed
  bins the term is subdominant to proper-motion noise (flicker-bin
  P90 delta 0.09 vs PM noise 0.23), shifting the Newton anchors by
  +0.003 (primary) and +0.004 (flicker) with no change in the data's
  position against any anchor; perspective-inclusive anchors are
  frozen here for the DR4 rerun in case RVs are not joined; the RV
  retrieval hand-off is filed in B2-B4-SPEC.md. Both pre-tag holes
  named in Amendment 2(d) are closed. Remaining before the tag: the owner's tag /
  release / OTS on MANIFEST.sha256.
