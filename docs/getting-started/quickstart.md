# Quickstart with an Existing Service

This example assumes RADKit Playbook is installed in the Python environment used
by your authorized RADKit client and `service` is already connected.
For setup, see the [installation guide](installation.md).

Authentication and service connection follow the
[RADKit documentation](https://radkit.cisco.com/); no credentials or real service
IDs are included in this guide.

## Bind and Inspect

```python
from pathlib import Path
import radkit_playbook as rpb

pb = rpb.bind(
    service,
    playbook_dir=Path("~/radkit-playbooks/playbooks").expanduser(),
)
print(pb.list())
print(pb.show("star_os_tech_support"))
```

The [catalog](../catalog/index.md) describes the seven public playbooks.
Examples use fictional inventory names; replace them with authorized targets.

## Preview Without Running Device Commands

```python
print(pb.preview("star_os_tech_support", target_node="upf-01"))
```

Check the target type and every generated command. Preview is not an online
storage or connectivity check and cannot establish the safety or eventual
success of a collection. Missing required variables may prompt interactively;
provide them explicitly for unattended use.

## Execute Only After Approval

The StarOS YAML generates an SSD archive, downloads it, and enables deletion of
the remote archive after successful verification. Confirm permissions, available
storage, SFTP readiness, and whether deletion is intended before using it.

```python
result = pb.run("star_os_tech_support", target_node="upf-01")
print(result)
```

To retain the remote archive, edit a trusted local YAML copy and set the
collection step's `cleanup: false` before previewing and running it.
Do not assume disabling file-capture cleanup disables separate explicit cleanup
commands in other playbooks.

Inspect `result.status`, `result.validation_status`, step errors, and artifacts.
The StarOS collection has no device-health assertions, so `Validation: N/A`
is expected; it does not mean the device is healthy.
