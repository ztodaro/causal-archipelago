# APOGEE DR17 retrieval provenance

- Retrieval completed: 2026-08-30T08:22:14Z
- Release used: SDSS APOGEE DR17 allStar catalog tables
- Service: SDSS DR17 SkyServer SQL Search web service
- Endpoint:
  `https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch`
- Catalog tables: `apogeeStar` joined to `aspcapStar` on `apstar_id`
- Retrieval path: 890 deterministic exact-ID SQL queries, with 150 frozen Gaia
  EDR3/DR3 source IDs per query except the final chunk. No positional match was
  used.
- Input: `m3-pathfinder/data/gaia_100pc_rv.csv`
- Input SHA-256:
  `d448975253784a2492e53ebbbea6ab55049d869effee9f7d19b3032b55792ac0`
- Exact SQL for every chunk: `apogee_queries.sql`
- SQL-manifest SHA-256:
  `8613f33093b2648c08ce94ec57622f395f85402b79884653f6f879607460a546`
- Retrieval script: `../retrieve_e1.py`
- Retrieval-script SHA-256:
  `6b9c57f140df7943bd8ec03e3e6b3d1792269e4e8574c12a02186df6ad7c112b`
- Result: `apogee_matches.csv`
- Result rows: 12,418
- Unique matched Gaia EDR3/DR3 source IDs: 10,042
- Result SHA-256:
  `edf401041aa142834cf1e1c364472e09f249c8b89c6086a28da0c1ef6e26c9da`

All matching allStar rows were retained, including multiple catalog entries for
the same Gaia source ID. `ASPCAP_STAR_BAD` is recorded from the official SDSS
server-side expression using `dbo.fApogeeAspcapFlag('STAR_BAD')`; it is not a
locally guessed bit mask.

For the requested count only, 5,963 catalog rows representing 4,882 unique
matched stars pass the frozen E1 construction cut: valid `FE_H`, no official
ASPCAP `STAR_BAD` bits, and `SNR > 70` (the DR17 warning threshold). No pairing,
masking, abundance comparison, or downstream statistic was run.
