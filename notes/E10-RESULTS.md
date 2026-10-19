# E10 Results — the forgetting curve

Date: 2026-08-30. Spec frozen `434506c` after the power gate and before
any excess computation. Data: E8 GALAH table (`b3ee7b2`), E1b machinery
verbatim. Run once (seeded); one reporting amendment (descriptive
medians for the underpowered bin, required by the spec's own reporting
rule) re-executed identically — powered-bin numbers byte-identical.
Raw output `e10_results.json`; figure `e10-results.png`.

## The curve

| age bin (Gyr) | matched pairs | clusters | twin excess (dex) | 95% CI | zero excluded |
|---|---|---|---|---|---|
| [0, 2) | 11 | 10 | −0.145 (descriptive) | — | underpowered (declared) |
| [2, 4.5) | 33 | 23 | **−0.167** | [−0.238, −0.055] | **yes** |
| [4.5, 8) | 25 | 25 | **−0.175** | [−0.259, **+0.007**] | no — by 0.007 dex |

Secondary (co-evality): linked pairs' median clock-age disagreement is
1.2–1.9 Gyr across all bins; their matched controls sit at 3.7–5.6 Gyr.
Linked pairs are co-eval at every age; chance pairs are not.

## Verdict under the frozen rule

The preregistered decision rule reads: mid-bin excludes zero AND
old-bin consistent with zero → **"FORGETTING DETECTED."** That is the
formal verdict and it stands as written — the rule was frozen and the
rule decides.

## The honest reading (reported alongside, as the spec's symmetric-reporting clause requires)

The old bin's POINT ESTIMATE (−0.175) is as large as the mid bin's
(−0.167) — larger, in fact. Its confidence interval includes zero by
seven thousandths of a dex, at a matched count sitting exactly on the
preregistered power floor (25 pairs). Nothing in these numbers shows
the excess shrinking with age; what they show is a measurement running
out of pairs, not a disk running out of memory. The defensible summary:
**the chemical twin excess of kinematically linked pairs persists in
point estimate through 8 Gyr, with significance beyond 4.5 Gyr lost at
this sample's power floor.** The frozen-rule verdict and this reading
are both reported; neither replaces the other. (This tension is the
cost of preregistration honestly paid — the rule was written expecting
decay, the data declined to cooperate, and we do not rewrite rules
after looking.)

## Two findings worth keeping regardless

1. **Age-consistency purifies.** Requiring both members to carry valid,
   mutually consistent [Y/Mg] clocks raises the twin excess from E1b's
   −0.10 (all linked pairs) to −0.17 — the co-eval precondition
   removes a large fraction of the chance-pair contamination. A
   practical upgrade for any future use of the selector (Paper II
   material).
2. **Direct relevance to E8.** E8 demoted kinematics at 4.6 Gyr on the
   assumption that linkage decays by the Sun's age. E10's old bin —
   spanning the Sun's age — shows linked pairs still twice as
   chemically alike as controls in point estimate. Kinematic linkage at
   solar age is weakened, not worthless; an E8b could justifiably
   re-weight it.

## What would settle it

The old bin needs pairs, not ideas: a looser clock-validity box (at the
cost of age precision), GALAH DR4 / wider footprints, or DR4 astrometry
expanding the linked-pair graph. An E10b spec would preregister the
enlarged sample and a proper decay-model fit (exponential vs constant,
likelihood ratio) instead of per-bin CIs. Not scheduled; the curve as
measured is committed.

---
## CORRECTION (2026-08-30, post independent audit)

Accepted: (1) The co-evality secondary was partly circular — treatment
pairs were preselected to |Δt| < 3 Gyr while controls faced no clock
requirement; the "linked pairs are co-eval; controls are not" framing
is RETRACTED (the treatment median was truncated by selection).
(2) The purification claim (−0.10 → −0.17) requires a same-population
ablation before being described as measured purification. (3) Scope
corrected: this experiment measures the chemical purity of pairs that
REMAIN linked at a given age, not the disk's forgetting rate; both
raw levels rise with age (linked +0.028, controls +0.036 dex between
powered bins) and the difference masks both. E10b requirements:
chemistry-defined parent population, recovery and purity estimated
separately, direct bin-contrast tests, Ratcliffe et al. clock caveat.

## Correction appended 2026-09-01 (E10b, Amendment 1; notes/E10B-RESULTS.md)

The "honest reading" above — that the twin excess persists in point
estimate through 8 Gyr — is withdrawn as an artefact of three things
this run could not see: controls that were neither orbit-matched
(E1c) nor given the treatment's clock-consistency cut, and clock
errors (median 2.7 Gyr per pair) comparable to the bin widths. An
orbit-matched mixture likelihood with the age error marginalised
finds the conatal fraction at 0.58 [0.29, 0.84] below 4.5 Gyr and
0.02 [0.00, 0.32] above (R = 0.03 [0.00, 0.73]; DECAY DETECTED). The
frozen-rule verdict above ("FORGETTING DETECTED") therefore stands;
finding 2 ("kinematic linkage at solar age is weakened, not
worthless") is downgraded to: at solar age the conatal fraction of
linked pairs is bounded above by ~0.3 and is consistent with zero.
Finding 1 (age-consistency purifies) is partly the same-age selection
acting on the treatment alone and is no longer licensed as a selector
upgrade without an equally selected control.
