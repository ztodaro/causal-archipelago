"""Frozen-input E1 archive intake: exact Gaia-ID joins only.

This script deliberately performs no pair construction, masking, or abundance
comparison.  It writes the two preregistered survey match tables.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

import requests


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "m3-pathfinder" / "data" / "gaia_100pc_rv.csv"
DATA = Path(__file__).resolve().parent / "data"
EXPECTED_SHA256 = "d448975253784a2492e53ebbbea6ab55049d869effee9f7d19b3032b55792ac0"
EXPECTED_ROWS = 133_468

GALAH_ENDPOINT = "https://datacentral.org.au/vo/tap/sync"
APOGEE_ENDPOINT = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"

GALAH_ELEMENTS = [
    "c", "n", "o", "na", "mg", "al", "si", "k", "ca", "sc", "ti",
    "v", "cr", "mn", "co", "ni", "cu", "zn", "rb", "sr", "y",
    "zr", "mo", "ru", "ba", "la", "ce", "nd", "sm", "eu",
]

GALAH_BASE_COLUMNS = [
    "sobject_id", "gaiadr3_source_id", "snr", "snr_px_ccd1",
    "snr_px_ccd2", "snr_px_ccd3", "snr_px_ccd4", "teff", "logg",
    "fe_h", "e_fe_h", "flag_sp", "flag_fe_h",
]
GALAH_ALPHA_COLUMNS = ["alpha_fe", "e_alpha_fe", "flag_alpha_fe"]
GALAH_ELEMENT_COLUMNS = [
    name
    for element in GALAH_ELEMENTS
    for name in (f"{element}_fe", f"e_{element}_fe", f"flag_{element}_fe")
]
GALAH_OUTPUT_COLUMNS = GALAH_BASE_COLUMNS + GALAH_ALPHA_COLUMNS + GALAH_ELEMENT_COLUMNS

APOGEE_OUTPUT_COLUMNS = [
    "APOGEE_ID", "GAIAEDR3_SOURCE_ID", "SNR", "TEFF", "LOGG", "FE_H",
    "FE_H_ERR", "ALPHA_M", "ASPCAPFLAG", "STARFLAG", "VHELIO_AVG",
    "VSCATTER", "NVISITS", "ASPCAP_STAR_BAD",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_source_ids() -> list[str]:
    actual = sha256(SOURCE)
    if actual != EXPECTED_SHA256:
        raise RuntimeError(f"source SHA-256 mismatch: {actual}")
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        ids = [row["source_id"] for row in csv.DictReader(handle)]
    if len(ids) != EXPECTED_ROWS:
        raise RuntimeError(f"expected {EXPECTED_ROWS} source rows, found {len(ids)}")
    if len(set(ids)) != len(ids) or any(not value.isdigit() for value in ids):
        raise RuntimeError("source_id values are not unique exact integer strings")
    return ids


def target_votable(ids: Iterable[str]) -> bytes:
    head = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<VOTABLE version='1.3' xmlns='http://www.ivoa.net/xml/VOTable/v1.3'>"
        "<RESOURCE><TABLE name='targets'>"
        "<FIELD name='source_id' datatype='long'/><DATA><TABLEDATA>"
    )
    rows = "".join(f"<TR><TD>{source_id}</TD></TR>" for source_id in ids)
    tail = "</TABLEDATA></DATA></TABLE></RESOURCE></VOTABLE>"
    return (head + rows + tail).encode("utf-8")


def galah_query() -> str:
    selected = [
        "g.sobject_id AS sobject_id",
        "g.gaiadr3_source_id AS gaiadr3_source_id",
        "g.snr_px_ccd3 AS snr",
        "g.snr_px_ccd1 AS snr_px_ccd1",
        "g.snr_px_ccd2 AS snr_px_ccd2",
        "g.snr_px_ccd3 AS snr_px_ccd3",
        "g.snr_px_ccd4 AS snr_px_ccd4",
        "g.teff AS teff", "g.logg AS logg", "g.fe_h AS fe_h",
        "g.e_fe_h AS e_fe_h", "g.flag_sp AS flag_sp",
        "g.flag_fe_h AS flag_fe_h",
    ]
    for element in GALAH_ELEMENTS:
        selected.extend(
            [
                f"g.{element}_fe AS {element}_fe",
                f"g.e_{element}_fe AS e_{element}_fe",
                f"g.flag_{element}_fe AS flag_{element}_fe",
            ]
        )
    return (
        "SELECT " + ",".join(selected)
        + " FROM TAP_UPLOAD.targets AS t"
        + " JOIN galah_dr4.mainstartable AS g"
        + " ON g.gaiadr3_source_id=t.source_id"
    )


def parse_csv_response(text: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    if not lines:
        raise RuntimeError("service response contained no CSV header")
    reader = csv.DictReader(io.StringIO("\n".join(lines)))
    rows = list(reader)
    if not reader.fieldnames:
        raise RuntimeError("service response contained no field names")
    return list(reader.fieldnames), rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def retrieve_galah(ids: list[str]) -> None:
    query = galah_query()
    payload = {
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "csv",
        "QUERY": query,
        "UPLOAD": "targets,param:targets",
    }
    print(f"GALAH: uploading {len(ids)} exact IDs ({len(target_votable(ids))} bytes)")
    response = requests.post(
        GALAH_ENDPOINT,
        data=payload,
        files={"targets": ("targets.xml", target_votable(ids), "application/x-votable+xml")},
        timeout=(60, 3600),
    )
    response.raise_for_status()
    if "QUERY_STATUS\" value=\"ERROR" in response.text:
        raise RuntimeError(response.text[:4000])
    _, rows = parse_csv_response(response.text)
    target_set = set(ids)
    for row in rows:
        source_id = row.get("gaiadr3_source_id", "")
        if source_id not in target_set or not source_id.isdigit():
            raise RuntimeError(f"unexpected GALAH source_id {source_id!r}")
        for name in GALAH_ALPHA_COLUMNS:
            row[name] = ""
    rows.sort(key=lambda row: (int(row["gaiadr3_source_id"]), int(row["sobject_id"])))
    write_csv(DATA / "galah_matches.csv", GALAH_OUTPUT_COLUMNS, rows)
    (DATA / "galah_query.adql").write_text(query + "\n", encoding="utf-8")
    print(f"GALAH: wrote {len(rows)} rows")


def apogee_query(ids: list[str]) -> str:
    return (
        "SELECT s.APOGEE_ID,s.GAIAEDR3_SOURCE_ID,s.SNR,"
        "a.TEFF,a.LOGG,a.FE_H,a.FE_H_ERR,a.ALPHA_M,a.ASPCAPFLAG,s.STARFLAG,"
        "s.VHELIO_AVG,s.VSCATTER,s.NVISITS,"
        "CASE WHEN (a.ASPCAPFLAG & dbo.fApogeeAspcapFlag('STAR_BAD')) = 0 "
        "THEN 0 ELSE 1 END AS ASPCAP_STAR_BAD "
        "FROM apogeeStar s JOIN aspcapStar a ON a.apstar_id=s.apstar_id "
        "WHERE s.GAIAEDR3_SOURCE_ID IN (" + ",".join(ids) + ")"
    )


def fetch_apogee_chunk(index: int, ids: list[str]) -> tuple[int, str, list[dict[str, str]]]:
    query = apogee_query(ids)
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            response = requests.get(
                APOGEE_ENDPOINT,
                params={"cmd": query, "format": "csv"},
                timeout=(30, 240),
            )
            if response.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {response.status_code}")
            response.raise_for_status()
            _, rows = parse_csv_response(response.text)
            return index, query, rows
        except (requests.RequestException, RuntimeError) as error:
            last_error = error
            if attempt == 4:
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"APOGEE chunk {index} failed after retries: {last_error}")


def retrieve_apogee(ids: list[str], batch_size: int = 150, workers: int = 4) -> None:
    chunks = [ids[start : start + batch_size] for start in range(0, len(ids), batch_size)]
    results: dict[int, tuple[str, list[dict[str, str]]]] = {}
    print(f"APOGEE: querying {len(chunks)} exact-ID chunks with {workers} workers")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(fetch_apogee_chunk, index, chunk): index
            for index, chunk in enumerate(chunks)
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            index, query, rows = future.result()
            results[index] = (query, rows)
            if completed % 50 == 0 or completed == len(chunks):
                print(f"APOGEE: completed {completed}/{len(chunks)} chunks", flush=True)

    rows: list[dict[str, str]] = []
    target_set = set(ids)
    manifest_lines = []
    for index in range(len(chunks)):
        query, chunk_rows = results[index]
        manifest_lines.append(f"-- chunk {index + 1:04d}/{len(chunks):04d}\n{query};\n")
        for row in chunk_rows:
            source_id = row.get("GAIAEDR3_SOURCE_ID", "")
            if source_id not in target_set or not source_id.isdigit():
                raise RuntimeError(f"unexpected APOGEE source_id {source_id!r}")
            rows.append(row)
    rows.sort(
        key=lambda row: (
            int(row["GAIAEDR3_SOURCE_ID"]),
            row["APOGEE_ID"],
            -float(row["SNR"]) if row["SNR"] else math.inf,
        )
    )
    write_csv(DATA / "apogee_matches.csv", APOGEE_OUTPUT_COLUMNS, rows)
    (DATA / "apogee_queries.sql").write_text("\n".join(manifest_lines), encoding="utf-8")
    print(f"APOGEE: wrote {len(rows)} rows")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("survey", choices=("galah", "apogee", "all"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=150)
    args = parser.parse_args()
    ids = read_source_ids()
    DATA.mkdir(parents=True, exist_ok=True)
    if args.survey in ("galah", "all"):
        retrieve_galah(ids)
    if args.survey in ("apogee", "all"):
        retrieve_apogee(ids, batch_size=args.batch_size, workers=args.workers)


if __name__ == "__main__":
    main()
