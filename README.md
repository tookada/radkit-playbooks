# RADKit Playbooks

Public YAML playbook collection for RADKit Playbook, providing reusable workflows
for Cisco network diagnostics, validation, and technical support data collection.

This repository contains playbooks and collection validation tools, not the
RADKit Playbook program source code or RADKit credentials.

## Collection

| Platform | Playbook | Purpose |
|---|---|---|
| ACI | [aci_on_demand_techsupport](playbooks/aci/aci_on_demand_techsupport.yaml) | Collect switch On-Demand TechSupport through APIC |
| CEE | [cee_tac_debug_create](playbooks/cee/cee_tac_debug_create.yaml) | Create, retrieve, and clean up a TAC debug package |
| CEE | [cee_tac_debug_fetch](playbooks/cee/cee_tac_debug_fetch.yaml) | Retrieve an existing TAC debug package and clean up |
| StarOS | [star_os_tech_support](playbooks/staros/star_os_tech_support.yaml) | Collect System Status Diagnostics and clean up the remote archive |
| SMF / Nexus | [smf_nexus_status_validation](playbooks/smf/smf_nexus_status_validation.yaml) | Validate SMF and adjacent Nexus switch status |
| SMF | [smf_status_validation](playbooks/smf/smf_status_validation.yaml) | Validate SMF status |
| IOS XR | [ios_xr_deepscan_diagnostics](playbooks/xr/ios_xr_deepscan_diagnostics.yaml) | Run DeepScan diagnostics and collect support archives |

## Requirements

- An authorized RADKit client session with access to the intended devices.
- A compatible RADKit Playbook package installed in the Python environment used
  by the RADKit client.
- Device software, permissions, storage, and file-transfer support appropriate
  to the selected playbook. CEE collection also requires access to the relevant
  Kubernetes host.

The program package is distributed separately. This initial collection does not
yet claim a tested compatibility matrix with a publicly released wheel.

## Usage

Clone this repository or download its ZIP archive:

```bash
git clone https://github.com/tookada/radkit-playbooks.git
```

In the RADKit client Python session, use the existing connected `service` object:

```python
from pathlib import Path
import radkit_playbook as rpb

pb = rpb.bind(
    service,
    playbook_dir=Path("~/radkit-playbooks/playbooks").expanduser(),
)
pb.list()
pb.show("smf_status_validation")
pb.preview("smf_status_validation", target_node="smf-01")
# Execute only after reviewing the preview and confirming authorization.
pb.run("smf_status_validation", target_node="smf-01")
```

Adjust the path to your checkout. Point to **`playbooks/`**, not the repository
root, so workflow configuration YAML is not discovered as a playbook.
`smf-01` and other example names are placeholders for your RADKit inventory.
Inspect each playbook's variables and commands before execution.

## Operational Precautions

- Diagnostic collections can be long-running and consume CPU, storage, and
  transfer bandwidth. IOS XR DeepScan invokes many support collections; do not
  run it indiscriminately on production devices.
- CEE and StarOS workflows include remote cleanup commands. The CEE workflows
  delete the selected debug package after successful retrieval. Review these
  actions and preserve any required evidence before execution.
- Supply only trusted, reviewed variable values; some are interpolated into
  device CLI or shell commands. Confirm inventory targets and requested IDs.
- Outputs and downloaded archives may contain sensitive operational information.
  Keep them outside this public repository.
- Validate behavior against your device/software version in a controlled lab.
  Static CI checks are not proof of device compatibility or live execution.

## Validation and Contributions

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/validate_playbooks.py
python3 -m unittest discover -s tests -v
```

GitHub Actions runs these checks on pushes and pull requests using public hosted
runners without device access or credentials. Checks cover YAML parsing,
duplicate keys, basic required fields, unique identifiers, and capture regex
syntax. They are not a complete RADKit Playbook schema or runtime test.

For changes, open a pull request describing the purpose, variables, expected
results, device/software versions, and whether lab validation was performed.
Never push customer names, identifiable device names, real IP addresses,
credentials, internal URLs, diagnostic outputs, or archives. Use generic example
values. Public branches and pull requests are visible before review.

## License

No reuse license has been selected yet. Public visibility alone does not grant
permission to reuse, modify, or redistribute these files. License terms will be
added separately once confirmed by the rights holder.
