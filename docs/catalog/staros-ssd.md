# StarOS SSD Collection

`star_os_tech_support` has two steps:

1. `staros_version`: run `show version` and optionally capture version/build values.
2. `staros_ssd_capture`: generate a compressed SSD, download it through SFTP,
   verify it, and perform the YAML's configured cleanup.

| Setting | Value |
|---|---|
| Group | `Diagnostics` |
| Inventory device type | `STAR_OS` |
| Optional variable | `destination_path`, default `/sftp` |
| Remote deletion | Enabled by the public YAML after verified retrieval |

```python
print(pb.show("star_os_tech_support"))
print(pb.preview("star_os_tech_support", target_node="upf-01"))
# Run only after reviewing storage, permissions, commands, and deletion policy.
result = pb.run("star_os_tech_support", target_node="upf-01")
print(result)
```

`upf-01` is fictional. The generated filename includes the target and timestamp.
Collection can take substantial time and consume storage. **The two-step public
YAML does not include an automatic free-space check.** Check available storage
using commands supported by your StarOS version before starting.

To keep remote diagnostics, set the capture step's `cleanup: false` in a trusted
local copy. The native-wheel pilots on macOS, Windows, and Linux used that
override, verified both steps and the downloaded archive, and did not test live
deletion. This playbook contains no health assertions; `Validation: N/A` is not a
device health verdict.
