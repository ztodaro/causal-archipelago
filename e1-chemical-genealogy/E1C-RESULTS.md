# E1c Results — orbit-matched controls for the comoving-pair twin excess: SHRINKS

Date: 2026-09-01. Spec: E1C-SPEC.md frozen at `73ee469` before
execution; script e1c_run.py (SHA-256 b276f718…13cd, recorded in
e1c_results.json) run once in the container holding the E1b inputs;
raw log e1c_run.log; figure e1c-results.png. Lane: Fable 5.1 at owner
instruction; Codex remains technical owner of record and is invited to
reproduce (the run is deterministic: seeds 17 and 1701).

## Reproduce-first gate

C0 re-executed E1b's control construction and statistics verbatim and
reproduced e1b_results.json exactly in both surveys (GALAH −0.1011
[−0.1203, −0.0825], 1,288 / 12,877 / 1,058; APOGEE −0.1034
[−0.1186, −0.0883], 4,461 / 42,952 / 1,605). PASS.

## Tolerances (from the treatment pairs' own kinematics, before chemistry)

| | tau_Lz (kpc km/s) | tau_Jz | tau_Jr | treatment medians |dLz|, |dJz|, |dJr| |
|---|---|---|---|---|
| GALAH | 16.83 | 0.387 | 1.840 | 6.48, 0.110, 0.578 |
| APOGEE | 16.82 | 0.410 | 1.514 | 6.86, 0.093, 0.427 |

## The graded result (S_min = 300 pc; controls Teff ±150 K, log g ±0.3, distance ±150 pc at every tier)

| tier | control definition | GALAH excess (dex) | 95% CI | n treat | APOGEE excess | 95% CI | n treat |
|---|---|---|---|---|---|---|---|
| C0 | E1b: near (<25 pc), dv > 6 km/s | −0.101 | [−0.120, −0.083] | 1,288 | −0.103 | [−0.119, −0.088] | 4,461 |
| C1 | far (>300 pc), orbit-free | −0.104 | [−0.123, −0.084] | 1,277 | −0.116 | [−0.129, −0.102] | 4,245 |
| C2 | + Lz matched | −0.088 | [−0.106, −0.069] | 1,268 | −0.098 | [−0.113, −0.084] | 3,633 |
| C3 | + Jz matched | −0.073 | [−0.094, −0.053] | 1,201 | −0.067 | [−0.082, −0.054] | 2,268 |
| **C4** | **+ Jr matched (full orbit) — PRIMARY** | **−0.055** | **[−0.083, −0.032]** | **874** | **−0.033** | **[−0.049, −0.017]** | **919** |

Control medians fall monotonically as orbit constraints are added
(GALAH 0.201 → 0.204 → 0.188 → 0.175 → 0.159 dex; APOGEE 0.188 →
0.199 → 0.171 → 0.151 → 0.137). Sensitivity: C4 at S_min = 100 pc gives
−0.049 [−0.071, −0.029] (GALAH) and −0.022 [−0.035, −0.009] (APOGEE);
at 1,000 pc both surveys are UNDERPOWERED (72 and 5 pairs) and are
reported descriptively only (−0.157 and −0.187).

## Verdict under the frozen rule

GALAH: C4 interval excludes zero; point estimate −0.055 is above E1b's
upper bound −0.0825 → **SHRINKS**. APOGEE: interval excludes zero;
−0.033 above −0.0883 → **SHRINKS**. Project verdict (weaker of the
two): **SHRINKS**.

## What this means, both directions

- Birth memory is real. Against controls that share the treatment
  pair's guiding radius, vertical action and radial action, kinematically
  linked pairs are still more alike in [Fe/H] than chance, with
  p ~ 1e-23 (GALAH) and 5e-13 (APOGEE). E1b's interpretation survives
  in kind.
- It is about half the size E1b reported, and E1b's control was the
  same kind of control the literature uses (Kamdar 2019: random field
  pairs, dTeff < 200 K; Nelson 2021: pairs minimising dTeff and dlog g).
  Roughly 0.05 dex (GALAH) to 0.07 dex (APOGEE) of the 0.10 dex excess
  is accounted for by orbit coherence — the radial gradient through Lz
  and the disc-population term through Jz carry most of it, with Jr
  adding the rest. The fresh-eyes toy model (random-pair median 0.206,
  same-orbit-no-birth pairs ~0.16) predicted this decomposition to
  within a few thousandths of a dex.
- Pre-declared caveat, in force: orbit-matched controls can contain
  siblings dispersed along the same orbit, which biases C4 toward zero.
  The C4 excess is therefore a lower bound on birth memory and the
  C0→C4 difference an upper bound on the orbit term.
- Composition caveat (not pre-declared; flagged on reading the
  output): only 874/1,288 (GALAH) and 919/4,461 (APOGEE) treatment
  pairs found full-orbit controls, and the APOGEE C4 subset's own
  treatment median (0.105) differs from the full sample's (0.084).
  Part of the APOGEE shrink could be subset composition rather than
  orbit. A labelled post-hoc diagnostic (e1c_diag.py, fresh seed 4242)
  recomputes every tier on the identical C4 subset; its numbers are
  appended in the section below and are descriptive, not
  decision-bearing.

## Licensed and not licensed

Licensed: the tiered table; "the comoving-pair twin excess against
orbit-matched controls is −0.055 [−0.083, −0.032] dex (GALAH) and
−0.033 [−0.049, −0.017] dex (APOGEE), roughly half the value obtained
against the field-pair controls used in E1b and in the published
comparisons"; the statement that no published comoving-pair
homogeneity study located by one lane used orbit-matched controls
(Deep Check on ST-20260901-001 still required before that sentence
leaves the project). Not licensed: any conatal fraction (that is
E10b's job); any statement that Kamdar 2019 or Nelson 2021 are wrong
in kind — their inference survives; their magnitudes need the
orbit-controlled restatement.

## Consequences inside the project

E1b's verdict (CONFIRMED) stands as frozen history; its magnitude is
superseded by this amendment for all forward use. Paper II's
chemistry section must carry the C4 numbers alongside E1b's, with the
orbit-coherence decomposition. E10b proceeds (condition met: SHRINKS)
using the C4 controls as its chance template. Deviations from the
spec: none. Post-hoc additions: the composition diagnostic, labelled.

## Post-hoc composition diagnostic (labelled; e1c_diag.py, seed 4242; descriptive only)

Every tier recomputed on the identical set of treatment pairs that
received full-orbit controls, so that composition and orbit effects
separate:

| tier (same pairs) | GALAH (874 pairs) | 95% CI | APOGEE (919 pairs) | 95% CI |
|---|---|---|---|---|
| C0-style (E1b: near, dv > 6) | −0.100 | [−0.125, −0.078] | −0.081 | [−0.096, −0.066] |
| C1 far, orbit-free | −0.098 | [−0.124, −0.075] | −0.080 | [−0.096, −0.064] |
| C2 + Lz | −0.078 | [−0.104, −0.058] | −0.062 | [−0.079, −0.047] |
| C3 + Jz | −0.071 | [−0.097, −0.048] | −0.045 | [−0.061, −0.031] |
| C4 + Jr (full orbit) | −0.055 | [−0.080, −0.031] | −0.033 | [−0.048, −0.016] |

Reading: in GALAH the C4 subset is representative (its E1b-style
excess, −0.100, equals the full sample's −0.101), so the entire
shrink is the orbit term: orbit matching removes ~45% of the excess.
In APOGEE the subset is not representative — pairs that find
full-orbit controls sit on colder orbits (median Jz 1.07 vs 2.03,
Jr 5.6 vs 11.1 kpc km/s) and nearer (225 vs 405 pc), and their
E1b-style excess is already smaller (−0.081 vs −0.103). Of APOGEE's
apparent −0.103 → −0.033, about 0.022 dex is composition and about
0.048 dex is orbit; on identical pairs, orbit matching removes ~60%.
The pre-declared SHRINKS verdict is unchanged by this decomposition;
what it sharpens is the sentence to carry forward: **on identical
pairs, orbit-matched controls remove roughly half (45–60%) of the
comoving-pair twin excess measured against field-pair controls, and
the remainder is birth memory at high significance in both surveys.**
The sensitivity of the C4 subset to orbit temperature is itself a
lead for E10b's successor: the orbit term is largest for hot orbits,
which is where Jz (population) and Jr (radial migration) carry the
most chemical information.

## Correction appended 2026-09-01 (Frontier Atlas Deep Check, two blind lanes; union report frontier-atlas/intake/DEEP-CHECK-2026-09-01-ORBIT-MATCHED-CHEMISTRY-UNION.md)

The sentence in "Licensed" about no published comoving-pair study
using orbit-matched controls is withdrawn as a broad claim. Orbit–
chemistry conditioning is established prior art: Coronado et al. 2020
(arXiv:2002.09496) measure pairwise [Fe/H] similarity as a function
of action–angle distance against a smooth phase-mixed mock — the
equivalent counterfactual to E1c's control, under different
vocabulary; Simpson et al. 2018, Manea et al. 2024, Spina et al.
2025 and Koch-Hansen et al. 2026 supply the surrounding substrate.
Classification: mechanism ANTICIPATED; E1c's observed-control
design (spatially separated real field non-pairs matched on Lz, Jr,
Jz with the treatment pairs held fixed) AS-APPLICATION, exact
implementation unlocated. Externally defensible language, adopted:
"Building on established orbit–chemistry coupling, we use spatially
separated field non-pairs matched on Lz, Jr and Jz to estimate how
much comoving-pair iron-abundance similarity remains after
conditioning on present-day Galactic actions." Cite Coronado 2020 as
the mechanism precedent; no "first" or "nobody". The measured
numbers and the SHRINKS verdict are unaffected. Also noted: the
reviewer's own one-lane search (this document's author) missed
Coronado 2020 — a vocabulary-translation miss of exactly the kind
the N1 study measured, and the reason the two-lane Deep Check is
mandatory before any external sentence.
