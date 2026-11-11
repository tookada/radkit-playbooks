"""Screen public-facing documentation and configuration before publication."""

import argparse
import ipaddress
from pathlib import Path
import re
from urllib.parse import urlsplit


PUBLIC_HOSTS = {
    "github.com", "tookada.github.io", "radkit.cisco.com",
    "developer.cisco.com", "www.cisco.com", "software.cisco.com",
    "example.com", "example.org", "example.net", "localhost", "127.0.0.1",
}
DOCUMENTATION_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24", "127.0.0.0/8")
)
PATTERNS = {
    "private key material": re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----"),
    "access token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b"),
    "literal credential": re.compile(
        r"""(?i)\b(?:password|passwd|secret|access_token)\s*[:=]\s*["'][A-Za-z0-9!@#$%^&*._-]{4,}["']"""
    ),
    "service-like identifier": re.compile(r"\b[a-z0-9]{4}(?:-[a-z0-9]{4}){2}\b"),
    "case/package/subscriber-like identifier": re.compile(r"\b[0-9]{9,16}\b"),
    "restricted classification marker": re.compile(
        r"(?i)^\s*(?:[#*>]+\s*)?(?:Cisco\s+)?(?:Confidential|Internal Use Only|Proprietary\s*(?:and|&)\s*Confidential)(?:\s*$|\s*[-:])"
    ),
}
URL = re.compile(r"""https?://[^\s<>()"']+""")
ADDRESS = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
CORPORATE_HOST = re.compile(r"\b(?:[A-Za-z0-9-]+\.)+(?:cisco\.com|internal|local)\b", re.I)


def inspect_text(text: str) -> list[tuple[int, str]]:
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        categories = {
            label for label, pattern in PATTERNS.items() if pattern.search(line)
        }
        for value in URL.findall(line):
            host = (urlsplit(value).hostname or "").lower().rstrip(".")
            if host not in PUBLIC_HOSTS and not host.endswith(".example"):
                categories.add("unreviewed URL host")
        for host in CORPORATE_HOST.findall(line):
            if host.lower() not in PUBLIC_HOSTS:
                categories.add("non-public hostname")
        for domain in EMAIL.findall(line):
            if domain.lower() not in {"example.com", "example.org", "example.net"}:
                categories.add("non-example email address")
        for value in ADDRESS.findall(line):
            try:
                address = ipaddress.ip_address(value)
            except ValueError:
                continue
            if not any(address in network for network in DOCUMENTATION_NETWORKS):
                categories.add("non-documentation IP address")
        findings.extend((number, category) for category in sorted(categories))
    return findings


def check_public_content(root: Path) -> list[str]:
    root = root.resolve()
    findings = []
    for name in ("src", "docs/dev", "docs/user", "radkit_playbook"):
        if (root / name).exists():
            findings.append(f"{name}: non-public source or legacy documentation directory")
    candidates = [
        root / name for name in ("README.md", "CONTRIBUTING.md", "mkdocs.yml")
        if (root / name).is_file()
    ]
    candidates.extend(root.glob("requirements*.txt"))
    candidates.extend(path for path in (root / ".github/workflows").glob("*") if path.is_file())
    if (root / "docs").exists():
        for path in sorted((root / "docs").rglob("*")):
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                findings.append(f"{path.relative_to(root)}: documentation must not link outside this repository")
            elif path.is_file():
                if path.suffix != ".md":
                    findings.append(f"{path.relative_to(root)}: unexpected documentation file type")
                else:
                    candidates.append(path)
    for path in sorted(set(candidates)):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            findings.append(f"{path.relative_to(root)}: source must remain inside this repository")
            continue
        for number, category in inspect_text(path.read_text(encoding="utf-8")):
            findings.append(f"{path.relative_to(root)}:{number}: {category}")
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    findings = check_public_content(args.root)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}")
        raise SystemExit(1)
    print("Public-content checks passed. Manual confidentiality review is still required.")


if __name__ == "__main__":
    main()
