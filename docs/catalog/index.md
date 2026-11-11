# Public Playbook Catalog

The public collection contains these seven YAML files. Download the named
`radkit-playbooks.zip` asset from the
[collection release](https://github.com/tookada/radkit-playbooks/releases/latest).
The YAML itself is the authoritative command list; review it before execution.

| Platform | Playbook | Guide |
|---|---|---|
| ACI | [aci_on_demand_techsupport](https://github.com/tookada/radkit-playbooks/blob/main/playbooks/aci/aci_on_demand_techsupport.yaml) | [ACI collection](aci-techsupport.md) |
| CEE | [cee_tac_debug_create](https://github.com/tookada/radkit-playbooks/blob/main/playbooks/cee/cee_tac_debug_create.yaml) | [CEE collection](cee-tac-debug.md) |
| CEE | [cee_tac_debug_fetch](https://github.com/tookada/radkit-playbooks/blob/main/playbooks/cee/cee_tac_debug_fetch.yaml) | [CEE collection](cee-tac-debug.md) |
| StarOS | [star_os_tech_support](https://github.com/tookada/radkit-playbooks/blob/main/playbooks/staros/star_os_tech_support.yaml) | [StarOS SSD](staros-ssd.md) |
| SMF / Nexus | [smf_nexus_status_validation](https://github.com/tookada/radkit-playbooks/blob/main/playbooks/smf/smf_nexus_status_validation.yaml) | [SMF and Nexus](smf-validation.md) |
| SMF | [smf_status_validation](https://github.com/tookada/radkit-playbooks/blob/main/playbooks/smf/smf_status_validation.yaml) | [SMF and Nexus](smf-validation.md) |
| IOS XR | [ios_xr_deepscan_diagnostics](https://github.com/tookada/radkit-playbooks/blob/main/playbooks/xr/ios_xr_deepscan_diagnostics.yaml) | [DeepScan](ios-xr-deepscan.md) |

Collection and program versions are independent. Publication does not establish
live compatibility with every listed platform. The current native-wheel live
pilots cover limited StarOS collection only, with remote cleanup disabled.
See [compatibility](../getting-started/installation.md) and
[operational safety](../user-guide/safety.md).

Legacy high-memory/BGP examples and other platform categories are not separate
downloads in this public collection.
