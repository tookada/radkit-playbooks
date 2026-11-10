# Maintainer and Contributor Guide

Customers only need the YAML-only release ZIP and a compatible RADKit Playbook
installation. Scripts, tests, and CI configuration in this repository support
maintenance; they are not included in that ZIP.

## Development and Validation

```bash
git clone https://github.com/tookada/radkit-playbooks.git
cd radkit-playbooks
python3 -m pip install -r requirements-validation.txt
python3 scripts/validate_playbooks.py
python3 -m unittest discover -s tests -v
```

GitHub Actions runs these checks on pushes and pull requests using public hosted
runners without device access or credentials. Static checks cover YAML parsing,
duplicate keys, basic required fields, unique identifiers, and capture regex
syntax. They are not a complete RADKit Playbook schema or runtime test.

Open a pull request describing the purpose, variables, expected results,
device/software versions, and whether lab validation was performed.
Never push customer names, identifiable device names, real IP addresses,
credentials, internal URLs, diagnostic outputs, or archives. Use generic example
values. Public branches and pull requests are visible before review.

## Build the Customer Download

```bash
python3 -m scripts.build_release
```

This validates the collection and creates:

- `dist/radkit-playbooks.zip`: YAML files only, under `playbooks/`.
- `dist/SHA256SUMS`: SHA-256 checksum for that ZIP.

Archive tests verify the directory structure, YAML-only contents, and checksum.
Generated files are ignored by Git.

## Publish a Collection Release

After review, checks, and any required controlled lab validation:

1. Select the reviewed commit on `main` and confirm all checks pass.
2. Create and push a new version tag, for example:

   ```bash
   git tag -a v0.1.0 -m "Initial YAML playbook collection"
   git push origin v0.1.0
   ```

3. The **Release YAML collection** workflow validates the collection, runs tests,
   builds the YAML-only ZIP, and creates a **draft** GitHub Release with the ZIP
   and checksum attached.
4. Inspect the draft and document compatibility and actual lab validation.
   Resolve license terms with the rights holder before inviting customer reuse.
5. Publish the release from GitHub after approval. Verify the download and
   checksum; the README's latest-release link will then resolve to it.

The workflow uses a GitHub-provided token scoped to this repository. It does not
access internal source, device credentials, or internal runners. It runs only
for version tags, not pull requests.

Do not silently replace published release assets. Use a new version for updates.
GitHub also provides automatic source archives; those include maintenance files
and are not the customer download.
