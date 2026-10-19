# El-Badry, Rix & Heintz (2021) nearby-pair intake provenance

- Retrieved (UTC): 2026-08-30T08:06:07Z
- Catalog: VizieR `J/MNRAS/506/2269`, table `catalog`
- Catalog description: El-Badry, Rix & Heintz (2021), *A million binaries from Gaia eDR3: sample selection and validation of Gaia parallax uncertainties*
- TAP endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync`
- Request: synchronous TAP query, ADQL, CSV output
- Selection: either component has parallax strictly greater than 9 mas
- Returned rows (excluding header): 30,574
- Output: `elbadry_nearby.csv`
- Output SHA-256: `5aa3416681d00dcbcd7e00f356e3f5159d79223a937e31c4b7d29e60ba11da07`
- Catalog ReadMe endpoint: `https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/506/2269/ReadMe`
- Saved ReadMe: `elbadry_ReadMe.txt`
- ReadMe SHA-256: `b04eb71613f35a5fe46367bb2b930eee03036018ae8ea36f73b3f72d5cca83c3`

Exact ADQL query:

```sql
SELECT
  Source1 AS source_id1,
  Source2 AS source_id2,
  Plx1 AS parallax1,
  Plx2 AS parallax2,
  sepAU AS sep_AU,
  theta AS pairdistance,
  R AS R_chance_align,
  BinType AS binary_type
FROM "J/MNRAS/506/2269/catalog"
WHERE Plx1 > 9 OR Plx2 > 9
ORDER BY Source1, Source2
```

Validation performed after retrieval was limited to intake integrity: the CSV contains 30,574 rows, both source-ID columns contain only decimal digits, and every row satisfies the stated parallax filter. No velocity, separation-distribution, pair-statistic, or project-Gaia-sample computation was performed. The project Gaia sample was not accessed.
