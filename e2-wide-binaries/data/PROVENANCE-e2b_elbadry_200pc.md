# E2b El-Badry powered-sample intake provenance

- Retrieval started (UTC): 2026-08-30T09:35:33Z
- Retrieval completed (UTC): 2026-08-30T09:36:53Z
- Published catalog: El-Badry, Rix & Heintz (2021), `gaia_edr3_binaries`
- Canonical release URL: `https://zenodo.org/records/4435257`
- Query service: VizieR TAP
- Endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync`
- Table: `J/MNRAS/506/2269/catalog`
- Explicit `MAXREC`: 200,000
- Independent pre-download `COUNT(*)`: 125,713
- Returned rows: 125,713
- Returned published columns: 220
- Unique EDR3/DR3 source IDs across both components: 251,426
- Output: `e2b_elbadry_200pc.csv`
- SHA-256: `4a8d9cd8017aa7178c9b5acaf8e9f34dce450d3cd96ee40ba0c430134c4dd9a0`
- Row-cap check: returned count equals `COUNT(*)` and is below `MAXREC`

Exact ADQL:

```sql
SELECT *
FROM "J/MNRAS/506/2269/catalog"
WHERE (Plx1 >= 5 OR Plx2 >= 5)
  AND R < 0.1
ORDER BY "Source1", "Source2"
```

Exact count query:

```sql
SELECT COUNT(*) AS n
FROM "J/MNRAS/506/2269/catalog"
WHERE (Plx1 >= 5 OR Plx2 >= 5)
  AND R < 0.1
```

## Step 2 decision

No Gaia DR3 quality join was needed. The published table contains, for both
components, `RUWE1/2`, `IPDfmp1/2` (ipd_frac_multi_peak), `epsi1/2`
(astrometric_excess_noise), `sepsi1/2` (astrometric_excess_noise_sig),
`RPlx1/2` (parallax_over_error), `e_pmRA1/2`, and `e_pmDE1/2`.

Validation was limited to schema completeness, exact decimal identifiers,
the two frozen intake predicates, and the explicit row-cap check. No other
filter, derived column, pair analysis, or sealed statistic was applied.
