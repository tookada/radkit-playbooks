"""Build a YAML-only customer archive and its SHA-256 checksum."""

import argparse
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from scripts.validate_playbooks import validate_file


def build_archive(collection: Path, output: Path) -> Path:
    files = sorted(
        path for path in collection.rglob("*")
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml"}
    )
    if not files:
        raise ValueError(f"no YAML playbooks found in {collection}")
    names = set()
    for path in files:
        if path.is_symlink():
            raise ValueError(f"symlinked playbooks are not allowed: {path}")
        name = validate_file(path)
        if name in names:
            raise ValueError(f"duplicate playbook name: {name}")
        names.add(name)
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, Path("playbooks") / path.relative_to(collection))
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    checksum = output.parent / "SHA256SUMS"
    checksum.write_text(f"{digest}  {output.name}\n", encoding="ascii")
    return checksum


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", type=Path, default=root / "playbooks")
    parser.add_argument(
        "--output", type=Path, default=root / "dist" / "radkit-playbooks.zip"
    )
    args = parser.parse_args()
    checksum = build_archive(args.collection, args.output)
    print(f"Created {args.output}")
    print(f"Created {checksum}")


if __name__ == "__main__":
    main()
