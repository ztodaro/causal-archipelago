# Causal Archipelago

This repository holds the locked studies discussed in the editorial "Felt novelty" on Compilation Press. Each study has its plan, the code that ran, the sources of its data, its results and the timestamp proofs that fix when the plan was written.

## The studies

| Folder | Study | Plan | Results |
| --- | --- | --- | --- |
| `e1-chemical-genealogy/` | E1: do comoving stars share their chemistry? | `E1-SPEC.md` | `E1-RESULTS.md` |
| `e1-chemical-genealogy/` | E1b: the same test on kiloparsec-scale pairs in GALAH and APOGEE | `E1B-SPEC.md` | `E1B-RESULTS.md` |
| `e1-chemical-genealogy/` | E1c: E1b repeated against stars on the same orbit | `E1C-SPEC.md` | `E1C-RESULTS.md` |
| `e2-wide-binaries/` | E2: a sealed test of gravity at low acceleration in wide binary stars | `E2-SPEC.md` | `E2-UNSEALED-RESULTS.md` |
| `e2-wide-binaries/` | E2b: the powered rerun of E2 | `E2B-SPEC.md` | `E2B-UNSEALED-RESULTS.md`, `E2B-STRESS-MEMO.md` |
| `solar-siblings/` | E8: candidate siblings of the Sun | `E8-SPEC.md` | `E8-RESULTS.md` |
| `notes/` | E10 and E10b: does shared chemistry fade with age? | `E10-SPEC.md`, `E10B-SPEC.md` | `E10-RESULTS.md`, `E10B-RESULTS.md` |
| `notes/e10c/` | E10c: an APOGEE replication of E10b, found infeasible | `E10C-SPEC.md` | `E10C-FEASIBILITY.md` |
| `notes/novelty-search/n1-retrospective/` | N1: can AI models tell whether an idea is new? | `../N1-SELF-AUDIT-CALIBRATION-SPEC.md`, `MANIFEST.md` | `RESULTS.md`, `I3-OPENAI-RESULTS.md`, `CROSS-LAB-SYNTHESIS.md` |
| `notes/dr4-freeze/` | Predictions frozen before Gaia DR4 (2 December 2026) | `DR4-FREEZE-SPEC.md`, `B2-B4-SPEC.md` | to be run on DR4 |

Each plan was committed before the analysis it describes was run. Results files record every outcome, including nulls and corrections.

## The timestamps

Three files were stamped with OpenTimestamps, a free public service that proves a file existed at a given moment.

| Stamped file | What it fixes |
| --- | --- |
| `precommit.txt` | Commit `7e75a61`, the state of the project before the first gravity test (E2) was opened on 30 August 2026. `PRECOMMITMENT.md` describes it. |
| `precommit-e2b.txt` | Commit `953e527`, the state before the second gravity test (E2b) was opened on 30 August 2026. |
| `notes/dr4-freeze/MANIFEST.sha256` | The SHA-256 of the 28 files frozen before Gaia DR4, on 1 September 2026. |

To check a stamp, run the OpenTimestamps client on its proof, for example `ots verify precommit-e2b.txt.ots`.

To check that the files here are the files that were stamped, run:

    python verify/check.py

The script uses the Python standard library only. It checks every file in the DR4 manifest against its SHA-256 and names the three method write-ups that were edited for publication (see below). It also rebuilds commits `7e75a61` and `953e527` from the git objects in `verify/snapshots/` and confirms that each published file has the same git blob id inside the stamped commit.

## What this record leaves out

The two stamped commits also held the project's working notes. Those notes are not published. The snapshot check uses their names and hashes, and their contents stay private.

Two data files are larger than GitHub allows: `e2-wide-binaries/data/e2b_elbadry_200pc.csv` and `solar-siblings/data/e8_galah_abund.csv`. Each has a provenance file with its source and SHA-256, and a retrieval script rebuilds it.

## Edits for publication

Files covered by a stamp are published exactly as stamped, with three exceptions. Three method write-ups in the DR4 manifest had process notes and links to unpublished working files removed:

- `e1-chemical-genealogy/E1C-SPEC.md`
- `notes/E10B-SPEC.md`
- `notes/dr4-freeze/B2-B4-SPEC.md`

These three no longer match their stamped hashes, and `verify/check.py` lists them. The scripts that carry out those methods and the results they produced are published as stamped, and they still match. One removed link pointed to the only note crediting the source of E10b's method, so `notes/E10B-SPEC.md` now credits Boufourou (arXiv:2608.24556) directly.

Fourteen unstamped documents were edited the same way. No number, method or finding changed. The edited files are:

- `e2-wide-binaries/E2B-STRESS-MEMO.md`
- `notes/dr4-freeze/DR4-FREEZE-SPEC.md`
- `notes/e10c/E10C-SPEC.md` and `notes/e10c/E10C-FEASIBILITY.md`
- `notes/novelty-search/N1-SELF-AUDIT-CALIBRATION-SPEC.md`
- in `notes/novelty-search/n1-retrospective/`: `MANIFEST.md`, `RAW-JUDGMENTS.md`, `N1-AMENDMENT-1.md`, `VERIFICATIONS-AND-R-2026-08-31.md`, `CROSS-LAB-SYNTHESIS.md`, `I3-PACKETS.md`, `I3-JUDGMENTS.md`, `I3-OPENAI-MANIFEST.md` and `I3-OPENAI-RESULTS.md`

## Corrections

The record only grows. A correction is a new dated entry beside the original, and the original stays as it was.
