"""Checks of training/sft/download_model.py (the larger-reader model files) that need no network: file hashes, the
folder check and the Hugging Face cache snapshot check."""
import hashlib
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "download_model", Path(__file__).resolve().parents[1] / "training" / "sft" / "download_model.py")
dm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dm)


def manifest_for(files):
    """A manifest for {name: bytes}: the weights file by SHA-256 (as LFS files are), the others by git blob SHA-1."""
    out = {}
    for name, data in files.items():
        if name.endswith(".safetensors"):
            out[name] = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        else:
            out[name] = {"size": len(data),
                         "git_sha1": hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()}
    return {"repo": "org/model", "revision": "0" * 40, "name": "model", "files": out}


FILES = {"config.json": b'{"model_type": "toy"}\n', "model-00001-of-00001.safetensors": b"\x00\x01weights" * 50}


class DownloadModelTest(unittest.TestCase):
    def test_git_blob_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "hello.txt"
            p.write_bytes(b"hello\n")
            self.assertEqual(dm.file_hash(p, "git_sha1"), "ce013625030ba8dba906f756967f9e9ca394464a")
            self.assertEqual(dm.file_hash(p, "sha256"), hashlib.sha256(b"hello\n").hexdigest())

    def test_check_dir(self):
        manifest = manifest_for(FILES)
        with tempfile.TemporaryDirectory() as tmp:
            for name, data in FILES.items():
                (Path(tmp) / name).write_bytes(data)
            self.assertEqual(dm.check_dir(manifest, tmp), [])
            weights = Path(tmp) / "model-00001-of-00001.safetensors"
            data = bytearray(FILES[weights.name])
            data[0] ^= 1  # same size, other content
            weights.write_bytes(bytes(data))
            self.assertEqual(dm.check_dir(manifest, tmp), [weights.name])
            (Path(tmp) / "config.json").unlink()
            self.assertEqual(sorted(dm.check_dir(manifest, tmp)), sorted(FILES))

    def test_check_links(self):
        manifest = manifest_for(FILES)
        with tempfile.TemporaryDirectory() as tmp:
            blobs, snap = Path(tmp) / "blobs", Path(tmp) / "snapshots" / ("0" * 40)
            blobs.mkdir()
            snap.mkdir(parents=True)
            for name, data in FILES.items():
                blob = blobs / dm.expected(manifest["files"][name])[1]
                blob.write_bytes(data)
                try:
                    os.symlink(os.path.relpath(blob, snap), snap / name)
                except OSError:
                    self.skipTest("symbolic links are not available here")
            self.assertEqual(dm.check_links(manifest, snap), [])
            (snap / "config.json").unlink()
            (snap / "config.json").write_bytes(FILES["config.json"])  # a plain copy is not accepted
            self.assertEqual(dm.check_links(manifest, snap), ["config.json"])


if __name__ == "__main__":
    unittest.main()
