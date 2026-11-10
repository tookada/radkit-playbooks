"""Static checks for the public YAML collection; no device commands are run."""

import argparse
import re
import sys
from pathlib import Path

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ValueError("mapping keys must be strings")
            if key in seen:
                raise ValueError(f"duplicate mapping key: {key}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def check_regexes(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "regex":
                if not isinstance(child, str):
                    raise ValueError("regex must be a string")
                re.compile(child)
            else:
                check_regexes(child)
    elif isinstance(value, list):
        for child in value:
            check_regexes(child)


def validate_file(path):
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError("playbook must be a mapping")
    for field in ("name", "description"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    if data["name"] != path.stem:
        raise ValueError("name must match the YAML filename")
    variables = data.get("variables", {})
    if not isinstance(variables, dict):
        raise ValueError("variables must be a mapping")
    for name, definition in variables.items():
        if not isinstance(definition, dict):
            raise ValueError(f"variable {name} must be a mapping")
    commands = data.get("commands")
    if not isinstance(commands, list) or not commands:
        raise ValueError("commands must be a non-empty list")
    step_ids = set()
    for command in commands:
        if not isinstance(command, dict):
            raise ValueError("each command must be a mapping")
        for field in ("id", "command"):
            if not isinstance(command.get(field), str) or not command[field].strip():
                raise ValueError(f"command {field} must be a non-empty string")
        if command["id"] in step_ids:
            raise ValueError(f"duplicate command id: {command['id']}")
        step_ids.add(command["id"])
    for command in commands:
        dependency = command.get("requires_step")
        if dependency is not None:
            if not isinstance(dependency, str) or dependency not in step_ids:
                raise ValueError(f"unknown requires_step: {dependency}")
    check_regexes(data)
    return data["name"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "playbooks",
    )
    args = parser.parse_args()
    files = sorted(
        path for path in args.directory.rglob("*")
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml"}
    )
    if not files:
        print(f"ERROR: no YAML playbooks found in {args.directory}", file=sys.stderr)
        return 1
    names = set()
    failed = False
    for path in files:
        try:
            name = validate_file(path)
            if name in names:
                raise ValueError(f"duplicate playbook name: {name}")
            names.add(name)
        except (ValueError, yaml.YAMLError, re.error, OSError) as exc:
            print(f"ERROR: {path}: {exc}", file=sys.stderr)
            failed = True
        else:
            print(f"OK: {path.relative_to(args.directory)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
