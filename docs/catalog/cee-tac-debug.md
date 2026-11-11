# CEE TAC Debug Packages

The CEE workflows coordinate a CEE Ops-Center inventory device and a Linux
Kubernetes control-plane host.

- `cee_tac_debug_create`: create, poll, merge, retrieve, and clean up a new package.
- `cee_tac_debug_fetch`: retrieve an existing package, reusing a valid merged
  archive when present rather than merging it unnecessarily.

## Variables

| Variable | Applies to | Meaning |
|---|---|---|
| `cee_node` | Both | Required CEE inventory name |
| `time_window` | Create | Required collection window, such as `last 15m` |
| `tac_id` | Fetch | Required existing debug-package ID, not a TAC case number |
| `k8s_node` | Both | Optional inventory override; otherwise discovered from CEE |

Use authorized inventory entries with CLI, Kubernetes/container permissions, and
SFTP access. A discovered host address must resolve to a suitable inventory
entry. Explicit override names make routing easier to inspect.

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

For fetch, inspect a package reported by your own CEE:

```python
print(pb.preview(
    "cee_tac_debug_fetch",
    variables={
        "cee_node": "cee-01",
        "k8s_node": "k8s-01",
        "tac_id": "<DEBUG_PACKAGE_ID>",
    },
))
```

Replace placeholders before execution; do not insert real IDs into public files.

## Impact and Results

These are not read-only workflows: they create/merge packages, stage files on the
Kubernetes host, and delete staged archives and the selected CEE package after
the relevant successful retrieval. Review both file-capture cleanup and the
separate final package-deletion step. Disabling only `cleanup` on a capture is
not enough to disable all deletion.

When an existing valid archive is reused, the conditional merge step is skipped;
the aggregate result can be `PARTIAL_SUCCESS`. Inspect the individual conditions,
steps, and artifacts rather than silently accepting or rejecting that status.
Empty/corrupt archives and failed transfers require investigation.

The native-wheel StarOS pilots did not establish CEE live compatibility.
