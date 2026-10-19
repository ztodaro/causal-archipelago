# E8 APOGEE DR17 abundance intake provenance

- Catalog retrieval started (UTC): 2026-08-30T16:20:05Z
- Catalog retrieval completed (UTC): 2026-08-30T16:20:22Z
- Catalog endpoint: `https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch`
- Catalog tables: `apogeeStar`, left exact join to `aspcapStar` on `apstar_id`
- Explicit SQL `TOP`: 400,000
- Independent base and joined row counts: 331,088
- Gaia-coordinate retrieval started (UTC): 2026-08-30T16:20:24Z
- Gaia-coordinate retrieval completed (UTC): 2026-08-30T16:40:01Z
- Gaia DR3 mirror endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync`
- Gaia TAP mode: synchronous exact-ID upload chunks
- Gaia coordinate table: VizieR `I/355/gaiadr3`
- Gaia exact-ID upload chunks: 4
- Gaia chunk size: at most 75,000 IDs
- Gaia per-chunk `MAXREC`: uploaded row count + 10
- Returned catalog rows: 331,088
- Unique Gaia EDR3 source IDs: 283,616
- Exact Gaia coordinate matches: 283,616
- Output: `e8_apogee_abund.csv`
- SHA-256: `ced7250223381732c2642dd4c5723908f691ca2e9ac9e47f83a0e802a5f9c040`
- Row-cap check: returned count equals `COUNT(*)` and is below `TOP`

SkyServer's `apogeeStar` table does not publish Gaia EDR3 RA/Dec. Those two
requested fields were supplied by an exact source-ID upload join to the
VizieR mirror of the published Gaia DR3 catalog. No positional matching or
row filtering was used.
`ASPCAP_STAR_BAD` is the explicitly requested official SDSS bit test.

Exact SkyServer SQL:

```sql
SELECT TOP 400000
  s.APOGEE_ID AS APOGEE_ID,
  s.GAIAEDR3_SOURCE_ID AS GAIAEDR3_SOURCE_ID,
  s.GAIAEDR3_PARALLAX AS GAIAEDR3_PARALLAX,
  s.GAIAEDR3_PMRA AS GAIAEDR3_PMRA,
  s.GAIAEDR3_PMDEC AS GAIAEDR3_PMDEC,
  s.VHELIO_AVG AS VHELIO_AVG,
  s.VSCATTER AS VSCATTER,
  s.NVISITS AS NVISITS,
  s.SNR AS SNR,
  a.TEFF AS TEFF,
  a.LOGG AS LOGG,
  a.FE_H AS FE_H,
  a.FE_H_ERR AS FE_H_ERR,
  a.ALPHA_M AS ALPHA_M,
  CASE WHEN a.ASPCAPFLAG IS NULL THEN NULL
       WHEN (a.ASPCAPFLAG & dbo.fApogeeAspcapFlag('STAR_BAD')) = 0
       THEN 0 ELSE 1 END AS ASPCAP_STAR_BAD,
  a.C_FE AS C_FE,
  a.C_FE_ERR AS C_FE_ERR,
  a.C_FE_FLAG AS C_FE_FLAG,
  a.N_FE AS N_FE,
  a.N_FE_ERR AS N_FE_ERR,
  a.N_FE_FLAG AS N_FE_FLAG,
  a.MG_FE AS MG_FE,
  a.MG_FE_ERR AS MG_FE_ERR,
  a.MG_FE_FLAG AS MG_FE_FLAG
FROM apogeeStar AS s
LEFT OUTER JOIN aspcapStar AS a ON a.apstar_id = s.apstar_id
WHERE s.GAIAEDR3_PARALLAX >= 1
ORDER BY s.GAIAEDR3_SOURCE_ID, s.APOGEE_ID
```

Exact count query:

```sql
SELECT COUNT(*) AS n, COUNT(a.apstar_id) AS abundance_matches
FROM apogeeStar AS s
LEFT OUTER JOIN aspcapStar AS a ON a.apstar_id = s.apstar_id
WHERE s.GAIAEDR3_PARALLAX >= 1
```

Exact Gaia EDR3 ADQL:

```sql
SELECT
  t.source_id AS source_id,
  g."RA_ICRS" AS ra,
  g."DE_ICRS" AS dec
FROM TAP_UPLOAD.targets AS t
JOIN "I/355/gaiadr3" AS g ON t.source_id = g."Source"
```

The requested C, N, and Mg abundance values, errors, and flags were all
available. No filter beyond `GAIAEDR3_PARALLAX >= 1`, derived abundance,
sieve, or analysis was run.
