"""Frozen E2b El-Badry catalog intake; no pair analysis."""

from __future__ import annotations

import csv
import hashlib
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
ENDPOINT = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"
CATALOG_URL = "https://zenodo.org/records/4435257"
TABLE = "J/MNRAS/506/2269/catalog"
MAXREC = 200_000
EXPECTED_ROWS = 125_713
EXPECTED_COLUMNS = 220

QUERY = """SELECT *
FROM \"J/MNRAS/506/2269/catalog\"
WHERE (Plx1 >= 5 OR Plx2 >= 5)
  AND R < 0.1
ORDER BY \"Source1\", \"Source2\""""

COUNT_QUERY = """SELECT COUNT(*) AS n
FROM \"J/MNRAS/506/2269/catalog\"
WHERE (Plx1 >= 5 OR Plx2 >= 5)
  AND R < 0.1"""

REQUIRED_PUBLISHED_COLUMNS = {
    "Source1", "Source2",
    "Plx1", "Plx2", "e_Plx1", "e_Plx2", "RPlx1", "RPlx2",
    "pmRA1", "pmRA2", "e_pmRA1", "e_pmRA2",
    "pmDE1", "pmDE2", "e_pmDE1", "e_pmDE2",
    "epsi1", "epsi2", "sepsi1", "sepsi2",
    "IPDfmp1", "IPDfmp2", "RUWE1", "RUWE2",
    "Gmag1", "Gmag2", "BPmag1", "BPmag2", "RPmag1", "RPmag2",
    "sepAU", "theta", "R", "BinType",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def request_with_retries() -> requests.Response:
    payload = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "csv",
        "MAXREC": str(MAXREC),
        "QUERY": QUERY,
    }
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = requests.post(
                ENDPOINT,
                data=payload,
                stream=True,
                timeout=(60, 7200),
            )
            if response.status_code in {429, 500, 502, 503, 504}:
                raise requests.HTTPError(f"HTTP {response.status_code}")
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            last_error = error
            if attempt == 3:
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"VizieR request failed after retries: {last_error}")


def download(destination: Path) -> tuple[str, str]:
    started = utc_now()
    response = request_with_retries()
    partial = destination.with_suffix(destination.suffix + ".partial")
    with partial.open("wb") as handle:
        for block in response.iter_content(chunk_size=1024 * 1024):
            if block:
                handle.write(block)
    head = partial.read_bytes()[:1000].lstrip()
    content_type = response.headers.get("Content-Type", "").lower()
    if head.startswith(b"<") or "xml" in content_type:
        preview = partial.read_text(encoding="utf-8", errors="replace")[:5000]
        raise RuntimeError(f"VizieR returned XML instead of CSV:\n{preview}")
    os.replace(partial, destination)
    return started, utc_now()


def validate(path: Path) -> tuple[int, int, list[str]]:
    row_count = 0
    source_ids: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(line for line in handle if line.strip() and not line.startswith("#"))
        if reader.fieldnames is None:
            raise RuntimeError("download has no CSV header")
        columns = list(reader.fieldnames)
        missing = REQUIRED_PUBLISHED_COLUMNS.difference(columns)
        if missing:
            raise RuntimeError(f"published columns missing from SELECT * result: {sorted(missing)}")
        if len(columns) != EXPECTED_COLUMNS:
            raise RuntimeError(f"expected {EXPECTED_COLUMNS} published columns, found {len(columns)}")
        for row in reader:
            row_count += 1
            for name in ("Source1", "Source2"):
                value = row[name]
                if not value or not value.isdecimal():
                    raise RuntimeError(f"{name} is not an exact integer string: {value!r}")
                source_ids.add(value)
            for name in ("dr2Source1", "dr2Source2"):
                value = row.get(name, "")
                if value and not value.isdecimal():
                    raise RuntimeError(f"{name} is not an exact integer string: {value!r}")
            if not (
                (float(row["Plx1"]) >= 5 or float(row["Plx2"]) >= 5)
                and float(row["R"]) < 0.1
            ):
                raise RuntimeError("row violates the frozen intake selection")
    if row_count != EXPECTED_ROWS:
        raise RuntimeError(f"row-count mismatch: expected {EXPECTED_ROWS}, found {row_count}")
    if row_count >= MAXREC:
        raise RuntimeError(f"result may have hit MAXREC={MAXREC}")
    return row_count, len(source_ids), columns


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    output = DATA / "e2b_elbadry_200pc.csv"
    print(f"E2b: downloading SELECT * with MAXREC={MAXREC}", flush=True)
    started, completed = download(output)
    rows, unique_sources, columns = validate(output)
    digest = sha256(output)
    provenance = DATA / "PROVENANCE-e2b_elbadry_200pc.md"
    provenance.write_text(
        f"""# E2b El-Badry powered-sample intake provenance

- Retrieval started (UTC): {started}
- Retrieval completed (UTC): {completed}
- Published catalog: El-Badry, Rix & Heintz (2021), `gaia_edr3_binaries`
- Canonical release URL: `{CATALOG_URL}`
- Query service: VizieR TAP
- Endpoint: `{ENDPOINT}`
- Table: `{TABLE}`
- Explicit `MAXREC`: {MAXREC:,}
- Independent pre-download `COUNT(*)`: {EXPECTED_ROWS:,}
- Returned rows: {rows:,}
- Returned published columns: {len(columns)}
- Unique EDR3/DR3 source IDs across both components: {unique_sources:,}
- Output: `e2b_elbadry_200pc.csv`
- SHA-256: `{digest}`
- Row-cap check: returned count equals `COUNT(*)` and is below `MAXREC`

Exact ADQL:

```sql
{QUERY}
```

Exact count query:

```sql
{COUNT_QUERY}
```

## Step 2 decision

No Gaia DR3 quality join was needed. The published table contains, for both
components, `RUWE1/2`, `IPDfmp1/2` (ipd_frac_multi_peak), `epsi1/2`
(astrometric_excess_noise), `sepsi1/2` (astrometric_excess_noise_sig),
`RPlx1/2` (parallax_over_error), `e_pmRA1/2`, and `e_pmDE1/2`.

Validation was limited to schema completeness, exact decimal identifiers,
the two frozen intake predicates, and the explicit row-cap check. No other
filter, derived column, pair analysis, or sealed statistic was applied.
""",
        encoding="utf-8",
    )
    print(
        f"E2b: rows={rows}, columns={len(columns)}, unique_sources={unique_sources}, sha256={digest}",
        flush=True,
    )


if __name__ == "__main__":
    main()
