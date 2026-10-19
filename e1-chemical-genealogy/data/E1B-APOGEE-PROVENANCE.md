# E1b APOGEE DR17 intake provenance

- Catalog retrieval started (UTC): 2026-08-30T08:50:33Z
- Catalog retrieval completed (UTC): 2026-08-30T08:50:44Z
- Catalog endpoint: `https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch`
- Catalog tables: `apogeeStar`, exact join to `aspcapStar` on `apstar_id`
- Gaia-coordinate retrieval started (UTC): 2026-08-30T08:50:45Z
- Gaia-coordinate retrieval completed (UTC): 2026-08-30T08:55:37Z
- Gaia EDR3 TAP endpoint: `https://gea.esac.esa.int/tap-server/tap/sync`
- Gaia coordinate table: `gaiaedr3.gaia_source`
- Result: `e1b_apogee.csv`
- Rows: 233,205
- Unique Gaia EDR3 source IDs: 201,602
- Exact Gaia coordinate matches: 201,602
- SHA-256: `806c97dd03f39d3ad0a77e6c8bc6b300dacfce76b4eddb9320dca22d108f0ce1`

SkyServer's DR17 `apogeeStar` table contains Gaia EDR3 source ID, parallax,
and proper motions but not Gaia EDR3 RA/Dec. The two requested coordinate
columns were therefore retrieved by an exact source-ID upload join to the
official Gaia EDR3 archive. No sky match or coordinate substitution was used.

Exact SkyServer SQL:

```sql
SELECT
  s.APOGEE_ID AS APOGEE_ID,
  s.GAIAEDR3_SOURCE_ID AS GAIAEDR3_SOURCE_ID,
  s.GAIAEDR3_PARALLAX AS GAIAEDR3_PARALLAX,
  s.GAIAEDR3_PARALLAX_ERROR AS GAIAEDR3_PARALLAX_ERROR,
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
  CASE WHEN (a.ASPCAPFLAG & dbo.fApogeeAspcapFlag('STAR_BAD')) = 0
       THEN 0 ELSE 1 END AS ASPCAP_STAR_BAD
FROM apogeeStar AS s
JOIN aspcapStar AS a ON a.apstar_id = s.apstar_id
WHERE s.GAIAEDR3_PARALLAX >= 1
  AND s.GAIAEDR3_PARALLAX_ERROR > 0
  AND s.GAIAEDR3_PARALLAX / s.GAIAEDR3_PARALLAX_ERROR >= 10
  AND s.SNR > 70
  AND s.GAIAEDR3_SOURCE_ID > 0
  AND s.VHELIO_AVG > -999
  AND a.FE_H > -999
  AND (a.ASPCAPFLAG & dbo.fApogeeAspcapFlag('STAR_BAD')) = 0
```

Exact Gaia EDR3 ADQL:

```sql
SELECT
  t.source_id AS source_id,
  g.ra AS ra,
  g.dec AS dec
FROM TAP_UPLOAD.targets AS t
JOIN gaiaedr3.gaia_source AS g ON t.source_id = g.source_id
```

Validation was limited to schema, decimal-ID, coordinate-join, and frozen-cut
integrity. No pairs or scientific statistics were computed.
