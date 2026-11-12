# RADKit Playbook

RADKit Playbook runs declarative YAML workflows through an already connected
Cisco RADKit service. Use it to inspect device state, evaluate captured values,
and collect diagnostic files.

## Downloads

- [Program wheels: v0.1.0 pilot beta](https://github.com/tookada/radkit-playbook-releases/releases/tag/v0.1.0)
- [YAML collection: v0.1.0](https://github.com/tookada/radkit-playbooks/releases/tag/v0.1.0)

See the [installation guide](getting-started/installation.md) for available
binaries and setup instructions. Program and collection versions are independent.

## Start Here

- [Overview and operational boundaries](getting-started/overview.md)
- [Installation and compatibility](getting-started/installation.md)
- [Quickstart with an existing service](getting-started/quickstart.md)
- [Public playbook catalog](catalog/index.md)
- [YAML authoring reference](PLAYBOOK_YAML_GUIDE.md)
- [Operational safety and data handling](user-guide/safety.md)

## Basic API

After obtaining an authorized connected `service` through RADKit:

```python
from pathlib import Path
import radkit_playbook as rpb

pb = rpb.bind(
    service,
    playbook_dir=Path("~/radkit-playbooks/playbooks").expanduser(),
)
print(pb.list())
print(pb.show("star_os_tech_support"))
print(pb.preview("star_os_tech_support", target_node="upf-01"))
```

`upf-01` is a fictional inventory name. Replace example values with your
authorized inventory and review the YAML before running commands.

## Beta Notice

This is a beta version for pilot users. Features and behavior may change.

Preview is not a device health check or proof that commands are safe for your
environment. Collection may create and delete files and consume device resources.
TAC uploads are optional and transfer selected local files outside your machine.
