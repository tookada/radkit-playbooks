# Running Playbooks and Interpreting Results

Only run reviewed playbooks against authorized targets after checking
[operational safety](safety.md) and [previewing](previewing.md).

```python
result = pb.run("smf_status_validation", target_node="smf-01")
print(result)
```

For multi-device command routing, provide the variables declared by the YAML:

```python
result = pb.run(
    "smf_nexus_status_validation",
    variables={
        "smf_node": ["smf-01"],
        "leaf_switches": ["leaf-01", "leaf-02"],
    },
)
print(result)
```

Example names are fictional. Required values may prompt when running
interactively; pass them explicitly for unattended execution.

## Execution and Validation Are Different

- `status`: execution outcome, including `SUCCESS`, `PARTIAL_SUCCESS`, `FAILURE`,
  or `SKIPPED`.
- `validation_status`: assertion outcome, such as `OK`, `FAIL`, or `N/A`.
- `run_directory`: local output directory.
- `command_results`: step status, errors, captures, validations, and artifacts
  for a single-target result.
- Batch results also expose per-target `node_results`.

A successful command can have failed health validations. Collection-only
playbooks can return `SUCCESS` with `validation_status: N/A`; this is not a device
health verdict. Inspect all step and artifact errors, not only the top-level
status.

`continue_on_error` controls execution failures and can be overridden by YAML.
Validation failures do not become execution failures by default;
`fail_on_validation: true` opts a step into that behavior. A run with intentional
skipped steps may be `PARTIAL_SUCCESS`; never silently treat that as full success.

## Local Outputs

Runs default to `~/.radkit/playbook_runs/`. Per-run directories contain logs,
`run.json`, and downloaded artifacts under target/step-specific `files/`
directories. Set a different base directory when binding:

```python
from pathlib import Path
pb = rpb.bind(
    service,
    playbook_dir=Path("~/radkit-playbooks/playbooks").expanduser(),
    output_dir=Path("~/radkit-results").expanduser(),
)
```

Keep outputs outside the public repository. They can contain configurations,
addresses, subscriber information, and other sensitive operational data.
See [file capture](../authoring/file-capture.md) for verification and cleanup.
