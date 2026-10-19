# N1 retrospective — OpenAI I3 execution addendum

Date: 2026-08-31. This addendum is committed before any OpenAI I3 judge
is dispatched. Original specification, packets, prompts, labels, and
Claude results remain unchanged. Scope: retrospective, descriptive,
contamination-flagged; no C1–C6 or prospective decision.

## Execution

- Source HEAD at preparation: 93067bf862e186ba793159a365c9c541795a85ae.
- Packet/prompt freeze: 98bc835; study specification: e972ae7.
- OpenAI Codex is the different-lab judge relative to Claude generators.
  Subagents inherit the current runtime model and reasoning settings;
  no model override is requested. Exact model/version and decoding
  temperature are not verifiable through the available harness. Record
  these as unknown/default, not as an invented pinned model identity.
  Consequently this is an OpenAI Codex replication, not a version-pinned
  model benchmark. Session/runtime identifiers are retained where exposed.
- Seven claims, attack then validate, three fresh subagents per claim and
  stance: 42 planned judgments. `fork_turns="none"` on every dispatch.
  One judgment per subagent; no re-use and no feedback to judges.
- Each subagent receives exactly the frozen stance prompt with the
  BACKGROUND/IDEA/FACETS packet substituted, with no heading, claim ID,
  ledger, outcome, prior response, or added experimental context.
- Conversation separation is harness-supported. Tools and shared files
  remain technically available, so closed-book/file isolation is enforced
  by the frozen instruction, not by a sandbox. No claim of physical or
  statistical independence of samples is made.
- Preserve full final responses verbatim. Retain observed tool use and
  formatting failures separately. A tool-using response is excluded under
  I3-PACKETS.md; any replacement uses the identical frozen prompt, and
  both attempts are retained. Up to one replacement per invalid judgment;
  remaining failures are missing, never silently filled.
- No external retrieval during judging or scoring. Named citations are
  judge assertions, not newly verified bibliographic evidence.
- Gemini is outside this OpenAI execution; I1, R, prospective judgments,
  and new ground-truth adjudication are not run here.

## Analysis fixed before I3 outcomes

Ground-truth labels remain the original six ANTICIPATED plus CLM-6
UNLOCATED. Use the binary verdict literally even when reasoning offers
an application/composite qualification. With c=confidence/100,
p(NOVEL)=c for NOVEL and 1-c for NOT-NOVEL. Brier=(p(NOVEL)-y)^2,
where y=1 for UNLOCATED and 0 for ANTICIPATED. Report novelty probability
separately from confidence in the selected verdict. Baselines: always
NOT-NOVEL accuracy 6/7; fixed p(NOVEL)=1/7 Brier 6/49 (in-sample).

Locate-rate follows the original generous material criterion, separately
from strict citation matching. Score all six ANTICIPATED claims regardless
of verdict. Human-readable per-response rationales accompany the scores;
all locate judgments are provisional orchestrator codings requiring owner
ratification. Scorer has read the ground truth and prior Claude results.

Strict matching follows the earlier RESULTS.md's actual coding for
comparability: CLM-1 Kamdar/Nelson observational pair-chemistry work;
CLM-2 Olson 2022 reporting law (author/topic alone without identifying the
work is insufficient); CLM-3 explicit Cech versus Vietoris–Rips frame;
CLM-4 Olson reporting ancestry together with the classical symmetrization
ancestry (earlier strict table did not credit classical inequalities alone);
CLM-5 Helly/convex common-witness optimization; CLM-7 Bloor's strong programme.
Material matching permits a described anticipating mechanism in an identified
literature/theorem family, including Ord/round-trip cosmological horizons,
Helly/pairwise-versus-joint intersections, classical volume inequalities,
and methodological reflexivity respectively. Mere repetition of the packet
does not count. Mark uncertain matches explicitly rather than treating a
plausible name as verified anticipation. CLM-6 locate scores are NA.

Report per-stance accuracy, locate rates, mean verdict confidence, mean
novelty probability, and Brier, with per-claim counts. Use 1,000 percentile
bootstrap resamples of whole claims (seed 20260831) for 95% intervals;
resample six ANTICIPATED clusters for locate and seven for other metrics.
Comparisons to the earlier Claude summary are descriptive only; do not
manufacture missing raw reasoning, exact material codings, or paired CIs.
The seven claims, not the 42 repeated samples, define effective diversity.

## Deviations and preservation

This is a dated extension of the original I3 plan (I3-PACKETS.md) to
isolated Codex subagents. Unknown exact model settings, available-but-prohibited tools,
and unblinded orchestration limit reproducibility and blinding. The earlier
Claude results were already public to the orchestrator before this addendum,
but none are supplied to judges. Hash every source and dispatched input,
record dispatch IDs/times, and commit the execution plan before running.
Original files remain unchanged.
