import hashlib
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.build_release import build_archive


PLAYBOOK = """\
name: sample
description: Generic test playbook
commands:
  - id: version
    command: show version
"""


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.collection = self.root / "playbooks"
        self.platform = self.collection / "platform"
        self.platform.mkdir(parents=True)
        self.source = self.platform / "sample.yaml"
        self.source.write_text(PLAYBOOK, encoding="utf-8")
        self.output = self.root / "dist" / "radkit-playbooks.zip"

    def test_archive_contains_only_yaml_under_playbooks(self):
        (self.platform / "README.md").write_text("Not a playbook", encoding="utf-8")
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "example.py").write_text("pass", encoding="ascii")
        build_archive(self.collection, self.output)
        with ZipFile(self.output) as archive:
            self.assertEqual(archive.namelist(), ["playbooks/platform/sample.yaml"])
            self.assertEqual(
                archive.read("playbooks/platform/sample.yaml").decode("utf-8"),
                PLAYBOOK,
            )
            self.assertIsNone(archive.testzip())

    def test_checksum(self):
        checksum = build_archive(self.collection, self.output)
        digest = hashlib.sha256(self.output.read_bytes()).hexdigest()
        self.assertEqual(
            checksum.read_text(encoding="ascii"),
            f"{digest}  radkit-playbooks.zip\n",
        )

    def test_yml_extension(self):
        self.source.rename(self.platform / "sample.yml")
        build_archive(self.collection, self.output)
        with ZipFile(self.output) as archive:
            self.assertEqual(archive.namelist(), ["playbooks/platform/sample.yml"])

    def test_empty_collection_fails(self):
        self.source.unlink()
        with self.assertRaisesRegex(ValueError, "no YAML"):
            build_archive(self.collection, self.output)
        self.assertFalse(self.output.exists())

    def test_invalid_playbook_fails(self):
        self.source.write_text("invalid", encoding="ascii")
        with self.assertRaisesRegex(ValueError, "mapping"):
            build_archive(self.collection, self.output)
        self.assertFalse(self.output.exists())

    def test_symlink_fails(self):
        alias = self.platform / "alias.yaml"
        alias.symlink_to(self.source)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            build_archive(self.collection, self.output)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
