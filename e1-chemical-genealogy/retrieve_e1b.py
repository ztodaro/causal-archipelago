"""Frozen E1b public-catalog intake.

This script retrieves only the three files named by E1B-SPEC.md.  It performs
selection-integrity checks, but no pair construction or scientific analysis.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import math
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
GAIA_ENDPOINT = "https://gea.esac.esa.int/tap-server/tap/sync"
CG_ENDPOINT = "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync"

GALAH_QUERY = """SELECT
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
ORDER BY gaiadr3_source_id, sobject_id"""

APOGEE_QUERY = """SELECT
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
  AND (a.ASPCAPFLAG & dbo.fApogeeAspcapFlag('STAR_BAD')) = 0"""

GAIA_COORD_QUERY = """SELECT
  t.source_id AS source_id,
  g.ra AS ra,
  g.dec AS dec
FROM TAP_UPLOAD.targets AS t
JOIN gaiaedr3.gaia_source AS g ON t.source_id = g.source_id"""

CG_QUERY = """SELECT
  \"GaiaDR2\",
  \"Cluster\",
  \"RA_ICRS\",
  \"DE_ICRS\",
  \"Plx\",
  \"proba\"
FROM \"J/A+A/640/A1/nodup\"
WHERE \"Plx\" >= 1
  AND \"proba\" >= 0.7
ORDER BY \"GaiaDR2\", \"Cluster\""""

GALAH_COLUMNS = [
    "sobject_id", "gaiadr3_source_id", "ra", "dec", "parallax",
    "parallax_error", "pmra", "pmdec", "rv", "e_rv", "snr", "teff",
    "logg", "fe_h", "e_fe_h", "flag_sp", "flag_fe_h",
]

APOGEE_RAW_COLUMNS = [
    "APOGEE_ID", "GAIAEDR3_SOURCE_ID", "GAIAEDR3_PARALLAX",
    "GAIAEDR3_PARALLAX_ERROR", "GAIAEDR3_PMRA", "GAIAEDR3_PMDEC",
    "VHELIO_AVG", "VSCATTER", "NVISITS", "SNR", "TEFF", "LOGG",
    "FE_H", "FE_H_ERR", "ALPHA_M", "ASPCAP_STAR_BAD",
]

APOGEE_COLUMNS = [
    "APOGEE_ID", "GAIAEDR3_SOURCE_ID", "GAIAEDR3_RA", "GAIAEDR3_DEC",
    "GAIAEDR3_PARALLAX", "GAIAEDR3_PMRA", "GAIAEDR3_PMDEC",
    "VHELIO_AVG", "VSCATTER", "NVISITS", "SNR", "TEFF", "LOGG",
    "FE_H", "FE_H_ERR", "ALPHA_M", "ASPCAP_STAR_BAD",
]

CG_COLUMNS = ["GaiaDR2", "Cluster", "RA_ICRS", "DE_ICRS", "Plx", "proba"]


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
    upload: bytes | None = None,
    maxrec: int = 1_000_000,
) -> tuple[str, str]:
    started = utc_now()
    payload = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "csv",
        "MAXREC": str(maxrec),
        "QUERY": query,
    }
    files = None
    if upload is not None:
        payload["UPLOAD"] = "targets,param:targets"
        files = {"targets": ("targets.xml", upload, "application/x-votable+xml")}
    response = request_with_retries(
        "POST",
        endpoint,
        data=payload,
        files=files,
        stream=True,
        timeout=(60, 7200),
    )
    save_stream(response, destination)
    return started, utc_now()


def sdss_download(query: str, destination: Path) -> tuple[str, str]:
    started = utc_now()
    response = request_with_retries(
        "GET",
        APOGEE_ENDPOINT,
        params={"cmd": query, "format": "csv"},
        stream=True,
        timeout=(60, 7200),
    )
    save_stream(response, destination)
    return started, utc_now()


def noncomment_lines(handle: Iterable[str]) -> Iterator[str]:
    for line in handle:
        if line.strip() and not line.startswith("#"):
            yield line


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(noncomment_lines(handle))
        rows = list(reader)
        if reader.fieldnames is None:
            raise RuntimeError(f"no CSV header in {path}")
        return list(reader.fieldnames), rows


def write_rows(path: Path, columns: list[str], rows: Iterable[dict[str, str]]) -> None:
    partial = path.with_suffix(path.suffix + ".partial")
    with partial.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(partial, path)


def require_columns(actual: list[str], expected: list[str], label: str) -> None:
    if actual != expected:
        raise RuntimeError(f"{label} columns differ:\nactual={actual}\nexpected={expected}")


def exact_decimal(value: str, label: str) -> None:
    if not value or not value.isdecimal():
        raise RuntimeError(f"{label} is not an exact decimal integer string: {value!r}")


def target_votable(source_ids: Iterable[str]) -> bytes:
    rows = "".join(f"<TR><TD>{html.escape(value)}</TD></TR>" for value in source_ids)
    xml = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<VOTABLE version='1.3' xmlns='http://www.ivoa.net/xml/VOTable/v1.3'>"
        "<RESOURCE><TABLE name='targets'><FIELD name='source_id' datatype='long'/>"
        f"<DATA><TABLEDATA>{rows}</TABLEDATA></DATA></TABLE></RESOURCE></VOTABLE>"
    )
    return xml.encode("utf-8")


def provenance(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def retrieve_galah() -> None:
    output = DATA / "e1b_galah.csv"
    print("GALAH: downloading frozen server-side selection", flush=True)
    started, completed = tap_download(GALAH_ENDPOINT, GALAH_QUERY, output)
    fields, rows = read_rows(output)
    require_columns(fields, GALAH_COLUMNS, "GALAH")
    ids: set[str] = set()
    for row in rows:
        exact_decimal(row["sobject_id"], "GALAH sobject_id")
        exact_decimal(row["gaiadr3_source_id"], "GALAH gaiadr3_source_id")
        if row["gaiadr3_source_id"] in ids:
            raise RuntimeError("duplicate GALAH Gaia source_id")
        ids.add(row["gaiadr3_source_id"])
        if not (
            int(row["flag_sp"]) == 0
            and int(row["flag_fe_h"]) == 0
            and float(row["snr"]) > 30
            and float(row["parallax"]) >= 1
            and float(row["parallax_error"]) > 0
            and float(row["parallax"]) / float(row["parallax_error"]) >= 10
            and row["rv"] != ""
            and row["fe_h"] != ""
        ):
            raise RuntimeError("GALAH row violates frozen selection")
    digest = sha256(output)
    provenance(
        DATA / "E1B-GALAH-PROVENANCE.md",
        f"""# E1b GALAH DR4 intake provenance

- Retrieval started (UTC): {started}
- Retrieval completed (UTC): {completed}
- Endpoint: `{GALAH_ENDPOINT}`
- Tables: `galah_dr4.mainstartable`, exact join to `galah_dr4.vacxmatchtable`
- Result: `e1b_galah.csv`
- Rows: {len(rows):,}
- Unique Gaia DR3 source IDs: {len(ids):,}
- SHA-256: `{digest}`

`rv` and `e_rv` are the DR4 primary-component fields `rv_comp_1` and
`e_rv_comp_1`. `snr` is the survey's `snr_px_ccd3`. Gaia position,
parallax, and proper motion are native fields from the DR4 Gaia crossmatch VAC.

Exact ADQL:

```sql
{GALAH_QUERY}
```

Validation was limited to schema, decimal-ID, uniqueness, and frozen-cut
integrity. No pairs or scientific statistics were computed.""",
    )
    print(f"GALAH: {len(rows)} rows, sha256={digest}", flush=True)


def retrieve_apogee() -> None:
    raw = DATA / "e1b_apogee.skyserver.raw.csv"
    coords = DATA / "e1b_apogee.gaiaedr3.coords.csv"
    output = DATA / "e1b_apogee.csv"
    print("APOGEE: downloading frozen server-side selection", flush=True)
    started, catalog_completed = sdss_download(APOGEE_QUERY, raw)
    fields, rows = read_rows(raw)
    require_columns(fields, APOGEE_RAW_COLUMNS, "APOGEE raw")
    source_ids: set[str] = set()
    for row in rows:
        source_id = row["GAIAEDR3_SOURCE_ID"]
        exact_decimal(source_id, "APOGEE GAIAEDR3_SOURCE_ID")
        source_ids.add(source_id)
        parallax = float(row["GAIAEDR3_PARALLAX"])
        parallax_error = float(row["GAIAEDR3_PARALLAX_ERROR"])
        if not (
            parallax >= 1
            and parallax_error > 0
            and parallax / parallax_error >= 10
            and float(row["SNR"]) > 70
            and float(row["VHELIO_AVG"]) > -999
            and float(row["FE_H"]) > -999
            and int(row["ASPCAP_STAR_BAD"]) == 0
        ):
            raise RuntimeError("APOGEE row violates frozen selection")

    sorted_ids = sorted(source_ids, key=int)
    print(f"APOGEE: exact Gaia EDR3 coordinate join for {len(sorted_ids)} unique IDs", flush=True)
    gaia_started, gaia_completed = tap_download(
        GAIA_ENDPOINT,
        GAIA_COORD_QUERY,
        coords,
        upload=target_votable(sorted_ids),
        maxrec=len(sorted_ids) + 10,
    )
    coord_fields, coord_rows = read_rows(coords)
    require_columns(coord_fields, ["source_id", "ra", "dec"], "Gaia EDR3 coordinates")
    coord_map: dict[str, tuple[str, str]] = {}
    for row in coord_rows:
        source_id = row["source_id"]
        exact_decimal(source_id, "Gaia EDR3 source_id")
        if source_id in coord_map:
            raise RuntimeError("duplicate Gaia EDR3 coordinate row")
        coord_map[source_id] = (row["ra"], row["dec"])
    missing = source_ids.difference(coord_map)
    extra = coord_map.keys() - source_ids
    if missing or extra:
        raise RuntimeError(f"Gaia coordinate join mismatch: missing={len(missing)}, extra={len(extra)}")

    rows.sort(
        key=lambda row: (
            int(row["GAIAEDR3_SOURCE_ID"]),
            row["APOGEE_ID"],
            -float(row["SNR"]) if row["SNR"] else math.inf,
        )
    )
    for row in rows:
        row["GAIAEDR3_RA"], row["GAIAEDR3_DEC"] = coord_map[row["GAIAEDR3_SOURCE_ID"]]
    write_rows(output, APOGEE_COLUMNS, rows)
    raw.unlink()
    coords.unlink()
    digest = sha256(output)
    provenance(
        DATA / "E1B-APOGEE-PROVENANCE.md",
        f"""# E1b APOGEE DR17 intake provenance

- Catalog retrieval started (UTC): {started}
- Catalog retrieval completed (UTC): {catalog_completed}
- Catalog endpoint: `{APOGEE_ENDPOINT}`
- Catalog tables: `apogeeStar`, exact join to `aspcapStar` on `apstar_id`
- Gaia-coordinate retrieval started (UTC): {gaia_started}
- Gaia-coordinate retrieval completed (UTC): {gaia_completed}
- Gaia EDR3 TAP endpoint: `{GAIA_ENDPOINT}`
- Gaia coordinate table: `gaiaedr3.gaia_source`
- Result: `e1b_apogee.csv`
- Rows: {len(rows):,}
- Unique Gaia EDR3 source IDs: {len(source_ids):,}
- Exact Gaia coordinate matches: {len(coord_map):,}
- SHA-256: `{digest}`

SkyServer's DR17 `apogeeStar` table contains Gaia EDR3 source ID, parallax,
and proper motions but not Gaia EDR3 RA/Dec. The two requested coordinate
columns were therefore retrieved by an exact source-ID upload join to the
official Gaia EDR3 archive. No sky match or coordinate substitution was used.

Exact SkyServer SQL:

```sql
{APOGEE_QUERY}
```

Exact Gaia EDR3 ADQL:

```sql
{GAIA_COORD_QUERY}
```

Validation was limited to schema, decimal-ID, coordinate-join, and frozen-cut
integrity. No pairs or scientific statistics were computed.""",
    )
    print(f"APOGEE: {len(rows)} rows, {len(source_ids)} unique IDs, sha256={digest}", flush=True)


def retrieve_cg() -> None:
    output = DATA / "e1b_cg_members.csv"
    print("Cantat-Gaudin: downloading frozen membership mask", flush=True)
    started, completed = tap_download(CG_ENDPOINT, CG_QUERY, output)
    fields, rows = read_rows(output)
    require_columns(fields, CG_COLUMNS, "Cantat-Gaudin")
    ids: set[str] = set()
    for row in rows:
        exact_decimal(row["GaiaDR2"], "Cantat-Gaudin GaiaDR2")
        ids.add(row["GaiaDR2"])
        if not (float(row["Plx"]) >= 1 and float(row["proba"]) >= 0.7):
            raise RuntimeError("Cantat-Gaudin row violates frozen selection")
    digest = sha256(output)
    provenance(
        DATA / "E1B-CG-PROVENANCE.md",
        f"""# E1b Cantat-Gaudin 2020 member intake provenance

- Retrieval started (UTC): {started}
- Retrieval completed (UTC): {completed}
- Endpoint: `{CG_ENDPOINT}`
- VizieR catalog: `J/A+A/640/A1`, table `nodup`
- Result: `e1b_cg_members.csv`
- Rows: {len(rows):,}
- Unique Gaia DR2 source IDs: {len(ids):,}
- SHA-256: `{digest}`

Exact ADQL:

```sql
{CG_QUERY}
```

Validation was limited to schema, decimal-ID, and frozen-cut integrity. This
file is an intake-only masking list; no pairing or scientific statistic was
computed.""",
    )
    print(f"Cantat-Gaudin: {len(rows)} rows, sha256={digest}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pull", choices=("galah", "apogee", "cg", "all"), default="all", nargs="?")
    args = parser.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)
    if args.pull in {"galah", "all"}:
        retrieve_galah()
    if args.pull in {"apogee", "all"}:
        retrieve_apogee()
    if args.pull in {"cg", "all"}:
        retrieve_cg()


if __name__ == "__main__":
    main()
