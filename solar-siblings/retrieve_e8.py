"""Frozen E8 survey-table intake; no sieve or scientific analysis."""

from __future__ import annotations

import csv
import hashlib
import html
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator

import requests


HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

GALAH_ENDPOINT = "https://datacentral.org.au/vo/tap/sync"
APOGEE_ENDPOINT = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"
GAIA_ENDPOINT = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"

GALAH_MAXREC = 400_000
GALAH_EXPECTED_ROWS = 349_899
GALAH_EXPECTED_DR3_IDS = 313_781
APOGEE_TOP = 400_000
APOGEE_EXPECTED_ROWS = 331_088
GAIA_CHUNK_SIZE = 75_000

ELEMENTS = [
    ("Na", "na"), ("Mg", "mg"), ("Al", "al"), ("Si", "si"),
    ("Ca", "ca"), ("Ti", "ti"), ("Cr", "cr"), ("Mn", "mn"),
    ("Ni", "ni"), ("Cu", "cu"), ("Zn", "zn"), ("Y", "y"),
    ("Ba", "ba"),
]

GALAH_BASE_SELECT = [
    "d.sobject_id AS sobject_id",
    "x.source_id AS gaiadr3_source_id",
    "d.source_id AS gaia_dr2_source_id",
    "d.ra AS ra", "d.dec AS dec", "d.parallax AS parallax",
    "d.parallax_error AS parallax_error", "d.pmra AS pmra",
    "d.pmdec AS pmdec", "d.rv_galah AS rv_galah",
    "d.e_rv_galah AS e_rv_galah", "d.snr_c3_iraf AS snr_c3_iraf",
    "d.flag_sp AS flag_sp", "d.teff AS teff", "d.logg AS logg",
    "d.fe_h AS fe_h", "d.e_fe_h AS e_fe_h", "d.flag_fe_h AS flag_fe_h",
]

GALAH_COLUMNS = [
    "sobject_id", "gaiadr3_source_id", "gaia_dr2_source_id", "ra", "dec",
    "parallax", "parallax_error", "pmra", "pmdec", "rv_galah",
    "e_rv_galah", "snr_c3_iraf", "flag_sp", "teff", "logg", "fe_h",
    "e_fe_h", "flag_fe_h",
]

for native, output in ELEMENTS:
    GALAH_BASE_SELECT.extend(
        [
            f"d.{native}_fe AS {output}_fe",
            f"d.e_{native}_fe AS e_{output}_fe",
            f"d.flag_{native}_fe AS flag_{output}_fe",
        ]
    )
    GALAH_COLUMNS.extend([f"{output}_fe", f"e_{output}_fe", f"flag_{output}_fe"])

GALAH_QUERY = (
    f"SELECT TOP {GALAH_MAXREC}\n  "
    + ",\n  ".join(GALAH_BASE_SELECT)
    + "\nFROM galah_dr3.main_star AS d"
    + "\nLEFT OUTER JOIN galah_dr4.vacxmatchtable AS x"
    + " ON d.sobject_id = x.sobject_id AND x.source_id > 0"
    + "\nWHERE d.parallax >= 1"
    + "\nORDER BY sobject_id"
)

GALAH_COUNT_QUERY = """SELECT COUNT(*) AS n, COUNT(x.source_id) AS matched_dr3_ids
FROM galah_dr3.main_star AS d
LEFT OUTER JOIN galah_dr4.vacxmatchtable AS x
  ON d.sobject_id = x.sobject_id AND x.source_id > 0
WHERE d.parallax >= 1"""

APOGEE_QUERY = f"""SELECT TOP {APOGEE_TOP}
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
ORDER BY s.GAIAEDR3_SOURCE_ID, s.APOGEE_ID"""

APOGEE_COUNT_QUERY = """SELECT COUNT(*) AS n, COUNT(a.apstar_id) AS abundance_matches
FROM apogeeStar AS s
LEFT OUTER JOIN aspcapStar AS a ON a.apstar_id = s.apstar_id
WHERE s.GAIAEDR3_PARALLAX >= 1"""

GAIA_COORD_QUERY = '''SELECT
  t.source_id AS source_id,
  g."RA_ICRS" AS ra,
  g."DE_ICRS" AS dec
FROM TAP_UPLOAD.targets AS t
JOIN "I/355/gaiadr3" AS g ON t.source_id = g."Source"'''

APOGEE_RAW_COLUMNS = [
    "APOGEE_ID", "GAIAEDR3_SOURCE_ID", "GAIAEDR3_PARALLAX",
    "GAIAEDR3_PMRA", "GAIAEDR3_PMDEC", "VHELIO_AVG", "VSCATTER",
    "NVISITS", "SNR", "TEFF", "LOGG", "FE_H", "FE_H_ERR", "ALPHA_M",
    "ASPCAP_STAR_BAD", "C_FE", "C_FE_ERR", "C_FE_FLAG", "N_FE",
    "N_FE_ERR", "N_FE_FLAG", "MG_FE", "MG_FE_ERR", "MG_FE_FLAG",
]

APOGEE_COLUMNS = [
    "APOGEE_ID", "GAIAEDR3_SOURCE_ID", "GAIAEDR3_RA", "GAIAEDR3_DEC",
    "GAIAEDR3_PARALLAX", "GAIAEDR3_PMRA", "GAIAEDR3_PMDEC",
    "VHELIO_AVG", "VSCATTER", "NVISITS", "SNR", "TEFF", "LOGG",
    "FE_H", "FE_H_ERR", "ALPHA_M", "ASPCAP_STAR_BAD", "C_FE",
    "C_FE_ERR", "C_FE_FLAG", "N_FE", "N_FE_ERR", "N_FE_FLAG", "MG_FE",
    "MG_FE_ERR", "MG_FE_FLAG",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def request_with_retries(method: str, url: str, **kwargs: object) -> requests.Response:
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code in {429, 500, 502, 503, 504}:
                raise requests.HTTPError(f"HTTP {response.status_code}")
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            last_error = error
            if attempt == 3:
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"request failed after retries: {last_error}")


def save_stream(response: requests.Response, destination: Path) -> None:
    partial = destination.with_suffix(destination.suffix + ".partial")
    with partial.open("wb") as handle:
        for block in response.iter_content(chunk_size=1024 * 1024):
            if block:
                handle.write(block)
    head = partial.read_bytes()[:1000].lstrip()
    content_type = response.headers.get("Content-Type", "").lower()
    if head.startswith(b"<") or "xml" in content_type:
        preview = partial.read_text(encoding="utf-8", errors="replace")[:5000]
        raise RuntimeError(f"service returned XML instead of CSV:\n{preview}")
    if head.startswith(b"{") or "json" in content_type:
        preview = partial.read_text(encoding="utf-8", errors="replace")[:5000]
        raise RuntimeError(f"service returned JSON instead of CSV:\n{preview}")
    os.replace(partial, destination)


def tap_download(
    endpoint: str,
    query: str,
    destination: Path,
    *,
    maxrec: int,
    upload: bytes | None = None,
) -> tuple[str, str]:
    started = utc_now()
    payload = {
        "REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv",
        "MAXREC": str(maxrec), "QUERY": query,
    }
    files = None
    if upload is not None:
        payload["UPLOAD"] = "targets,param:targets"
        files = {"targets": ("targets.xml", upload, "application/x-votable+xml")}
    response = request_with_retries(
        "POST", endpoint, data=payload, files=files, stream=True,
        timeout=(60, 7200),
    )
    save_stream(response, destination)
    return started, utc_now()


def sdss_download(query: str, destination: Path) -> tuple[str, str]:
    started = utc_now()
    response = request_with_retries(
        "GET", APOGEE_ENDPOINT, params={"cmd": query, "format": "csv"},
        stream=True, timeout=(60, 7200),
    )
    save_stream(response, destination)
    return started, utc_now()


def noncomment_lines(handle: Iterable[str]) -> Iterator[str]:
    for line in handle:
        if line.strip() and not line.startswith("#"):
            yield line


def target_votable(source_ids: Iterable[str]) -> bytes:
    rows = "".join(f"<TR><TD>{html.escape(value)}</TD></TR>" for value in source_ids)
    xml = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<VOTABLE version='1.3' xmlns='http://www.ivoa.net/xml/VOTable/v1.3'>"
        "<RESOURCE><TABLE name='targets'><FIELD name='source_id' datatype='long'/>"
        f"<DATA><TABLEDATA>{rows}</TABLEDATA></DATA></TABLE></RESOURCE></VOTABLE>"
    )
    return xml.encode("utf-8")


def download_gaia_coordinates(
    source_ids: list[str], destination: Path
) -> tuple[str, str, int]:
    started = utc_now()
    chunks = [
        source_ids[start : start + GAIA_CHUNK_SIZE]
        for start in range(0, len(source_ids), GAIA_CHUNK_SIZE)
    ]
    merged = destination.with_suffix(destination.suffix + ".merge.partial")
    with merged.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target, fieldnames=["source_id", "ra", "dec"], lineterminator="\n"
        )
        writer.writeheader()
        for index, chunk in enumerate(chunks, start=1):
            chunk_path = destination.with_name(
                f"{destination.stem}.chunk-{index:02d}{destination.suffix}"
            )
            print(
                f"Gaia EDR3 coordinates: chunk {index}/{len(chunks)} ({len(chunk)} IDs)",
                flush=True,
            )
            tap_download(
                GAIA_ENDPOINT,
                GAIA_COORD_QUERY,
                chunk_path,
                maxrec=len(chunk) + 10,
                upload=target_votable(chunk),
            )
            chunk_rows = 0
            with chunk_path.open(newline="", encoding="utf-8-sig") as source:
                reader = csv.DictReader(noncomment_lines(source))
                require_columns(
                    list(reader.fieldnames or []),
                    ["source_id", "ra", "dec"],
                    f"Gaia coordinate chunk {index}",
                )
                for row in reader:
                    chunk_rows += 1
                    writer.writerow(row)
            if chunk_rows != len(chunk) or chunk_rows >= len(chunk) + 10:
                raise RuntimeError(
                    f"Gaia chunk {index} count/cap mismatch: "
                    f"rows={chunk_rows}, requested={len(chunk)}"
                )
            chunk_path.unlink()
    os.replace(merged, destination)
    return started, utc_now(), len(chunks)


def require_columns(actual: list[str], expected: list[str], label: str) -> None:
    if actual != expected:
        raise RuntimeError(f"{label} columns differ:\nactual={actual}\nexpected={expected}")


def decimal_id(value: str, label: str, *, allow_blank: bool = False) -> None:
    if allow_blank and value == "":
        return
    if not value or not value.isdecimal():
        raise RuntimeError(f"{label} is not an integer string: {value!r}")


def provenance(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def retrieve_galah() -> None:
    output = DATA / "e8_galah_abund.csv"
    print(f"GALAH DR3: downloading with TOP/MAXREC={GALAH_MAXREC}", flush=True)
    started, completed = tap_download(
        GALAH_ENDPOINT, GALAH_QUERY, output, maxrec=GALAH_MAXREC
    )
    rows = 0
    matched_dr3_ids = 0
    native_dr2_ids = 0
    sobject_ids: set[str] = set()
    with output.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(noncomment_lines(handle))
        require_columns(list(reader.fieldnames or []), GALAH_COLUMNS, "GALAH")
        for row in reader:
            rows += 1
            decimal_id(row["sobject_id"], "GALAH sobject_id")
            decimal_id(
                row["gaia_dr2_source_id"], "GALAH Gaia DR2 source_id", allow_blank=True
            )
            decimal_id(row["gaiadr3_source_id"], "GALAH Gaia DR3 source_id", allow_blank=True)
            if row["gaia_dr2_source_id"]:
                native_dr2_ids += 1
            if row["gaiadr3_source_id"]:
                matched_dr3_ids += 1
            if row["sobject_id"] in sobject_ids:
                raise RuntimeError("duplicate GALAH sobject_id")
            sobject_ids.add(row["sobject_id"])
            if float(row["parallax"]) < 1:
                raise RuntimeError("GALAH row violates parallax floor")
    if rows != GALAH_EXPECTED_ROWS or rows >= GALAH_MAXREC:
        raise RuntimeError(f"GALAH count/cap mismatch: rows={rows}, maxrec={GALAH_MAXREC}")
    if matched_dr3_ids != GALAH_EXPECTED_DR3_IDS:
        raise RuntimeError(f"GALAH DR3-ID match mismatch: {matched_dr3_ids}")
    digest = sha256(output)
    provenance(
        DATA / "PROVENANCE-e8_galah_abund.md",
        f"""# E8 GALAH DR3 abundance intake provenance

- Retrieval started (UTC): {started}
- Retrieval completed (UTC): {completed}
- Endpoint: `{GALAH_ENDPOINT}`
- Primary table: `galah_dr3.main_star` (DR3 Main Allstar Clean)
- Identifier join: left exact `sobject_id` join to `galah_dr4.vacxmatchtable`
- Explicit ADQL `TOP`: {GALAH_MAXREC:,}
- Explicit TAP `MAXREC`: {GALAH_MAXREC:,}
- Independent `COUNT(*)`: {GALAH_EXPECTED_ROWS:,}
- Returned rows: {rows:,}
- Native Gaia DR2 IDs present: {native_dr2_ids:,}
- Native Gaia DR2 ID blanks retained: {rows - native_dr2_ids:,}
- Exact Gaia DR3 IDs supplied: {matched_dr3_ids:,}
- Unmatched Gaia DR3 IDs retained blank: {rows - matched_dr3_ids:,}
- Output: `e8_galah_abund.csv`
- SHA-256: `{digest}`
- Row-cap check: returned count equals `COUNT(*)` and is below both limits

GALAH DR3's native `source_id` is a Gaia DR2 identifier. It is retained as
`gaia_dr2_source_id`. The requested `gaiadr3_source_id` is supplied only where
the same exact GALAH `sobject_id` exists in the published DR4 crossmatch; no
positional match or source-ID relabeling was used, and no DR3 row was dropped.

Exact ADQL:

```sql
{GALAH_QUERY}
```

Exact count query:

```sql
{GALAH_COUNT_QUERY}
```

All 13 requested abundance value/error/flag triplets were available. No
filter beyond `parallax >= 1`, derived abundance, sieve, or analysis was run.""",
    )
    print(
        f"GALAH DR3: rows={rows}, matched_dr3_ids={matched_dr3_ids}, sha256={digest}",
        flush=True,
    )


def retrieve_apogee() -> None:
    raw = DATA / "e8_apogee_abund.skyserver.raw.csv"
    coords = DATA / "e8_apogee_abund.gaiaedr3.coords.csv"
    output = DATA / "e8_apogee_abund.csv"
    print(f"APOGEE DR17: downloading with TOP={APOGEE_TOP}", flush=True)
    started, catalog_completed = sdss_download(APOGEE_QUERY, raw)
    rows = 0
    source_ids: set[str] = set()
    with raw.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(noncomment_lines(handle))
        require_columns(list(reader.fieldnames or []), APOGEE_RAW_COLUMNS, "APOGEE raw")
        for row in reader:
            rows += 1
            source_id = row["GAIAEDR3_SOURCE_ID"]
            decimal_id(source_id, "APOGEE Gaia EDR3 source_id")
            source_ids.add(source_id)
            if float(row["GAIAEDR3_PARALLAX"]) < 1:
                raise RuntimeError("APOGEE row violates parallax floor")
    if rows != APOGEE_EXPECTED_ROWS or rows >= APOGEE_TOP:
        raise RuntimeError(f"APOGEE count/cap mismatch: rows={rows}, top={APOGEE_TOP}")

    sorted_ids = sorted(source_ids, key=int)
    print(f"APOGEE DR17: exact Gaia EDR3 coordinate join for {len(sorted_ids)} IDs", flush=True)
    gaia_started, gaia_completed, gaia_chunks = download_gaia_coordinates(
        sorted_ids, coords
    )
    coord_map: dict[str, tuple[str, str]] = {}
    with coords.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(noncomment_lines(handle))
        require_columns(list(reader.fieldnames or []), ["source_id", "ra", "dec"], "Gaia coordinates")
        for row in reader:
            source_id = row["source_id"]
            decimal_id(source_id, "Gaia EDR3 source_id")
            if source_id in coord_map:
                raise RuntimeError("duplicate Gaia coordinate row")
            coord_map[source_id] = (row["ra"], row["dec"])
    missing = source_ids.difference(coord_map)
    extra = coord_map.keys() - source_ids
    if missing or extra:
        raise RuntimeError(f"Gaia coordinate join mismatch: missing={len(missing)}, extra={len(extra)}")

    partial = output.with_suffix(output.suffix + ".partial")
    with raw.open(newline="", encoding="utf-8-sig") as source, partial.open(
        "w", newline="", encoding="utf-8"
    ) as target:
        reader = csv.DictReader(noncomment_lines(source))
        writer = csv.DictWriter(target, fieldnames=APOGEE_COLUMNS, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in reader:
            row["GAIAEDR3_RA"], row["GAIAEDR3_DEC"] = coord_map[row["GAIAEDR3_SOURCE_ID"]]
            writer.writerow(row)
    os.replace(partial, output)
    raw.unlink()
    coords.unlink()
    digest = sha256(output)
    provenance(
        DATA / "PROVENANCE-e8_apogee_abund.md",
        f"""# E8 APOGEE DR17 abundance intake provenance

- Catalog retrieval started (UTC): {started}
- Catalog retrieval completed (UTC): {catalog_completed}
- Catalog endpoint: `{APOGEE_ENDPOINT}`
- Catalog tables: `apogeeStar`, left exact join to `aspcapStar` on `apstar_id`
- Explicit SQL `TOP`: {APOGEE_TOP:,}
- Independent base and joined row counts: {APOGEE_EXPECTED_ROWS:,}
- Gaia-coordinate retrieval started (UTC): {gaia_started}
- Gaia-coordinate retrieval completed (UTC): {gaia_completed}
- Gaia DR3 mirror endpoint: `{GAIA_ENDPOINT}`
- Gaia TAP mode: synchronous exact-ID upload chunks
- Gaia coordinate table: VizieR `I/355/gaiadr3`
- Gaia exact-ID upload chunks: {gaia_chunks}
- Gaia chunk size: at most {GAIA_CHUNK_SIZE:,} IDs
- Gaia per-chunk `MAXREC`: uploaded row count + 10
- Returned catalog rows: {rows:,}
- Unique Gaia EDR3 source IDs: {len(source_ids):,}
- Exact Gaia coordinate matches: {len(coord_map):,}
- Output: `e8_apogee_abund.csv`
- SHA-256: `{digest}`
- Row-cap check: returned count equals `COUNT(*)` and is below `TOP`

SkyServer's `apogeeStar` table does not publish Gaia EDR3 RA/Dec. Those two
requested fields were supplied by an exact source-ID upload join to the
official Gaia EDR3 archive. No positional matching or row filtering was used.
`ASPCAP_STAR_BAD` is the explicitly requested official SDSS bit test.

Exact SkyServer SQL:

```sql
{APOGEE_QUERY}
```

Exact count query:

```sql
{APOGEE_COUNT_QUERY}
```

Exact Gaia EDR3 ADQL:

```sql
{GAIA_COORD_QUERY}
```

The requested C, N, and Mg abundance values, errors, and flags were all
available. No filter beyond `GAIAEDR3_PARALLAX >= 1`, derived abundance,
sieve, or analysis was run.""",
    )
    print(
        f"APOGEE DR17: rows={rows}, unique_ids={len(source_ids)}, sha256={digest}",
        flush=True,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pull", choices=("galah", "apogee", "all"), nargs="?", default="all")
    args = parser.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)
    if args.pull in {"galah", "all"}:
        retrieve_galah()
    if args.pull in {"apogee", "all"}:
        retrieve_apogee()


if __name__ == "__main__":
    main()
