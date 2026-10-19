"""Frozen-position ESO metadata census. Never requests a spectrum/download URL."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import requests


ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://archive.eso.org/tap_obs/sync"
MAXREC = 1_000_000
NS = {"v": "http://www.ivoa.net/xml/VOTable/v1.3"}
PROTOCOL = ROOT / "solar-siblings/E8-FOLLOWUP-PROTOCOL.md"
TARGETS = ROOT / "solar-siblings/e8_followup_targets.csv"
PROTOCOL_SHA = "98582f94e626281bd27cee237d4a8163ea1ec07b4f4f185ba384e161fea39841"
TARGETS_SHA = "46a04ded16b4ab98999a30d8976a3a8358fa2f04bfe470e3766a7e95cf2fe827"
PRODUCT_COLUMNS = (
    "dp_id,obs_id,obs_publisher_did,instrument_name,dataproduct_type,"
    "calib_level,p3orig,obs_collection,target_name,s_ra,s_dec,"
    "em_res_power,em_min,em_max,t_exptime,snr,t_min,t_max,"
    "proposal_id,obs_release_date,obstech"
)
RAW_COLUMNS = (
    "dp_id,instrument,ra,dec,dp_tech,dp_type,dp_cat,date_obs,mjd_obs,"
    "exposure,release_date,prog_id,object,target,ins_mode,slit_path,"
    "grat_path,lambda_min,lambda_max"
)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs():
    commit = subprocess.check_output(
        ["git", "log", "-1", "--format=%H", "--", str(PROTOCOL.relative_to(ROOT))],
        cwd=ROOT, text=True,
    ).strip()
    if not commit.startswith("96d4fa3"):
        raise RuntimeError(f"Frozen protocol commit mismatch: {commit}")
    for path, expected in [(PROTOCOL, PROTOCOL_SHA), (TARGETS, TARGETS_SHA)]:
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"Frozen input SHA-256 mismatch: {path}: {actual}")
    with TARGETS.open(newline="", encoding="utf-8") as f:
        targets = list(csv.DictReader(f))
    assert len(targets) == 20
    assert [int(t["rank"]) for t in targets] == list(range(1, 21))
    assert targets[18]["source_id"] == ""
    for t in targets:
        assert t["source_id"] == "" or t["source_id"].isdigit()
        assert t["survey_id"].isdigit()
    return commit, targets


def tap_query(label, query, rank=None):
    started = utc_now()
    response = requests.post(
        ENDPOINT,
        data={"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "votable",
              "MAXREC": str(MAXREC), "QUERY": query},
        timeout=(20, 90),
    )
    if not response.ok:
        raise RuntimeError(f"{label}: HTTP {response.status_code}: {response.text[:2000]}")
    root = ET.fromstring(response.content)
    statuses = [info.attrib.get("value") for info in root.findall(".//v:INFO", NS)
                if info.attrib.get("name") == "QUERY_STATUS"]
    if not statuses or any(s != "OK" for s in statuses):
        raise RuntimeError(f"{label}: query failed/overflowed: {response.text[-2000:]}")
    table = root.find(".//v:TABLE", NS)
    if table is None:
        raise RuntimeError(f"{label}: missing result table")
    fields = [f.attrib["name"] for f in table.findall("v:FIELD", NS)]
    td = table.find("v:DATA/v:TABLEDATA", NS)
    if td is None:
        raise RuntimeError(f"{label}: expected TABLEDATA serialization")
    rows = []
    for tr in td.findall("v:TR", NS):
        cells = [(cell.text or "").strip() for cell in tr.findall("v:TD", NS)]
        if len(cells) != len(fields):
            raise RuntimeError(f"{label}: malformed row")
        rows.append(dict(zip(fields, cells)))
    if len(rows) >= MAXREC:
        raise RuntimeError(f"{label}: row limit reached")
    print(f"{label}: {len(rows)} metadata rows; QUERY_STATUS={statuses}", flush=True)
    return {"label": label, "rank": rank, "query": query, "started_utc": started,
            "completed_utc": utc_now(), "http_status": response.status_code,
            "query_status": statuses, "response_sha256": hashlib.sha256(response.content).hexdigest(),
            "fields": fields, "rows": rows}


def collect():
    commit, targets = verify_inputs()
    snapshot = {"endpoint": ENDPOINT, "maxrec": MAXREC,
                "protocol_commit": commit, "protocol_sha256": PROTOCOL_SHA,
                "targets_sha256": TARGETS_SHA, "started_utc": utc_now(),
                "targets": [{k: t[k] for k in ("rank", "source_id", "survey_id", "ra", "dec")}
                            for t in targets], "results": []}
    queries = []
    for target in targets:
        rank = target["rank"]
        cone = f"CONTAINS(s_region,CIRCLE('ICRS',{target['ra']},{target['dec']},2.0/3600.0))=1"
        # The raw table has no dataproduct_type or resolving-power column.
        # Retrieve in-scope positional metadata first; never assume a UVES
        # setting passes the resolving-power threshold from its name alone.
        queries.append((f"candidate-{int(rank):02d}-obscore",
                        f"SELECT {PRODUCT_COLUMNS}\nFROM ivoa.ObsCore\n"
                        "WHERE instrument_name IN ('HARPS','ESPRESSO','FEROS','UVES')\n"
                        "AND dataproduct_type='spectrum'\n"
                        "AND (instrument_name<>'UVES' OR em_res_power>=40000)\n"
                        f"AND {cone}\nORDER BY t_min,dp_id", rank))
        queries.append((f"candidate-{int(rank):02d}-raw",
                        f"SELECT {RAW_COLUMNS}\nFROM dbo.raw\n"
                        "WHERE instrument IN ('HARPS','ESPRESSO','FEROS','UVES')\n"
                        f"AND {cone}\nORDER BY mjd_obs,dp_id", rank))
    for instrument in ("HARPS", "ESPRESSO"):
        names = ",".join(f"'{name}'" for base in ("Vesta", "Ceres", "Juno", "Moon", "Ganymede")
                         for name in (base, base.upper(), base.lower()))
        queries.append((f"solar-{instrument}",
                        f"SELECT TOP 5 {PRODUCT_COLUMNS}\nFROM ivoa.ObsCore\n"
                        f"WHERE instrument_name='{instrument}' AND dataproduct_type='spectrum'\n"
                        f"AND target_name IN ({names})\n"
                        "AND em_res_power>=40000\n"
                        f"AND obs_release_date<='{snapshot['started_utc']}'\n"
                        "ORDER BY t_min DESC,dp_id", None))
    tempdir = Path(tempfile.mkdtemp(prefix="e8_eso_census_"))
    snapshot_path = tempdir / "metadata_snapshot.json"
    print(f"Metadata-only audit snapshot: {snapshot_path}", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(tap_query, *query): query[0] for query in queries}
        for future in as_completed(futures):
            result = future.result()
            snapshot["results"].append(result)
            snapshot_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    snapshot["results"].sort(key=lambda r: r["label"])
    snapshot["completed_utc"] = utc_now()
    verify_inputs()
    snapshot_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(f"COLLECTION COMPLETE: {snapshot_path}", flush=True)
    for result in snapshot["results"]:
        if result["rows"]:
            print(json.dumps({"label": result["label"], "rows": result["rows"]}), flush=True)


def mjd_iso(value):
    """Display the published MJD as UTC; no spectral processing."""
    epoch = datetime(1858, 11, 17, tzinfo=timezone.utc)
    return (epoch + timedelta(days=float(value))).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def finalize(snapshot_path):
    commit, targets = verify_inputs()
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    assert snapshot["protocol_commit"] == commit
    assert snapshot["protocol_sha256"] == PROTOCOL_SHA
    assert snapshot["targets_sha256"] == TARGETS_SHA
    assert snapshot["endpoint"] == ENDPOINT and snapshot["maxrec"] == MAXREC
    assert snapshot.get("completed_utc")
    assert snapshot["targets"] == [{k: t[k] for k in ("rank", "source_id", "survey_id", "ra", "dec")}
                                   for t in targets]
    results = {r["label"]: r for r in snapshot["results"]}
    expected = {f"candidate-{rank:02d}-{kind}" for rank in range(1, 21)
                for kind in ("obscore", "raw")} | {"solar-HARPS", "solar-ESPRESSO"}
    assert set(results) == expected and len(snapshot["results"]) == len(expected)
    for result in results.values():
        assert result["http_status"] == 200
        assert result["query_status"] and all(s == "OK" for s in result["query_status"])
        assert len(result["rows"]) < MAXREC
    # Fail closed if a future rerun returns candidates. Raw type, UVES settings,
    # resolution and coverage would require a separate metadata-only review.
    if any(r["rows"] for r in results.values() if r["rank"] is not None):
        raise RuntimeError("Nonzero candidates require intake metadata review; no output written")
    for instrument in ("HARPS", "ESPRESSO"):
        rows = results[f"solar-{instrument}"]["rows"]
        assert len(rows) == 5 and len({r["dp_id"] for r in rows}) == 5
        for row in rows:
            assert row["instrument_name"] == instrument
            assert row["dataproduct_type"] == "spectrum"
            assert row["target_name"].lower() in {"vesta", "ceres", "juno", "moon", "ganymede"}
            assert float(row["em_res_power"]) >= 40000
            assert datetime.fromisoformat(row["obs_release_date"]) <= datetime.fromisoformat(snapshot["started_utc"])
    outdir = ROOT / "solar-siblings/data"
    census = outdir / "e8_archival_census.csv"
    provenance = outdir / "PROVENANCE-e8_archival_census.md"
    if census.exists() or provenance.exists():
        raise RuntimeError("Refusing to overwrite existing census/provenance")
    columns = ["rank", "source_id", "sobject_id", "archive", "instrument",
               "em_res_power", "em_min", "em_max", "t_exptime", "snr",
               "obs_date_utc", "obs_date_mjd", "proposal_id", "dataset_id",
               "product_origin", "calib_level", "obs_release_date", "access_status"]
    with census.open("x", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=columns, lineterminator="\n").writeheader()
    census_sha = sha256(census)
    text = f"""# E8 archival census — ESO spectra availability

Intake only. No science spectrum, FITS file, preview, spectral array, or line
measurement was downloaded or examined. The E8-CONFIRM gate remains closed.

## Frozen-input verification

- Latest protocol commit: `{commit}` (required prefix `96d4fa3`).
- Protocol SHA-256: `{PROTOCOL_SHA}`.
- Target-list SHA-256: `{TARGETS_SHA}`.
- All three mandatory checks passed before retrieval, after retrieval, and before
  finalization. Neither frozen file was modified.
- 20 targets. Target `survey_id` maps to `sobject_id` in the census schema.
  All identifiers remain decimal strings; rank 19's Gaia ID remains blank.

## Acquisition and scope

- Endpoint: `{ENDPOINT}` (HTTPS version of the requested ESO endpoint).
- Retrieval started UTC: `{snapshot['started_utc']}`.
- Retrieval completed UTC: `{snapshot['completed_utc']}`.
- Every query uses HTTP POST: `REQUEST=doQuery`, `LANG=ADQL`, `FORMAT=votable`,
  `MAXREC={MAXREC}`. VOTable TABLEDATA cells were parsed as strings.
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
"""
    for t in targets:
        text += f"| {t['rank']} | {t['source_id']} | {t['survey_id']} | 0 | 0 | 0 |\n"
    text += """
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
"""
    for instrument in ("HARPS", "ESPRESSO"):
        for r in results[f"solar-{instrument}"]["rows"]:
            text += (f"| {instrument} | {r['target_name']} | {r['dp_id']} | {mjd_iso(r['t_min'])} | "
                     f"{r['t_min']} | {r['em_res_power']} | {r['snr']} | {r['t_exptime']} | "
                     f"{r['proposal_id']} | {r['obs_release_date']} |\n")
    text += "\nPublished wavelength bounds (metres):\n\n| Dataset/product ID | em_min | em_max |\n|---|---|---|\n"
    for instrument in ("HARPS", "ESPRESSO"):
        for r in results[f"solar-{instrument}"]["rows"]:
            text += f"| {r['dp_id']} | {r['em_min']} | {r['em_max']} |\n"
    text += f"""
## Files and reproducibility

- `e8_archival_census.csv`: **0 data rows**, {len(columns)} columns, {census.stat().st_size} bytes.
- CSV SHA-256: `{census_sha}`.
- Script: `solar-siblings/retrieve_e8_census.py`, SHA-256 `{sha256(Path(__file__))}`.
- Collection: `python -u solar-siblings/retrieve_e8_census.py collect`.
- Finalization: `python -u solar-siblings/retrieve_e8_census.py finalize <metadata_snapshot.json>`.
  Collection prints the temporary metadata snapshot path. Finalization makes no
  network requests and refuses to overwrite existing deliverables. Future nonzero
  candidate results fail closed pending raw-setting/coverage metadata review.
- Preliminary schema, technique-label, and first-target syntax checks were
  metadata-only. The authoritative acquisition is the complete 42-query run below.

## Exact acquisition queries and response audit

"""
    for label in sorted(results):
        r = results[label]
        text += (f"### {label}\n\n"
                 f"- Start UTC: `{r['started_utc']}`; end UTC: `{r['completed_utc']}`.\n"
                 f"- Rows: `{len(r['rows'])}`; HTTP `{r['http_status']}`; QUERY_STATUS `OK`.\n"
                 f"- Response VOTable SHA-256: `{r['response_sha256']}`.\n\n"
                 f"```sql\n{r['query']}\n```\n\n")
    provenance.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    verify_inputs()
    print(json.dumps({"census_rows": 0, "census_sha256": census_sha,
                      "provenance_sha256": sha256(provenance),
                      "solar_examples": {i: len(results[f'solar-{i}']['rows'])
                                         for i in ('HARPS', 'ESPRESSO')}}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["collect", "finalize"])
    parser.add_argument("snapshot", nargs="?", type=Path)
    args = parser.parse_args()
    if args.command == "collect":
        collect()
    else:
        if args.snapshot is None:
            parser.error("finalize requires the collected metadata snapshot path")
        finalize(args.snapshot)
