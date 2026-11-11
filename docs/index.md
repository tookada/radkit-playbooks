# RADKit Playbook

RADKit Playbook runs declarative YAML workflows through an already connected
Cisco RADKit service. Use it to inspect device state, evaluate captured values,
and collect diagnostic files.

## Publication Status

The [YAML collection](https://github.com/tookada/radkit-playbooks) is public.
The [program's binary distribution repository](https://github.com/tookada/radkit-playbook-releases)
is being prepared; **no public program wheel has been released yet**.
See [installation and compatibility](getting-started/installation.md) for the
current scope and remaining installation limitations.

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

## Scope and Licensing

Preview is not a device health check or proof that commands are safe for your
environment. Collection may create and delete files and consume device resources.
TAC uploads are optional and transfer selected local files outside your machine.

License terms are pending. Public visibility alone does not grant permission to
reuse, modify, or redistribute these materials. Do not treat this project's
documentation as a support or compatibility commitment beyond its stated tests.
