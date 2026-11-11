# ACI On-Demand TechSupport

`aci_on_demand_techsupport` targets an APIC inventory entry and collects the three
On-Demand TechSupport archives for one fabric switch.

```python
print(pb.preview(
    "aci_on_demand_techsupport",
    target_node="apic-01",
    variables={"node_id": 101},
))
```

`apic-01` and switch ID 101 are illustrative. The primary target is the controller,
not the switch. The required `node_id` is an integer from 101 to 4000.

The public YAML uses the ACI collector, 30-second status polling, a 1,800-second
collection timeout, a 3,600-second per-file transfer budget, and `cleanup: false`.
Its trigger includes upgrade logs.

Every controller that may store an artifact must have an appropriate RADKit
inventory entry and SFTP access. If inventory names differ from discovered APIC
names, use `collection.apic_devices` in a trusted local copy.

Success requires a new completed collection and all three verified artifacts.
A pending collection, changed job, missing file, or size mismatch is a failure.
A timeout does not cancel the controller's job.

Local concurrency exclusion is scoped to the same OS user, machine, RADKit
service, and switch ID; it is not a distributed fabric-wide lock.
See the [complete reference](../PLAYBOOK_YAML_GUIDE.md) for mappings, verification,
cleanup, supported trigger forms, and concurrency limits.

Do not treat the native-wheel StarOS tests as live ACI validation.
