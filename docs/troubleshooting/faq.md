# Frequently Asked Questions

## Does a diagnostic playbook change anything?

It can. Collection may create files and jobs, and cleanup can delete files or
debug packages. YAML is executable operational intent, not a read-only sandbox.
See [safety](../user-guide/safety.md).

## A run succeeded. Is the device healthy?

Not necessarily. Execution and assertion outcomes are separate. A collection-only
playbook can return `SUCCESS` with `Validation: N/A`.
Review [result interpretation](../user-guide/running.md).

## Where are results stored?

Under `~/.radkit/playbook_runs/` by default, or your configured `output_dir`.
Keep logs and archives private and outside this repository.

## Why can a collection take so long?

Archive size, device load, collection jobs, transfer bandwidth, and local archive
verification all contribute. Review command timeouts and collection transfer
timeouts, and do not assume retrying is safe while a previous job is still active.

## Why is a known playbook missing?

Point `playbook_dir` to the extracted `playbooks/` directory, check valid YAML
and unique names, and ensure the requested name exists in the
[public catalog](../catalog/index.md). Some legacy examples are not public assets.

## Can I browse the documentation offline?

The wheel does not bundle this site or expose an `rpb.docs()` launcher.
On a connected machine, clone the public documentation repository and build:

```bash
python3 -m pip install -r requirements-docs.txt
python3 -m mkdocs build --strict
```

Copy the generated `site/` directory to the offline machine and serve it locally:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8000/`. Serving over HTTP allows local search/navigation
assets to load. This is offline documentation, not a claim that RADKit itself
can connect to a remote service without network access.

## Is this a production release?

This is a beta version for pilot users. Features and behavior may change.
Review the playbook and target devices before execution.
