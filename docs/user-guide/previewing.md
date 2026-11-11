# Previewing Execution

`pb.preview()` evaluates inventory matching and command routing without executing
the playbook's device commands. It may prompt for missing required variables in
an interactive terminal.

```python
print(pb.preview("star_os_tech_support", target_node="upf-01"))
print(pb.preview("smf_status_validation", targets=["smf-01", "smf-02"]))
```

Use only one target selector: `target_node`, `targets`, or `target_pattern`.
For example:

```python
print(pb.preview("smf_status_validation", target_pattern=r"^smf-\d+$"))
```

All names and patterns are fictional examples. Check the selected inventory
entries and device types carefully; a broad pattern can select more devices than
intended.

## Command-Level Targets

CEE collection routes commands between a CEE device and a Kubernetes host:

```python
print(pb.preview(
    "cee_tac_debug_create",
    variables={
        "cee_node": "cee-01",
        "k8s_node": "k8s-01",
        "time_window": "last 15m",
    },
))
```

Supplying an explicit host makes the intended inventory routing easier to
review. Targets and conditions depending on runtime captures cannot be fully
resolved before earlier commands run.

## What Preview Does Not Prove

Preview is not a live connectivity, SFTP, free-space, command-support, or device
health test. It does not execute polling or predict all capture values and
conditional branches. Review the YAML itself, especially cleanup commands.
The public StarOS playbook has two steps; no automatic free-space precheck is
included in that YAML. Operators must check storage before starting collection.
