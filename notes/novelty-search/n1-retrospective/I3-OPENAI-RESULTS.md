# N1 retrospective — OpenAI I3 results

Date: 2026-08-31. **Completed: 42 judgments, seven claims, two stances,
three fresh sessions per claim and stance.** Runtime metadata identifies
OpenAI `gpt-5.6-sol`, reasoning `xhigh`. All 42 responses say NOT-NOVEL.
This is descriptive, contamination-flagged retrospective evidence only;
it licenses no C1–C6 conclusion and changes no ground-truth label.

The execution addendum and exact intended inputs were committed at
`470ab5a15a320392910fbed6e74b8250205976c7` at 15:39:25 UTC, before the first
dispatch at 15:39:37 UTC. The last response completed at 15:52:58 UTC.
Original specification, prompts, packets, Claude results, and this run's
frozen addendum all retain their pre-run SHA-256 hashes.

## Scores against the frozen ledger

| Cell | Verdict accuracy | Strict locate, provisional | Generous mechanism-family match, provisional | Mean verdict confidence | Mean p(NOVEL) | Brier |
| --- | --- | --- | --- | --- | --- | --- |
| I3-att | 18/21 = 85.7% | 8/18 = 44.4% | 18/18 = 100% | 90.05% | 9.95% | 0.12307 |
| I3-val | 18/21 = 85.7% | 7/18 = 38.9% | 18/18 = 100% | 93.10% | 6.90% | 0.13676 |

**The accuracy equals the always-NOT-NOVEL baseline.** There are six
ANTICIPATED claims and one UNLOCATED claim, and both stances classify every
claim identically. The apparent improvement over the earlier Claude
15/21 results comes entirely from CLM-4; it is not evidence of useful
binary discrimination on this set.

The in-sample constant probability p(NOVEL)=1/7 has Brier 0.12245; the
fully certain always-NOT-NOVEL baseline has Brier 0.14286. Neither OpenAI
cell beats the empirical-prevalence probability baseline. That baseline
uses the observed class mix, so it is a descriptive reference, not an
out-of-sample predictor. Mean confidence is confidence in the selected
verdict; it must not be mistaken for novelty confidence.

Claim-clustered bootstrap, 1,000 resamples, seed 20260831: accuracy 95%
interval 57.1–100% for both stances; strict locate 11.1–77.8% for attack
and 5.6–72.2% for validate; Brier 0.00637–0.34139 and 0.00285–0.39403,
respectively. Full intervals are in [the generated table](openai-i3/RESULT-TABLE.md).
The generous match bootstrap returns 100–100% because every included
observation was coded 1. This is a degenerate resampling result, not
certainty about true locating performance or the correctness of the coding.
Seven claims, or six for locate, are the resampling units; several claims are related, so their independence is not established.

## What the judges located

Every claim received six NOT-NOVEL verdicts. CLM-6 therefore received six
scored errors; all other claims received six scored correct verdicts.

| Claim | Strict attack | Strict validate | Observation |
| --- | --- | --- | --- |
| CLM-1, comoving chemistry | 3/3 | 1/3 | All attack samples name Kamdar; two validate samples name other observational chemistry work. |
| CLM-2, reporting law | 0/3 | 0/3 | No Olson 2022. Judges identify causal diamonds or round-trip computation/resource constraints. |
| CLM-3, pairwise/common receiver | 2/3 | 3/3 | Five explicitly name Čech–Vietoris–Rips; the sixth names Čech nerves versus clique/flag complexes and gives the same distinction. |
| CLM-4, moving archives | 0/3 | 0/3 | All describe the Brunn–Minkowski/difference-body or central-section volume argument; none identifies Olson reporting ancestry. |
| CLM-5, weighted archives | 3/3 | 3/3 | All identify common-receipt convex/minimax/one-center geometry and higher-order constraints. |
| CLM-6, wide-binary design | NA | NA | All identify standard simulation-based calibration; none establishes the exact sealed four-statistic protocol. |
| CLM-7, reflexive predictability | 0/3 | 0/3 | All name Argyris action science; none names Bloor. |

The clearest local difference from the earlier Claude report is CLM-3:
OpenAI explicitly names Čech–Rips in 5/6 outputs, whereas the earlier
report recorded 0/9. However, OpenAI names Bloor in 0/6, compared with
9/9 in that report, and still misses Olson in every CLM-2 output.
Different retrieved literature is observable; a general cross-lab
advantage is not established. These comparisons use the existing Claude
report as supplied, without reconstructing its missing full reasoning.

On CLM-4 the binary verdict changes while the described mathematical
ancestry largely agrees. OpenAI consistently treats the core
symmetrization mechanism as established and leaves the specific
cosmological application or union formula potentially original. The
earlier Claude report described NOVEL judgments that also recognized
classical ingredients. This difference can arise from the mechanism-versus-
application boundary without any new prior-art discovery.

CLM-6 remains a scoring/construct warning. The prompt asks about the
core mechanism, while the ledger's UNLOCATED status protects a specific
preregistered design at its date. OpenAI calls noise calibration standard
and distinguishes it from the complete protocol. Its mean confidence on
this scored error is 87.67% under attack and 95.00% under validate. The
label remains unchanged: this run does not adjudicate the competing scope
interpretations or the underlying gravity question.

## Locate coding requires owner review

All locate numbers are **provisional orchestrator codings**, with a reason
for each response in [LOCATE-CODINGS.json](openai-i3/LOCATE-CODINGS.json).
No owner ratification or new bibliographic verification has occurred.

The generous column follows the earlier report's permissive practice of
crediting described mechanism families and alternative antecedents. It
must not be presented as verified location of the actual anticipating
work required by the original primary endpoint. In particular, causal
diamonds do not prove that the named paper contains Olson's exact
arbitrary-speed formula, and Argyris is not identification of Bloor.
Several judges explicitly acknowledge those limits.

Two transparent sensitivities illustrate the coding dependence:

- Counting the Čech-versus-clique/flag response as a strict equivalent
  changes attack strict locate from 8/18 to 9/18 (50%). The main count
  conservatively requires the explicit Vietoris–Rips name.
- Withholding generous credit for the six Argyris responses until they
  are accepted as anticipating equivalents changes generous matching to
  15/18 (83.3%) in each stance. Further source-level adjudication could
  also change other generous codings.

CLM-4 strict coding preserves the prior report's convention: classical
inequalities alone do not count without the Olson reporting ancestry.
CLM-5 instead has a mathematical-slot reference standard. These differing
reference granularities limit interpretation of a single aggregate
strict percentage. They were disclosed before OpenAI judging; no rule
was silently revised to favor the new outputs.

## Integrity and limits

- 42 distinct subagent runtime sessions, each with `fork_turns="none"`,
  one incoming task message, no follow-up, no model override, and zero
  observed tool calls. All final responses meet the requested format and
  150-word reasoning limit. No discard, replacement, or retry occurred.
- Isolation remains instruction-enforced for tools/files. Standard
  harness instructions, the working-directory/plugin environment, and
  routing names remain present. Claim indices appear in routing names;
  no adjudications, semantic claim headings, prior outputs, or research
  conversation were included in the task payloads.
- Actual model/effort were discovered in runtime records after the
  first dispatches, rather than pinned in advance. Temperature is not
  exposed or controlled. The OpenAI I3 designation follows the supplied
  Claude-family handoff; per-claim generation lineage was not independently
  reconstructed. This is not a controlled model-identity experiment.
- Local logs encrypt task payloads. All 42 encrypted parent payloads
  match their corresponding child deliveries. Plaintext-to-frozen-input
  hashing cannot be independently performed on those encrypted logs;
  the intended plaintext inputs are frozen and the submitted text is in
  the root tool calls. The initial checker falsely treated ciphertext as
  plaintext; it was corrected, and the outputs are unchanged.
- Orchestrator and scorer knew ground truth and the earlier Claude
  results; judges were not given that material. Familiarity/contamination,
  packet authorship, small claim count, mixed label scopes, and correlated
  repeats remain limitations. Assertions of prior art in raw responses
  are model outputs, not verified new evidence.

For a future, separately frozen prospective run, settle mechanism-level
versus complete-configuration labels and exact-source versus equivalent-
mechanism locating criteria before collecting judgments. This report
does not amend the current spec, justify changing the prospective design,
or establish whether session commitment or lab identity causes failures.

Gemini, I1, R, prospective claims, and new G searches were not run.

## Artifacts and reproduction

- [Complete verbatim final responses](I3-JUDGMENTS.md).
- [Pre-dispatch addendum](I3-OPENAI-MANIFEST.md).
- [Machine-readable scores](openai-i3/SCORES.csv) and [summary and intervals](openai-i3/SCORES.json).
- [Frozen inputs](openai-i3/inputs/) and [verbatim outputs](openai-i3/raw/).

SCORES.csv records the SHA-256 of every frozen input and every response.
Scientific adjudication of the provisional locate coding remains the owner's step.
