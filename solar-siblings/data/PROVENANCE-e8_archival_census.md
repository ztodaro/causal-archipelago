# E8 archival census — ESO spectra availability

Intake only. No science spectrum, FITS file, preview, spectral array, or line
measurement was downloaded or examined. The E8-CONFIRM gate remains closed.

## Frozen-input verification

- Latest protocol commit: `96d4fa36d4aa7ca1f67fc1eb37ac8f4eb4b0ecd6` (required prefix `96d4fa3`).
- Protocol SHA-256: `98582f94e626281bd27cee237d4a8163ea1ec07b4f4f185ba384e161fea39841`.
- Target-list SHA-256: `46a04ded16b4ab98999a30d8976a3a8358fa2f04bfe470e3766a7e95cf2fe827`.
- All three mandatory checks passed before retrieval, after retrieval, and before
  finalization. Neither frozen file was modified.
- 20 targets. Target `survey_id` maps to `sobject_id` in the census schema.
  All identifiers remain decimal strings; rank 19's Gaia ID remains blank.

## Acquisition and scope

- Endpoint: `https://archive.eso.org/tap_obs/sync` (HTTPS version of the requested ESO endpoint).
- Retrieval started UTC: `2026-08-30T21:11:25Z`.
- Retrieval completed UTC: `2026-08-30T21:11:47Z`.
- Every query uses HTTP POST: `REQUEST=doQuery`, `LANG=ADQL`, `FORMAT=votable`,
  `MAXREC=1000000`. VOTable TABLEDATA cells were parsed as strings.
- All 42 responses returned HTTP 200 and QUERY_STATUS=OK, with no OVERFLOW.
  Candidate queries have no TOP clause; all returned zero rows, below the limit.
  Solar TOP 5 clauses deliberately sample examples and are not total counts.
- Separate searches cover processed spectra (`ivoa.ObsCore`) and raw observations
  (`dbo.raw`). Both use the archive `s_region` point and frozen input coordinates
  verbatim with radius `2.0/3600.0` degrees. No epoch propagation, expanded cone,
  alternate coordinates, candidate-name search, or Gaia-ID substitution was used.
- ObsCore cuts: the four requested instruments, dataproduct_type='spectrum', and
  UVES em_res_power>=40000. No SNR or release-date cut was applied to candidates.
  No later R/coverage filtering is needed because all candidate searches are empty.
- Raw metadata has no dataproduct_type, em_res_power, or SNR; lambda_min/max are
  documented as image-only. Raw queries retrieve all observation types in the
  specified cones for the four instruments, for metadata-only eligibility review.
  They returned zero rows too. No raw classification or UVES R was inferred;
  no FITS-header retrieval was needed.
- Wavelength bounds are metres; exposure is seconds; t_min is MJD days; R is
  dimensionless. Published SNR is ESO's average spectrum SNR, not a separately
  established per-pixel SNR. UTC solar dates below only reformat the retained MJD.
- Solar examples have calib_level=2 and p3orig=IDP: ESO-generated Phase-3 products.
  Public status uses the published release date compared with retrieval UTC.
  All ten solar examples are public. No proprietary exclusion applied to candidates.
- Scope is anonymous archive-visible metadata at the specified positions and
  radius. Restricted metadata and observations outside these cones are outside
  this census; the zero result is not a claim about such unqueried records.

Official archive documentation:

- [ESO raw and processed tables](https://www.eso.org/cms/eso-data/eso-data-products.html)
- [ESO query examples and spatial conventions](https://archive.eso.org/programmatic/)
- [Programmatic access and authentication](https://archive.eso.org/cms/eso-data/programmatic-access.html)
- Live schema inspected with `SELECT table_name,column_name,datatype,unit,description
  FROM TAP_SCHEMA.columns WHERE table_name IN ('ivoa.ObsCore','dbo.raw')`.

## Candidate counts, including zeros

| Rank | Gaia source_id | GALAH sobject_id | ObsCore spectra | Raw records | Usable datasets |
|---|---|---|---:|---:|---:|
| 1 | 6379813798086252160 | 150830005101255 | 0 | 0 | 0 |
| 2 | 5377439590220801920 | 170507007201316 | 0 | 0 | 0 |
| 3 | 4704616882942264320 | 161119003101102 | 0 | 0 | 0 |
| 4 | 6716036271949014400 | 140607000701099 | 0 | 0 | 0 |
| 5 | 6086357992929479296 | 170413003601143 | 0 | 0 | 0 |
| 6 | 4674777576177682304 | 161011003401074 | 0 | 0 | 0 |
| 7 | 6136285231098954112 | 150606002901099 | 0 | 0 | 0 |
| 8 | 5386338556301313536 | 160525002201184 | 0 | 0 | 0 |
| 9 | 5777013798065575040 | 160326002101102 | 0 | 0 | 0 |
| 10 | 6562738963484316800 | 140811004501075 | 0 | 0 | 0 |
| 11 | 5401532260806155648 | 160422003001063 | 0 | 0 | 0 |
| 12 | 6124054985305292928 | 170418003701322 | 0 | 0 | 0 |
| 13 | 6728919696365591040 | 170710002201158 | 0 | 0 | 0 |
| 14 | 3909125855243117568 | 150409006101289 | 0 | 0 | 0 |
| 15 | 4813718329390688768 | 161104004301097 | 0 | 0 | 0 |
| 16 | 3205136631885550336 | 171102003901103 | 0 | 0 | 0 |
| 17 | 4058723586386753152 | 170509006201383 | 0 | 0 | 0 |
| 18 | 652737211113728256 | 161228002501099 | 0 | 0 | 0 |
| 19 |  | 150606003402394 | 0 | 0 | 0 |
| 20 | 5282999444146406400 | 171205004101352 | 0 | 0 | 0 |

Total candidate x dataset rows: **0**. Total usable candidate datasets: **0**.
The CSV is intentionally header-only. Zero is a successful data result, not a query failure.

## Solar-reference availability

Five public reflected-sunlight products per instrument were found. These are
availability examples, selected by target name, R>=40000, public release, and
descending observation time. They are not adopted differential standards.
The sampled HARPS Moon products publish SNR 7.6–7.7; no SNR cut was applied.
The ESPRESSO examples publish SNR 203.7–345.4. These are transcribed metadata,
not a validation of suitability for a later differential analysis.

| Instrument | Target | Dataset/product ID | Observation UTC | MJD | R | SNR | Exposure (s) | Program | Release UTC |
|---|---|---|---|---|---:|---:|---:|---|---|
| HARPS | Moon | ADP.2016-04-20T08:25:53.493 | 2016-04-01T09:47:13.942Z | 57479.40780026 | 115000.0 | 7.7 | 119.998 | 096.C-0210(A) | 2017-04-01T10:01:03.900Z |
| HARPS | Moon | ADP.2016-04-20T08:25:53.485 | 2016-04-01T09:44:43.033Z | 57479.40605363 | 115000.0 | 7.7 | 119.998 | 096.C-0210(A) | 2017-04-01T09:55:55.317Z |
| HARPS | Moon | ADP.2016-04-20T08:25:53.755 | 2016-04-01T09:42:12.085Z | 57479.40430654 | 115000.0 | 7.7 | 119.998 | 096.C-0210(A) | 2017-04-01T09:55:55.317Z |
| HARPS | Moon | ADP.2016-04-20T08:25:53.747 | 2016-04-01T09:39:40.947Z | 57479.40255726 | 115000.0 | 7.6 | 119.998 | 096.C-0210(A) | 2017-04-01T09:55:55.317Z |
| HARPS | Moon | ADP.2016-04-20T08:25:53.741 | 2016-04-01T09:37:09.548Z | 57479.40080496 | 115000.0 | 7.6 | 119.998 | 096.C-0210(A) | 2017-04-01T09:50:46.563Z |
| ESPRESSO | Ganymede | ADP.2021-11-04T16:29:28.661 | 2021-10-06T00:50:14.907Z | 59493.03489476 | 140000.0 | 345.4 | 90.0 | 108.22GM.001 | 2022-10-06T01:00:24Z |
| ESPRESSO | Vesta | ADP.2021-09-03T15:16:51.419 | 2021-03-10T04:42:53.938Z | 59283.19645762 | 140000.0 | 233.6 | 60.0 | 106.218R.002 | 2022-03-10T04:51:14Z |
| ESPRESSO | Vesta | ADP.2021-09-03T15:07:46.192 | 2021-03-08T04:51:21.821Z | 59281.2023359 | 140000.0 | 235.3 | 45.0 | 106.218R.002 | 2022-03-08T05:00:41Z |
| ESPRESSO | ceres | ADP.2021-04-19T12:50:48.797 | 2019-04-26T10:03:23.826Z | 58599.41902577 | 140000.0 | 203.7 | 600.0 | 1102.A-0852(C) | 2020-04-26T10:30:32Z |
| ESPRESSO | Vesta | ADP.2021-04-14T14:24:19.871 | 2018-11-19T00:58:24.532Z | 58441.04056172 | 190000.0 | 205.7 | 1500.0 | 0102.D-0185(A) | 2019-05-18T01:30:53Z |

Published wavelength bounds (metres):

| Dataset/product ID | em_min | em_max |
|---|---|---|
| ADP.2016-04-20T08:25:53.493 | 3.7822300000000004E-7 | 6.91349E-7 |
| ADP.2016-04-20T08:25:53.485 | 3.7822300000000004E-7 | 6.91349E-7 |
| ADP.2016-04-20T08:25:53.755 | 3.7822300000000004E-7 | 6.91349E-7 |
| ADP.2016-04-20T08:25:53.747 | 3.7822300000000004E-7 | 6.91349E-7 |
| ADP.2016-04-20T08:25:53.741 | 3.7822300000000004E-7 | 6.91349E-7 |
| ADP.2021-11-04T16:29:28.661 | 3.7719999999999996E-7 | 7.89997E-7 |
| ADP.2021-09-03T15:16:51.419 | 3.7719999999999996E-7 | 7.89997E-7 |
| ADP.2021-09-03T15:07:46.192 | 3.7719999999999996E-7 | 7.89997E-7 |
| ADP.2021-04-19T12:50:48.797 | 3.7719999999999996E-7 | 7.89997E-7 |
| ADP.2021-04-14T14:24:19.871 | 3.7719999999999996E-7 | 7.89997E-7 |

## Files and reproducibility

- `e8_archival_census.csv`: **0 data rows**, 18 columns, 193 bytes.
- CSV SHA-256: `531598f6e8c5b4c658a93489fb3222ec8a58e440c88ecf39716eb47408da3a14`.
- Script: `solar-siblings/retrieve_e8_census.py`, SHA-256 `619b93773d380a59ed37bf4322a51204ac7249ef394d47d049631a2775896570`.
- Collection: `python -u solar-siblings/retrieve_e8_census.py collect`.
- Finalization: `python -u solar-siblings/retrieve_e8_census.py finalize <metadata_snapshot.json>`.
  Collection prints the temporary metadata snapshot path. Finalization makes no
  network requests and refuses to overwrite existing deliverables. Future nonzero
  candidate results fail closed pending raw-setting/coverage metadata review.
- Preliminary schema, technique-label, and first-target syntax checks were
  metadata-only. The authoritative acquisition is the complete 42-query run below.

## Exact acquisition queries and response audit

### candidate-01-obscore

- Start UTC: `2026-08-30T21:11:25Z`; end UTC: `2026-08-30T21:11:27Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `b6552905d5076a99f4884a3f720f5f63e38937b2c91dcf1837af3cb3f1435000`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',355.36124,-73.202774,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-01-raw

- Start UTC: `2026-08-30T21:11:25Z`; end UTC: `2026-08-30T21:11:27Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `7d09e008e4e3625cfb3ce807e2746085ad4caafd4f3aba0921401061cdffb07c`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',355.36124,-73.202774,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-02-obscore

- Start UTC: `2026-08-30T21:11:25Z`; end UTC: `2026-08-30T21:11:27Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `5205966c8bb5b3129935fbf2f700264c5b853bc06899e80750fe87bf507e1925`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',179.9236,-47.269196,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-02-raw

- Start UTC: `2026-08-30T21:11:27Z`; end UTC: `2026-08-30T21:11:28Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `78770897c73a2cbb062c0c8fa81728644f5789efb97fee65c8ca8783005032d6`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',179.9236,-47.269196,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-03-obscore

- Start UTC: `2026-08-30T21:11:27Z`; end UTC: `2026-08-30T21:11:28Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `afbda6a6233dcf7e345f0dfd3e03cfb0c4218c3fbd429dab7038de258e5fa579`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',19.846664,-67.33961,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-03-raw

- Start UTC: `2026-08-30T21:11:27Z`; end UTC: `2026-08-30T21:11:28Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `89b8334cee7698ab86658bccb26d3b81e64e6fb707a2546bf3b8e9fc79c45131`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',19.846664,-67.33961,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-04-obscore

- Start UTC: `2026-08-30T21:11:28Z`; end UTC: `2026-08-30T21:11:30Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `c941b5c861259ce9a23d0ba419e8765827a17833fbce5695b842282ec6e8b982`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',282.42023,-42.688404,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-04-raw

- Start UTC: `2026-08-30T21:11:28Z`; end UTC: `2026-08-30T21:11:30Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `ca931e4685c9d6cecdc38e2a84befbe411b55a3d173c0d772ac06d09010a3b15`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',282.42023,-42.688404,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-05-obscore

- Start UTC: `2026-08-30T21:11:28Z`; end UTC: `2026-08-30T21:11:30Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `5f3e786ca8b0e965c35a0f18a2ce95230495575328583ce78d55c723cd436440`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',195.8565,-46.901955,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-05-raw

- Start UTC: `2026-08-30T21:11:30Z`; end UTC: `2026-08-30T21:11:31Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `d085d65e20f2e1f44eb271dcc2485074dec4c4ed32d1e3269448745db0652769`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',195.8565,-46.901955,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-06-obscore

- Start UTC: `2026-08-30T21:11:30Z`; end UTC: `2026-08-30T21:11:31Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `834606dffe2be4753c9574553b72dc1ea8bac74cbec688a537fa15992094083f`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',67.370476,-65.861115,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-06-raw

- Start UTC: `2026-08-30T21:11:30Z`; end UTC: `2026-08-30T21:11:31Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `d3a29428408eae9916f68e90f98fc1d86427bf011a91c1bcc55c80fe1a5df720`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',67.370476,-65.861115,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-07-obscore

- Start UTC: `2026-08-30T21:11:31Z`; end UTC: `2026-08-30T21:11:33Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `0bdb58c00ba4e30e19722bfec447c9bdd904a19bc7acdfefe8e136c55b600a7d`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',198.59834,-43.688652,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-07-raw

- Start UTC: `2026-08-30T21:11:31Z`; end UTC: `2026-08-30T21:11:33Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `e64249c1694305ac1422cc7d5a77cf284c6ce87841c0b8831464b3e7c9a5965e`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',198.59834,-43.688652,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-08-obscore

- Start UTC: `2026-08-30T21:11:31Z`; end UTC: `2026-08-30T21:11:32Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `8548645e407c3b0b581f7557e09614a607f4577d6682bdfba61622f26177491e`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',166.67232,-47.4955,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-08-raw

- Start UTC: `2026-08-30T21:11:32Z`; end UTC: `2026-08-30T21:11:34Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `554f65242c47508b23d811431c5752077e735e6150edebe85b71952ce5d91ac7`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',166.67232,-47.4955,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-09-obscore

- Start UTC: `2026-08-30T21:11:33Z`; end UTC: `2026-08-30T21:11:34Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `dd9bef13ecd4379dee4561be0926d847ed86d3a9698a63b3875428c31f907c94`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',255.38428,-79.36358,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-09-raw

- Start UTC: `2026-08-30T21:11:33Z`; end UTC: `2026-08-30T21:11:34Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `0107287290c39c40a85818823d0f208ce7efbd6e16c381984ae37f6f14e7f170`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',255.38428,-79.36358,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-10-obscore

- Start UTC: `2026-08-30T21:11:34Z`; end UTC: `2026-08-30T21:11:35Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `40eedb5da9c20d0f4ef6b2c5b096d2e5052e94c6542cd2ca7cb17e1d295d4f08`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',326.34222,-47.891125,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-10-raw

- Start UTC: `2026-08-30T21:11:34Z`; end UTC: `2026-08-30T21:11:36Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `e8f28a092ea623617c89e5a70009b576a667b4b08654c087c8b8d53d61ff1bde`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',326.34222,-47.891125,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-11-obscore

- Start UTC: `2026-08-30T21:11:34Z`; end UTC: `2026-08-30T21:11:36Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `85ad33f8a23b523ffd61cfbc430b14e7a49f798ee26fca81da3d85db06f0ce91`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',165.97632,-35.187733,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-11-raw

- Start UTC: `2026-08-30T21:11:35Z`; end UTC: `2026-08-30T21:11:37Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `e46c9db4af099ec981d0133ca096f1e240a9f56e62dac690d7b6242a4fbf5999`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',165.97632,-35.187733,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-12-obscore

- Start UTC: `2026-08-30T21:11:36Z`; end UTC: `2026-08-30T21:11:37Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `8ce4a71f12c6cb87e273e0ba0a2c0aa526ec1ca1701ec5da606ab4cb6ecae028`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',211.72575,-33.3097,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-12-raw

- Start UTC: `2026-08-30T21:11:36Z`; end UTC: `2026-08-30T21:11:37Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `be2fc6c43b433a9880ec2ac170973ad58bd0027096a5f1b8643d5ef79ff15419`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',211.72575,-33.3097,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-13-obscore

- Start UTC: `2026-08-30T21:11:37Z`; end UTC: `2026-08-30T21:11:38Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `8db656473ff2c103454f3772297808f5ca0014ecf3d4d60dfcb6232245bd8305`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',281.34625,-39.06656,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-13-raw

- Start UTC: `2026-08-30T21:11:37Z`; end UTC: `2026-08-30T21:11:39Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `744826dc4783a3bedb7ca0c072c119a95c3df9385446c455787ab9d81f9da682`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',281.34625,-39.06656,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-14-obscore

- Start UTC: `2026-08-30T21:11:37Z`; end UTC: `2026-08-30T21:11:39Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `fd8fa338c8390ead31aaa34df71e6e5d8c2227c8bd6190839f1e7508feb7aa04`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',174.30875,4.83916,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-14-raw

- Start UTC: `2026-08-30T21:11:38Z`; end UTC: `2026-08-30T21:11:39Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `a2a28acff1b98df207fe879dfbe25cf4724dfa2e3a2eeabb1f3519bdc59e4195`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',174.30875,4.83916,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-15-obscore

- Start UTC: `2026-08-30T21:11:39Z`; end UTC: `2026-08-30T21:11:40Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `079b7f0a0cce9354808504f659c6bc83bd670a111af3098a4386a82eaa863be2`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',74.19841,-41.214207,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-15-raw

- Start UTC: `2026-08-30T21:11:39Z`; end UTC: `2026-08-30T21:11:40Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `24179e0bcef9d05f19044f1037b8e28d70c03326d6603ef4e5002c68e18b8704`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',74.19841,-41.214207,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-16-obscore

- Start UTC: `2026-08-30T21:11:39Z`; end UTC: `2026-08-30T21:11:41Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `eb0fe2aae00799685f21e7bdc63070cede5cc6263854b067a61b2fd933ab733c`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',69.81029,-2.015513,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-16-raw

- Start UTC: `2026-08-30T21:11:40Z`; end UTC: `2026-08-30T21:11:42Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `f01a1c4e983af75026d6da20e864e5ecd5314ac1b8e0c968dd3e3af63d699941`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',69.81029,-2.015513,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-17-obscore

- Start UTC: `2026-08-30T21:11:40Z`; end UTC: `2026-08-30T21:11:42Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `9c578c7894d88e2873fece144850c4fa6bcfa439c0cd2e11c42dd3210a22b893`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',262.34827,-29.45382,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-17-raw

- Start UTC: `2026-08-30T21:11:41Z`; end UTC: `2026-08-30T21:11:42Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `b9b746d3addb74610da7e87a97134f0c7c95c91530e43d2c24802b16543193af`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',262.34827,-29.45382,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-18-obscore

- Start UTC: `2026-08-30T21:11:42Z`; end UTC: `2026-08-30T21:11:43Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `2d756171d73df4ced47b7808b69c3862b4a47380402e2f5345eca4006de1a52a`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',127.13989,16.159811,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-18-raw

- Start UTC: `2026-08-30T21:11:42Z`; end UTC: `2026-08-30T21:11:44Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `93f1e21b8e018a7f981bb5d1a59323ad37ee9f7f61883e57ea12df4032a80980`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',127.13989,16.159811,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-19-obscore

- Start UTC: `2026-08-30T21:11:42Z`; end UTC: `2026-08-30T21:11:44Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `a2d17565728669768a06130e5fa08cc506c923b32fb5c41b19ea6a321daa754a`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',243.59245,-25.462933,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-19-raw

- Start UTC: `2026-08-30T21:11:43Z`; end UTC: `2026-08-30T21:11:45Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `e0260e89b6752aed205b3b96ba258c26567c294318e7679e7ba766066fa2bb04`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',243.59245,-25.462933,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### candidate-20-obscore

- Start UTC: `2026-08-30T21:11:44Z`; end UTC: `2026-08-30T21:11:45Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `79e5b6f1c5dcf7e6207e4ef483a89ecd8c5363e42077c3703125753095f11e73`.

```sql
SELECT dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')
AND dataproduct_type='spectrum'
AND (instrument_name<>'UVES' OR em_res_power>=40000)
AND CONTAINS(s_region,CIRCLE('ICRS',95.167145,-67.451324,2.0/3600.0))=1
ORDER BY t_min,dp_id
```

### candidate-20-raw

- Start UTC: `2026-08-30T21:11:44Z`; end UTC: `2026-08-30T21:11:45Z`.
- Rows: `0`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `d07c4c35cdfb0796bef185f1e9cdcbb4f70804583f03f1ec7ce68f26ef7993f0`.

```sql
SELECT dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,exposure,release_date,prog_id,object,target,ins_mode,slit_path,grat_path,lambda_min,lambda_max
FROM dbo.raw
WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')
AND CONTAINS(s_region,CIRCLE('ICRS',95.167145,-67.451324,2.0/3600.0))=1
ORDER BY mjd_obs,dp_id
```

### solar-ESPRESSO

- Start UTC: `2026-08-30T21:11:45Z`; end UTC: `2026-08-30T21:11:46Z`.
- Rows: `5`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `9649214af49236f238b56b0a3eda7baa60e237b8ee95fbfe5747c649c1000f89`.

```sql
SELECT TOP 5 dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name='ESPRESSO' AND dataproduct_type='spectrum'
AND target_name IN ('Vesta','VESTA','vesta','Ceres','CERES','ceres','Juno','JUNO','juno','Moon','MOON','moon','Ganymede','GANYMEDE','ganymede')
AND em_res_power>=40000
AND obs_release_date<='2026-08-30T21:11:25Z'
ORDER BY t_min DESC,dp_id
```

### solar-HARPS

- Start UTC: `2026-08-30T21:11:45Z`; end UTC: `2026-08-30T21:11:47Z`.
- Rows: `5`; HTTP `200`; QUERY_STATUS `OK`.
- Response VOTable SHA-256: `bf52410de0d1f1179a1ca1674a0ba1bf236a32ec27348a334686282995ef4905`.

```sql
SELECT TOP 5 dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,proposal_id,obs_release_date,obstech
FROM ivoa.ObsCore
WHERE instrument_name='HARPS' AND dataproduct_type='spectrum'
AND target_name IN ('Vesta','VESTA','vesta','Ceres','CERES','ceres','Juno','JUNO','juno','Moon','MOON','moon','Ganymede','GANYMEDE','ganymede')
AND em_res_power>=40000
AND obs_release_date<='2026-08-30T21:11:25Z'
ORDER BY t_min DESC,dp_id
```
