# N1 retrospective arm — RESULTS (descriptive; contamination-flagged; no C1–C5 verdicts)

Date: 2026-08-31. Executed under the frozen MANIFEST.md and PACKETS.md
(committed before any judge ran). 63 judgments: 7 claims × 3 cells
(I2-val, I2-att fable; X1-att sonnet exploratory) × k=3. All judges
isolated, closed-book by instruction, zero tool uses recorded in every
run. Raw verdict/confidence/prior-art lines preserved in
RAW-JUDGMENTS.md; full reasoning texts for the two total-miss claims
included there verbatim.

## Headline numbers

| Cell | Verdict accuracy | Mean confidence | Brier |
| --- | --- | --- | --- |
| I2-val (fable, validate) | 15/21 = 71.4% | 76.4 | 0.215 |
| I2-att (fable, attack) | 15/21 = 71.4% | 74.8 | 0.202 |
| X1-att (sonnet, attack, exploratory) | 15/21 = 71.4% | 67.5 | 0.179 |
| All | 45/63 = 71.4% | 73.2 | 0.199 |

Reference points: Shahid et al.'s zero-shot cell measured 68% on their
benchmark (not comparable — different set, and this one is
contaminated in the judges' favor); an always-NOT-NOVEL rule scores
85.7% on this class-imbalanced set, BEATING every cell — verdict
accuracy is the wrong headline here, exactly as the MANIFEST
predicted. Locate-rate and the failure geometry are the findings.

## Finding 1 — verdicts were determined entirely by the claim, never by the cell

Within every one of the seven claims, all nine judgments agreed on the
verdict: stance changed nothing, model changed nothing, and the k=3
decoding repeats never split. On heavily contaminated retrospective
material, attack-vs-validate framing and same-lab model distance
produced zero verdict variance — the entire signal (and the entire
failure) lives at the claim level. Sonnet ran systematically less
confident (67.5 vs ~75.6) with the same verdicts, hence its better
Brier: humility, not skill. Consequence for the prospective arm: if
stance and distribution effects exist, they live on uncontaminated
claims; the retrospective arm cannot see them, and nothing here
licenses shrinking the prospective design.

## Finding 2 — both total misses sit exactly in the anticipation/obviousness penumbra

Five claims scored 9/9 correct; two scored 0/9. The two are precisely
the claims whose ground-truth labels straddle the anticipation/
obviousness line:

- CLM-4 (moving-collector optimization; G = ANTICIPATED at mechanism
  level, composite adjudicated "application of established
  mathematics"): all nine said NOVEL — while mostly NAMING the
  classical symmetrization ancestry (Rogers–Shephard/Brunn–Minkowski,
  isodiametric) and reasoning "ingredients classical, composite
  unlocated." That is materially the ledger's own final language,
  forced through a binary that has no "as-application" option.
- CLM-6 (E2b design; G = UNLOCATED at date): all nine said NOT-NOVEL,
  arguing noise-injected forward-modeled anchors are standard practice
  in the Chae/Banik/Pittordis–Sutherland literature and the sealed
  preregistration is "procedural packaging." The ledger's licensed
  claim is the executed preregistered instance, not the mechanism
  family — again the binary forced a side.

The binary NOVEL/NOT-NOVEL format failed exactly where Part II's
anticipation/obviousness distinction lives, and nowhere else. This is
direct retrospective support for the verdict-tier output (proceed-as-
novel / as-application / as-replication / decline) over any binary
gate, and for facet-level scoring: at the slot level, judges and
ledger substantially agree on both miss claims.

- Calibration detail: the CLM-6 misses carried the study's HIGHEST
  confidence (mean 79.7 — confidently wrong); the CLM-4 misses its
  lowest (59.3 — wrong but hedged). Mean confidence when correct,
  74.3; when incorrect, 69.5. Confidence was nearly useless as a
  wrongness signal, driven by two opposite-signed failures.

## Finding 3 — the vocabulary-translation failure replicates, now in the judges

Strict locate-rate (naming the ledger's adjudicated prior) vs material
locate-rate (describing mechanism-anticipating published work) on the
six ANTICIPATED claims:

| Claim | Strict | Material | What was named instead |
| --- | --- | --- | --- |
| CLM-1 (Nelson/Kamdar) | 9/9 | 9/9 | the actual literature, precisely |
| CLM-2 (Olson 2022) | 0/9 | 9/9 | Ord 2021 round-trip half-horizon, Heyl 2005, causal diamonds |
| CLM-3 (Čech–Rips) | 0/9 | 9/9 | Helly's theorem, common-knowledge results, common-cause literature |
| CLM-4 (Olson + isodiametric) | 0/9 | ~7/9 | the classical inequalities, without Olson/Gardner |
| CLM-5 (Helly/convex/causal cones) | 9/9 | 9/9 | Helly, weighted 1-center/SOCP, Kent/Hayden–May summoning |
| CLM-7 (Bloor) | 9/9 | 9/9 | Bloor's strong programme, by name, in every judgment |
| Total | 27/54 = 50% | ~52/54 = 96% | |

The mechanism is almost always found; the ledger's exact citation is
found half the time, and the misses are translations — the same
insight located under a different field's name (Helly for Čech–Rips;
Ord's geometry for Olson's reporting law). This replicates, in the
judges, the project's own Čech–Rips vocabulary miss, and quantifies
Part II's rule: cross-vocabulary translation is where closed-book
search dies. Note the ledger itself called Čech–Rips the insight's
"native frame" — the judges' unanimous Helly identification is a
defensible alternative native frame, worth recording in the ledger.

## Finding 4 (the sleeper) — the knowledge was in the weights; the failure was in the session

CLM-1 and CLM-7 are the two claims whose generating sessions
experienced full felt novelty (the comoving-chemistry idea; the RPP
essay). Fresh-session judges from the same model family, closed book,
identified both as reconstructions instantly, unanimously, with the
correct citations — Kamdar/Nelson at mean confidence ~92, Bloor at
~65. The generator family demonstrably CONTAINED the deflating
knowledge; what failed in the original events was not retrieval
capacity but the generating context. Tentative but pointed: felt
novelty may be a property of the generating session state (commitment,
in-context momentum) at least as much as of the distribution — which
elevates N1's C3 contrast (I1 in-context vs I2 fresh-session) from
control to the single most interesting prospective measurement, and
suggests the cheapest gate of all may be "ask the same model again,
fresh, before believing yourself."

## Deviations and integrity notes

R anchor deferred (per MANIFEST, dated reason). One X1 run on CLM-5
returned with an unevaluated-safety-review warning from the harness;
its output was a normal verdict block with no anomalies and is
retained, flagged in RAW-JUDGMENTS.md. Two judge claims warrant
owner-side kill-budget verification before any reuse: (a) one X1
judgment asserted Pittordis & Sutherland ran a preregistered
timestamped Gaia DR3 wide-binary analysis — if true it tightens the
CLM-6 penumbra reading, if confabulated it is itself a datapoint on
attack-stance overreach; (b) the CLM-2 judges' repeated attribution of
the half-horizon/one-eighth result to Ord 2021 should be checked
against the actual text. Packet authorship bias stands as recorded.
Zero tool uses in all 63 runs supports instruction-enforced isolation
holding.

## What this arm licenses (and does not)

Licensed: the descriptive findings above; the recommendation to score
facets and use verdict tiers; the elevation of C3 in the prospective
arm; the vocabulary-translation quantification. Not licensed: any
C1–C5 verdict (contamination biases judge performance upward and the
set is class-imbalanced 6/1); any claim about I1 (not run); any
stance or identity effect (none observable through the contamination
ceiling). The prospective arm's design stands unchanged, with C3
flagged priority.
