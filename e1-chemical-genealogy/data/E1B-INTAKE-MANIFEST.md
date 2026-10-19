# E1b intake manifest

- Frozen specification: `e1-chemical-genealogy/E1B-SPEC.md` at `ec12d01`
- Frozen-spec verification: byte-unmodified before and after retrieval
- Retrieval script: `../retrieve_e1b.py`
- Retrieval-script SHA-256: `e20af5851ec9d99cdccef95ebe771fefc0b523fedd0276ecaac9b3243552d905`

## Artifacts

| Pull | File | Rows | Unique source IDs | SHA-256 |
|---|---|---:|---:|---|
| GALAH DR4 | `e1b_galah.csv` | 318,005 | 318,005 | `317d9738ad21db97d89441be2390d6c0667f00cf9d6d350587a993727438d029` |
| APOGEE DR17 | `e1b_apogee.csv` | 233,205 | 201,602 | `806c97dd03f39d3ad0a77e6c8bc6b300dacfce76b4eddb9320dca22d108f0ce1` |
| Cantat-Gaudin 2020 | `e1b_cg_members.csv` | 55,466 | 55,169 | `1a50786209aa1bbe7400eab5d4ba8f8f287d3ef3302a44a0e46e623892d87708` |

Each file has a survey-specific provenance record containing its endpoint,
exact query, retrieval timestamps, row count, and SHA-256.

## Intake-integrity audit

- All three CSV schemas match the frozen request.
- All Gaia source identifiers are decimal integer strings.
- Recomputed frozen-cut violations: zero in all three files.
- GALAH Gaia source IDs are unique.
- APOGEE's 201,602 unique Gaia EDR3 IDs all received exact Gaia EDR3
  coordinate matches; repeated allStar rows have zero coordinate conflicts.
- Temporary raw-download, coordinate-join, and bytecode files are excluded
  from the final tree.

No pair construction, masking application, abundance comparison, or other
scientific analysis was performed.
