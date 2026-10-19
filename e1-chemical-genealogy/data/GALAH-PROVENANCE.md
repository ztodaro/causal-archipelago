# GALAH DR4 retrieval provenance

- Retrieval completed: 2026-08-30T08:09:08Z
- Release used: GALAH DR4 (no fallback)
- Service: AAO Data Central TAP sync endpoint
- Endpoint: `https://datacentral.org.au/vo/tap/sync`
- Catalog table: `galah_dr4.mainstartable` (the one-row-per-star DR4 main catalog)
- Retrieval path: inline VOTable upload of all 133,468 frozen Gaia DR3
  `source_id` values, followed by a server-side exact `BIGINT` equality join.
- Input: `m3-pathfinder/data/gaia_100pc_rv.csv`
- Input SHA-256:
  `d448975253784a2492e53ebbbea6ab55049d869effee9f7d19b3032b55792ac0`
- Exact ADQL: `galah_query.adql`
- ADQL SHA-256:
  `a2ff502530507a05a18246220bd62a245d3826bd5829204cdbfa320cfedfadba`
- Retrieval script: `../retrieve_e1.py`
- Retrieval-script SHA-256:
  `6b9c57f140df7943bd8ec03e3e6b3d1792269e4e8574c12a02186df6ad7c112b`
- Result: `galah_matches.csv`
- Result rows: 4,749
- Unique matched Gaia DR3 source IDs: 4,749
- Result SHA-256:
  `7638e2d664db878bb9807e4d76009460fcaac0a2d80f2ac86c0114ff9e53892e`

The public DR4 main table exposes no catalog-level `alpha_fe`, `e_alpha_fe`,
or `flag_alpha_fe` fields. Those three requested output columns are therefore
present but blank; they were not inferred or synthesized. The service does
expose the individual element ratios, errors, and flags, so all cheaply
returned `X_fe`, `e_X_fe`, and `flag_X_fe` triplets were retained. The output
column `snr` is the unmodified `snr_px_ccd3` value, the DR4 red-camera S/N used
in the survey's published quality recommendation; the four camera-specific S/N
columns are also retained.

For the requested count only, 981 matched stars pass the frozen E1 construction
cut: valid `fe_h`, `flag_sp = 0`, `flag_fe_h = 0`, and `snr_px_ccd3 > 30`.
No pairing, masking, abundance comparison, or downstream statistic was run.
