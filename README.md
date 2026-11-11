# RADKit Playbooks

Public YAML playbook collection for RADKit Playbook, providing reusable workflows
for Cisco network diagnostics, validation, and technical support data collection.

Download the YAML-only collection to use these playbooks. You do not need Git,
the validation tools, or the tests. The RADKit Playbook program is provided
separately.

## Documentation and Program Downloads

- [User and authoring documentation source](docs/index.md)
- Planned GitHub Pages site: <https://tookada.github.io/radkit-playbooks/>
  (publication is being prepared).
- [Program wheel distribution](https://github.com/tookada/radkit-playbook-releases):
  public binary releases and customer installation instructions are still being
  prepared.

The documentation in this repository is the public source of truth for usage,
YAML authoring, compatibility, and the playbook catalog. See the
[installation status](docs/getting-started/installation.md) and
[operational safety guide](docs/user-guide/safety.md) before use.

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

## Download

From the [latest release](https://github.com/tookada/radkit-playbooks/releases/latest),
download **`radkit-playbooks.zip`** and optionally **`SHA256SUMS`** to check the
download. Choose the named ZIP asset, not GitHub's automatic "Source code"
archives, which contain the entire repository.

On macOS, with both downloaded files in the current directory:

```bash
shasum -a 256 -c SHA256SUMS
unzip radkit-playbooks.zip -d ~/radkit-playbooks
```

The ZIP contains only the YAML collection under `playbooks/`; it does not include
scripts, tests, or CI configuration. Extract new versions into a fresh directory
to avoid keeping playbooks removed in a later release.

Individual YAML files can also be downloaded from the collection links above.

## Usage

After installing a compatible program package, use the existing connected
`service` object in your RADKit client Python session:

```python
from pathlib import Path
import radkit_playbook as rpb

pb = rpb.bind(
    service,
    playbook_dir=Path("~/radkit-playbooks/playbooks").expanduser(),
)
pb.list()
print(pb.show("smf_status_validation"))
print(pb.preview("smf_status_validation", target_node="smf-01"))
```

For execution, results, collection, and upload procedures, see the
[Quickstart](docs/getting-started/quickstart.md) and
[user guide](docs/user-guide/running.md).

Adjust the path to your extracted collection. Point to **`playbooks/`**, not the repository
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

## Contributing

For authoring, validation, and release procedures, see the
[maintainer guide](CONTRIBUTING.md). These development steps are not required to
use the downloaded playbooks.

## License

No reuse license has been selected yet. Public visibility alone does not grant
permission to reuse, modify, or redistribute these files. License terms will be
added separately once confirmed by the rights holder.
