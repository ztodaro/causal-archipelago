"""Check that the files in this repository match what was timestamped.

Run from the repository root:  python verify/check.py

1. DR4 freeze: every file listed in notes/dr4-freeze/MANIFEST.sha256 must match its SHA-256, except the three
   method write-ups named in EDITED_FOR_PUBLICATION (see README), which are reported as changed.
2. Gravity-test snapshots: rebuild commits 7e75a61 (pre-unseal-v1) and 953e527 (pre-unseal-e2b) from the git
   objects in verify/snapshots/, confirm each commit id is the one written in precommit.txt or precommit-e2b.txt,
   then confirm each published file listed for that snapshot has the same git blob id inside that commit.

The OpenTimestamps proofs themselves (*.ots) are checked separately with the OpenTimestamps client:
    ots verify precommit.txt.ots
    ots verify precommit-e2b.txt.ots
    ots verify notes/dr4-freeze/MANIFEST.sha256.ots
Uses the Python standard library only.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Stamped in the DR4 manifest, then edited to remove process notes before publication (README, "Edits for
# publication"). They no longer match their stamped hashes. The scripts and results they describe still do.
EDITED_FOR_PUBLICATION = {
    "e1-chemical-genealogy/E1C-SPEC.md",
    "notes/E10B-SPEC.md",
    "notes/dr4-freeze/B2-B4-SPEC.md",
}


def git_id(kind, data):
    return hashlib.sha1(f"{kind} {len(data)}\0".encode() + data).hexdigest()


def tree_entries(data):
    entries, i = {}, 0
    while i < len(data):
        space = data.index(b" ", i)
        nul = data.index(b"\0", space)
        name = data[space + 1:nul].decode("utf-8")
        entries[name] = data[nul + 1:nul + 21].hex()
        i = nul + 21
    return entries


def check_dr4():
    manifest = ROOT / "notes" / "dr4-freeze" / "MANIFEST.sha256"
    good, edited, bad = 0, [], 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", line.strip())
        if not m:
            continue
        digest, path = m.groups()
        f = ROOT / path
        if f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() == digest:
            good += 1
        elif path in EDITED_FOR_PUBLICATION:
            edited.append(path)
        else:
            bad += 1
            print(f"  DR4 mismatch: {path}")
    print(f"DR4 freeze manifest: {good} files match, {bad} do not")
    if edited:
        print(f"  {len(edited)} method write-ups were edited for publication and no longer match their stamped hash:")
        for path in edited:
            print(f"    {path}")
    return bad == 0


def check_snapshot(name, stamp_file):
    d = ROOT / "verify" / "snapshots" / name
    info = json.loads((d / "files.json").read_text(encoding="utf-8"))
    objects = {}
    for f in d.iterdir():
        if f.suffix in (".commit", ".tree"):
            data = f.read_bytes()
            kind = f.suffix[1:]
            if git_id(kind, data) != f.stem:
                print(f"  {name}: object {f.name} does not hash to its name")
                return False
            objects[f.stem] = (kind, data)
    commit = info["commit"]
    stamped = (ROOT / stamp_file).read_text(encoding="utf-8").split()[0]
    if commit != stamped or commit not in objects:
        print(f"  {name}: commit {commit} is not the stamped id {stamped}")
        return False
    root_tree = re.search(rb"^tree ([0-9a-f]{40})", objects[commit][1], re.M).group(1).decode()
    good = bad = 0
    for path, blob in info["files"].items():
        node = root_tree
        for part in path.split("/")[:-1]:
            node = tree_entries(objects[node][1])[part]
        recorded = tree_entries(objects[node][1]).get(path.split("/")[-1])
        actual = git_id("blob", (ROOT / path).read_bytes()) if (ROOT / path).exists() else None
        if recorded == blob == actual:
            good += 1
        else:
            bad += 1
            print(f"  {name}: {path} differs from the stamped snapshot")
    print(f"{name} (commit {commit[:7]}, stamped in {stamp_file}): {good} files match, {bad} do not")
    return bad == 0


if __name__ == "__main__":
    results = [check_dr4(),
               check_snapshot("pre-unseal-v1", "precommit.txt"),
               check_snapshot("pre-unseal-e2b", "precommit-e2b.txt")]
    sys.exit(0 if all(results) else 1)
