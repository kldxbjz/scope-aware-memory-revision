"""Reader model files for the larger-reader check (bigreader.sbatch; post-hoc, docs/analysis.md), against a manifest
that pins the repository, the revision and every file's size and hash (bigreader_model.json).

  python -I download_model.py --manifest bigreader_model.json --dir LOCAL_DIR      # fetch, then check every file
  python -I download_model.py --manifest bigreader_model.json --check LOCAL_DIR    # check only
  python -I download_model.py --manifest bigreader_model.json --check-links SNAPSHOT_DIR

--dir downloads exactly the manifest's files at its revision with up to TRIES calls (a repeated call resumes
unfinished files), then compares size and hash of each file with the manifest: SHA-256 for LFS files, the git blob
SHA-1 for the others. --check-links accepts a Hugging Face cache snapshot (for example a shared cache) without reading
the weights: every file must exist with the manifest's size and link to the blob named by its hash, which is how the
cache stores files. Exit 0 = every file matches; nothing outside the given folder is written."""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

TRIES, WAIT = 8, 30
T0 = time.time()


def log(*a):
    print(time.strftime("%H:%M:%S"), round(time.time() - T0), *a, flush=True)


def file_hash(path, kind):
    """sha256 of the content, or git_sha1: SHA-1 of b"blob <size>\\0" + content (the git blob id)."""
    h = hashlib.sha256() if kind == "sha256" else hashlib.sha1(b"blob %d\0" % path.stat().st_size)
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


def expected(entry):
    return ("sha256", entry["sha256"]) if "sha256" in entry else ("git_sha1", entry["git_sha1"])


def check_dir(manifest, folder):
    """Names of the manifest files that are missing or differ in size or hash."""
    bad = []
    for name, entry in manifest["files"].items():
        p = Path(folder) / name
        kind, want = expected(entry)
        if not p.is_file() or p.stat().st_size != entry["size"] or file_hash(p, kind) != want:
            bad.append(name)
    return bad


def check_links(manifest, snapshot):
    """Names of the manifest files that a cache snapshot lacks, or holds with another size or blob."""
    bad = []
    for name, entry in manifest["files"].items():
        p = Path(snapshot) / name
        _, want = expected(entry)
        if not p.is_file() or p.stat().st_size != entry["size"] or not p.is_symlink() \
                or os.path.basename(os.readlink(p)) != want:
            bad.append(name)
    return bad


def download(manifest, folder):
    from huggingface_hub import snapshot_download
    Path(folder).mkdir(parents=True, exist_ok=True)
    for attempt in range(1, TRIES + 1):
        try:
            snapshot_download(manifest["repo"], revision=manifest["revision"], local_dir=str(folder), token=False,
                              max_workers=8, allow_patterns=sorted(manifest["files"]))
            log("download call finished, attempt", attempt)
            return
        except Exception as exc:  # a broken connection: the next call resumes the unfinished files
            log("attempt", attempt, "failed:", type(exc).__name__, str(exc)[:200])
            if attempt == TRIES:
                sys.exit(f"download failed after {TRIES} attempts")
            time.sleep(WAIT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--dir", help="download into this folder, then check it")
    group.add_argument("--check", help="check this folder only")
    group.add_argument("--check-links", help="check a Hugging Face cache snapshot by sizes and blob names")
    a = ap.parse_args()
    manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    total = sum(e["size"] for e in manifest["files"].values()) / 1e9
    if a.check_links:
        bad = check_links(manifest, a.check_links)
        log(f"{a.check_links}: {len(manifest['files'])} files, mismatches: {bad or 'none'}")
    else:
        folder = a.dir or a.check
        if a.dir:
            log(f"fetching {manifest['repo']}@{manifest['revision'][:8]} ({total:.2f} GB) into {folder}")
            download(manifest, folder)
        bad = check_dir(manifest, folder)
        log(f"checked {len(manifest['files'])} files ({total:.2f} GB) in {folder}, mismatches: {bad or 'none'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
