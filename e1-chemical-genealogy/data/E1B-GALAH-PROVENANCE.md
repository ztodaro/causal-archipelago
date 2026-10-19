# E1b GALAH DR4 intake provenance

- Retrieval started (UTC): 2026-08-30T08:50:17Z
- Retrieval completed (UTC): 2026-08-30T08:50:23Z
- Endpoint: `https://datacentral.org.au/vo/tap/sync`
- Tables: `galah_dr4.mainstartable`, exact join to `galah_dr4.vacxmatchtable`
- Result: `e1b_galah.csv`
- Rows: 318,005
- Unique Gaia DR3 source IDs: 318,005
- SHA-256: `317d9738ad21db97d89441be2390d6c0667f00cf9d6d350587a993727438d029`

`rv` and `e_rv` are the DR4 primary-component fields `rv_comp_1` and
`e_rv_comp_1`. `snr` is the survey's `snr_px_ccd3`. Gaia position,
parallax, and proper motion are native fields from the DR4 Gaia crossmatch VAC.

Exact ADQL:

```sql
SELECT
  g.sobject_id AS sobject_id,
  g.gaiadr3_source_id AS gaiadr3_source_id,
  x.ra AS ra,
  x.dec AS dec,
  x.parallax AS parallax,
  x.parallax_error AS parallax_error,
  x.pmra AS pmra,
  x.pmdec AS pmdec,
  g.rv_comp_1 AS rv,
  g.e_rv_comp_1 AS e_rv,
  g.snr_px_ccd3 AS snr,
  g.teff AS teff,
  g.logg AS logg,
  g.fe_h AS fe_h,
  g.e_fe_h AS e_fe_h,
  g.flag_sp AS flag_sp,
  g.flag_fe_h AS flag_fe_h
FROM galah_dr4.mainstartable AS g
JOIN galah_dr4.vacxmatchtable AS x
  ON g.gaiadr3_source_id = x.source_id
WHERE g.flag_sp = 0
  AND g.flag_fe_h = 0
  AND g.snr_px_ccd3 > 30
  AND x.parallax >= 1
  AND x.parallax_over_error >= 10
  AND g.rv_comp_1 IS NOT NULL
  AND g.fe_h IS NOT NULL
ORDER BY gaiadr3_source_id, sobject_id
```

Validation was limited to schema, decimal-ID, uniqueness, and frozen-cut
integrity. No pairs or scientific statistics were computed.
