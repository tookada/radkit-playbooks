# IOS XR DeepScan Diagnostics

`ios_xr_deepscan_diagnostics` is a substantial sequence of Admin/XR support
collections and operational diagnostics for `IOS_XR` inventory devices.
It is not a lightweight first connectivity test.

```python
print(pb.show("ios_xr_deepscan_diagnostics"))
print(pb.preview(
    "ios_xr_deepscan_diagnostics",
    target_node="xr-01",
    variables={"cpu_locations": ["0/RP0/CPU0"]},
))
```

The `cpu_locations` list must match the intended hardware; YAML defaults are not
a discovery or compatibility guarantee.

Before any run:

- Review every command and the number of generated support archives.
- Budget device CPU, storage, collection time, and transfer bandwidth.
- Confirm SFTP, command privileges, and active RP/VM discovery where Admin files
  must be copied into an accessible XR filesystem.
- Review enabled remote deletion for both original and bridged copies.
- Validate the device/software behavior in a controlled environment.

See [SFTP readiness](../troubleshooting/sftp-xr.md) and
[file capture](../authoring/file-capture.md). The native-wheel StarOS pilots did
not validate DeepScan or IOS XR execution.
