from pathlib import Path
import re
import tempfile
import unittest

import yaml

from scripts.check_public_content import check_public_content, inspect_text


ROOT = Path(__file__).resolve().parents[1]


class PublicContentTests(unittest.TestCase):
    def test_selected_public_content_passes(self):
        self.assertEqual(check_public_content(ROOT), [])

    def test_rejects_non_public_values_without_echoing_them(self):
        samples = {
            "https://portal.example.internal/": "unreviewed URL host",
            "portal.example.internal": "non-public hostname",
            "192.168.10.20": "non-documentation IP address",
            "upload_to_cxd='123456789'": "case/package/subscriber-like identifier",
            "abc1-def2-ghi3": "service-like identifier",
            "# Confidential": "restricted classification marker",
            "password='not-a-real-password'": "literal credential",
            "person@customer.invalid": "non-example email address",
            "-----BEGIN PRIVATE KEY-----": "private key material",
        }
        for sample, category in samples.items():
            with self.subTest(category=category):
                self.assertIn((1, category), inspect_text(sample))

    def test_allows_documentation_addresses_and_public_links(self):
        self.assertEqual(inspect_text(
            "192.0.2.1 198.51.100.2 203.0.113.3 http://127.0.0.1:8000/\n"
            "https://radkit.cisco.com/ https://github.com/tookada/radkit-playbooks\n"
            "https://tookada.github.io/radkit-playbooks/ user@example.com"
        ), [])

    def test_rejects_private_source_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs/dev").mkdir(parents=True)
            self.assertTrue(check_public_content(root))

    def test_rejects_documentation_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "README.md").write_text("# Public\n")
            (root / "docs/linked.md").symlink_to(root / "README.md")
            self.assertTrue(check_public_content(root))


class DocumentationTests(unittest.TestCase):
    def test_yaml_examples_are_valid_yaml(self):
        for path in (ROOT / "docs").rglob("*.md"):
            examples = re.findall(
                r"^```ya?ml[ \t]*\n(.*?)^```[ \t]*$",
                path.read_text(),
                re.MULTILINE | re.DOTALL,
            )
            for number, example in enumerate(examples, 1):
                with self.subTest(document=str(path.relative_to(ROOT)), example=number):
                    yaml.safe_load(example)

    def test_every_document_is_in_navigation(self):
        config = yaml.safe_load((ROOT / "mkdocs.yml").read_text())

        def pages(item):
            if isinstance(item, str):
                yield item
            elif isinstance(item, list):
                for child in item:
                    yield from pages(child)
            elif isinstance(item, dict):
                for child in item.values():
                    yield from pages(child)

        actual = {str(path.relative_to(ROOT / "docs")) for path in (ROOT / "docs").rglob("*.md")}
        self.assertEqual(set(pages(config["nav"])), actual)

    def test_catalog_links_to_exact_public_collection(self):
        catalog = (ROOT / "docs/catalog/index.md").read_text()
        playbooks = list((ROOT / "playbooks").rglob("*.yaml"))
        self.assertEqual(len(playbooks), 7)
        for path in playbooks:
            playbook = yaml.safe_load(path.read_text())
            expected = (
                f"[{playbook['name']}](https://github.com/tookada/radkit-playbooks/blob/main/"
                f"{path.relative_to(ROOT).as_posix()})"
            )
            self.assertIn(expected, catalog)


if __name__ == "__main__":
    unittest.main()
