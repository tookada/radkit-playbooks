import re
import tempfile
import unittest
from pathlib import Path

from scripts.validate_playbooks import validate_file


VALID = """\
name: sample
description: Generic test playbook
commands:
  - id: version
    command: show version
"""


class ValidationTests(unittest.TestCase):
    def validate(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.yaml"
            path.write_text(text, encoding="utf-8")
            return validate_file(path)

    def test_valid(self):
        self.assertEqual(self.validate(VALID), "sample")

    def test_duplicate_key(self):
        with self.assertRaisesRegex(ValueError, "duplicate mapping key"):
            self.validate(VALID + "description: duplicate\n")

    def test_missing_commands(self):
        with self.assertRaisesRegex(ValueError, "commands"):
            self.validate("name: sample\ndescription: Example\n")

    def test_duplicate_step(self):
        with self.assertRaisesRegex(ValueError, "duplicate command id"):
            self.validate(VALID + "  - id: version\n    command: show clock\n")

    def test_invalid_regex(self):
        with self.assertRaises(re.error):
            self.validate(
                VALID + "    capture:\n      value:\n        regex: '['\n"
            )

    def test_filename_mismatch(self):
        with self.assertRaisesRegex(ValueError, "filename"):
            self.validate(VALID.replace("name: sample", "name: different"))

    def test_unknown_dependency(self):
        with self.assertRaisesRegex(ValueError, "unknown requires_step"):
            self.validate(VALID + "    requires_step: missing\n")

    def test_dependency_must_be_string(self):
        with self.assertRaisesRegex(ValueError, "unknown requires_step"):
            self.validate(VALID + "    requires_step: [version]\n")

    def test_variable_must_be_mapping(self):
        with self.assertRaisesRegex(ValueError, "variable target"):
            self.validate(VALID + "variables:\n  target: invalid\n")


if __name__ == "__main__":
    unittest.main()
