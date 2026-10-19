# N1 — I3 different-lab judge cells (procedure)

The I3 cells require judges from a different lab than the generator
family. Budget: 10–30 minutes per model pass.

## Procedure

1. Fresh chat per judgment (no memory of prior packets; disable
   memory/personalization if offered). Turn OFF browsing/tools —
   these are CLOSED-BOOK cells; if the model searches anyway, discard
   and note it.
2. For each claim CLM-1 … CLM-7 in PACKETS.md: paste one of the two
   frozen prompts below, replacing {PACKET} with the packet text
   verbatim (BACKGROUND + IDEA + FACETS, nothing else — no claim ID,
   no project context).
3. Cells to run, in priority order: I3-att × all 7 claims in each of
   two models (ChatGPT, Gemini) — that is the decision-relevant cell.
   If budget allows, add I3-val the same way. k=1 per model per
   stance is acceptable for this arm; k=3 preferred.
4. Record each response verbatim (verdict/confidence/prior-art/
   reasoning) in a new file I3-JUDGMENTS.md next to this one, with
   model name, version if shown, date, and stance. Do not correct or
   annotate responses inline.
5. Comparison of interest once recorded: on CLM-2 and CLM-3, do
   different-lab judges find the strict citations (Olson 2022
   arXiv:2208.07871; the Čech–Rips / random-geometric-complexes
   frame) that all 18 same-lab attack judgments missed? That is the
   cleanest retrospective test of whether vocabulary translation
   improves with training-distribution distance. On CLM-4 and CLM-6,
   do they land on the same side of the binary as the same-lab cells
   (claim-driven), or split (cell-driven)?

## Frozen prompt — S-att (attack stance)

You are a red-team prior-art hunter. Your success metric IS finding
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
{PACKET}

## Frozen prompt — S-val (validate stance)

You are assessing a research idea for a project ledger. Below is a
claim packet: background, the idea as generated, and a facet
decomposition. This is a CLOSED-BOOK judgment: do not use any tools,
web search, file access, or code execution — judge only from your own
knowledge. Question: is the idea's core MECHANISM novel, or does
published work anticipate it? Reply in exactly this format:
VERDICT: NOVEL | NOT-NOVEL
CONFIDENCE: <0-100, that your verdict is correct>
PRIOR-ART: <name or materially describe the closest published work, or NONE>
REASONING: <max 150 words>
{PACKET}
