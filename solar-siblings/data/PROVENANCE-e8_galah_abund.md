# E8 GALAH DR3 abundance intake provenance

- Retrieval started (UTC): 2026-08-30T15:54:44Z
- Retrieval completed (UTC): 2026-08-30T15:55:00Z
- Endpoint: `https://datacentral.org.au/vo/tap/sync`
- Primary table: `galah_dr3.main_star` (DR3 Main Allstar Clean)
- Identifier join: left exact `sobject_id` join to `galah_dr4.vacxmatchtable`
- Explicit ADQL `TOP`: 400,000
- Explicit TAP `MAXREC`: 400,000
- Independent `COUNT(*)`: 349,899
- Returned rows: 349,899
- Native Gaia DR2 IDs present: 349,869
- Native Gaia DR2 ID blanks retained: 30
- Exact Gaia DR3 IDs supplied: 313,781
- Unmatched Gaia DR3 IDs retained blank: 36,118
- Output: `e8_galah_abund.csv`
- SHA-256: `5b50329e6e5dd3ff36d2f7535cea520000928caf67ee09d51deee16cbe135da4`
- Row-cap check: returned count equals `COUNT(*)` and is below both limits

GALAH DR3's native `source_id` is a Gaia DR2 identifier. It is retained as
`gaia_dr2_source_id`. The requested `gaiadr3_source_id` is supplied only where
the same exact GALAH `sobject_id` exists in the published DR4 crossmatch; no
positional match or source-ID relabeling was used, and no DR3 row was dropped.

Exact ADQL:

```sql
SELECT TOP 400000
  d.sobject_id AS sobject_id,
  x.source_id AS gaiadr3_source_id,
  d.source_id AS gaia_dr2_source_id,
  d.ra AS ra,
  d.dec AS dec,
  d.parallax AS parallax,
  d.parallax_error AS parallax_error,
  d.pmra AS pmra,
  d.pmdec AS pmdec,
  d.rv_galah AS rv_galah,
  d.e_rv_galah AS e_rv_galah,
  d.snr_c3_iraf AS snr_c3_iraf,
  d.flag_sp AS flag_sp,
  d.teff AS teff,
  d.logg AS logg,
  d.fe_h AS fe_h,
  d.e_fe_h AS e_fe_h,
  d.flag_fe_h AS flag_fe_h,
  d.Na_fe AS na_fe,
  d.e_Na_fe AS e_na_fe,
  d.flag_Na_fe AS flag_na_fe,
  d.Mg_fe AS mg_fe,
  d.e_Mg_fe AS e_mg_fe,
  d.flag_Mg_fe AS flag_mg_fe,
  d.Al_fe AS al_fe,
  d.e_Al_fe AS e_al_fe,
  d.flag_Al_fe AS flag_al_fe,
  d.Si_fe AS si_fe,
  d.e_Si_fe AS e_si_fe,
  d.flag_Si_fe AS flag_si_fe,
  d.Ca_fe AS ca_fe,
  d.e_Ca_fe AS e_ca_fe,
  d.flag_Ca_fe AS flag_ca_fe,
  d.Ti_fe AS ti_fe,
  d.e_Ti_fe AS e_ti_fe,
  d.flag_Ti_fe AS flag_ti_fe,
  d.Cr_fe AS cr_fe,
  d.e_Cr_fe AS e_cr_fe,
  d.flag_Cr_fe AS flag_cr_fe,
  d.Mn_fe AS mn_fe,
  d.e_Mn_fe AS e_mn_fe,
  d.flag_Mn_fe AS flag_mn_fe,
  d.Ni_fe AS ni_fe,
  d.e_Ni_fe AS e_ni_fe,
  d.flag_Ni_fe AS flag_ni_fe,
  d.Cu_fe AS cu_fe,
  d.e_Cu_fe AS e_cu_fe,
  d.flag_Cu_fe AS flag_cu_fe,
  d.Zn_fe AS zn_fe,
  d.e_Zn_fe AS e_zn_fe,
  d.flag_Zn_fe AS flag_zn_fe,
  d.Y_fe AS y_fe,
  d.e_Y_fe AS e_y_fe,
  d.flag_Y_fe AS flag_y_fe,
  d.Ba_fe AS ba_fe,
  d.e_Ba_fe AS e_ba_fe,
  d.flag_Ba_fe AS flag_ba_fe
FROM galah_dr3.main_star AS d
LEFT OUTER JOIN galah_dr4.vacxmatchtable AS x ON d.sobject_id = x.sobject_id AND x.source_id > 0
WHERE d.parallax >= 1
ORDER BY sobject_id
```

Exact count query:

```sql
SELECT COUNT(*) AS n, COUNT(x.source_id) AS matched_dr3_ids
FROM galah_dr3.main_star AS d
LEFT OUTER JOIN galah_dr4.vacxmatchtable AS x
  ON d.sobject_id = x.sobject_id AND x.source_id > 0
WHERE d.parallax >= 1
```

All 13 requested abundance value/error/flag triplets were available. No
filter beyond `parallax >= 1`, derived abundance, sieve, or analysis was run.
