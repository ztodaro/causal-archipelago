# E1b Cantat-Gaudin 2020 member intake provenance

- Retrieval started (UTC): 2026-08-30T08:55:47Z
- Retrieval completed (UTC): 2026-08-30T08:55:51Z
- Endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync`
- VizieR catalog: `J/A+A/640/A1`, table `nodup`
- Result: `e1b_cg_members.csv`
- Rows: 55,466
- Unique Gaia DR2 source IDs: 55,169
- SHA-256: `1a50786209aa1bbe7400eab5d4ba8f8f287d3ef3302a44a0e46e623892d87708`

Exact ADQL:

```sql
SELECT
  "GaiaDR2",
  "Cluster",
  "RA_ICRS",
  "DE_ICRS",
  "Plx",
  "proba"
FROM "J/A+A/640/A1/nodup"
WHERE "Plx" >= 1
  AND "proba" >= 0.7
ORDER BY "GaiaDR2", "Cluster"
```

Validation was limited to schema, decimal-ID, and frozen-cut integrity. This
file is an intake-only masking list; no pairing or scientific statistic was
computed.
