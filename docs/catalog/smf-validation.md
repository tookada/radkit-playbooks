# SMF and Nexus Validation

## SMF Status

`smf_status_validation` runs SMF operational commands and evaluates captured
status patterns. Its inventory type is `ULTRA_CORE_5G_SMF`.

```python
print(pb.preview("smf_status_validation", target_node="smf-01"))
result = pb.run("smf_status_validation", target_node="smf-01")
print(result)
```

Checks include system readiness, NRF registration, role redundancy, BFD/BGP
neighbor output, and georeplication output. Review the YAML's exact regexes and
expected values against your software version.

## SMF and Adjacent Nexus Nodes

`smf_nexus_status_validation` routes checks to SMF devices and adjacent Nexus
inventory entries (`NX_OS`) using list variables:

```python
print(pb.preview(
    "smf_nexus_status_validation",
    variables={
        "smf_node": ["smf-01"],
        "leaf_switches": ["leaf-01", "leaf-02"],
    },
))
```

All names are fictional. Use the same reviewed variable mapping for `pb.run()`
when authorized. Read each per-device result; a successful transport command can
still have a failed health assertion.

These are targeted pattern-based checks, not a complete health certification.
The native-wheel live pilots did not validate SMF or Nexus execution.
