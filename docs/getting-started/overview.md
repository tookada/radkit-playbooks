# Overview and Operational Boundaries

RADKit Playbook adds reusable YAML workflows to a connected RADKit service.
It does not replace RADKit installation, authentication, inventory management,
or device authorization.

```text
Operator's Python / RADKit environment
    +-- RADKit Playbook + local YAML collection
    |       +-- local run logs, artifacts, and optional usage metrics
    |
    +-- connected RADKit service --> authorized inventory devices
    |
    +-- optional client-side upload --> Cisco TAC case
```

## Execution Model

1. Bind to the existing `service` using `rpb.bind(service, ...)`.
2. Discover local playbooks with `pb.list()` and inspect one with `pb.show()`.
3. Use `pb.preview()` to review inventory matching and command routing.
4. Execute the reviewed YAML using `pb.run()`.
5. Inspect execution status, validation results, and downloaded files separately.

Playbooks can route individual commands to other inventory devices, capture
values from output, iterate over captured lists, poll for completion, and wait
between observations. See the [authoring reference](../PLAYBOOK_YAML_GUIDE.md).

## Safety Boundaries

- YAML contains commands, not a sandboxed description of intent. Trust the file
  and every supplied variable before execution.
- Diagnostic commands can create files, initiate collection jobs, or delete
  remote packages. "Diagnostics" does not mean read-only or zero impact.
- File capture downloads and verifies artifacts before its configured cleanup.
  Additional explicit command steps can also delete files; inspect the full YAML.
- RADKit connectivity and authentication have their own network requirements.
  Local metrics or an offline documentation copy do not make a remote RADKit
  session fully disconnected.
- Optional TAC upload operates from the client using local logs/artifacts and
  requires authorization, case access, and network connectivity.

Refer to [operational safety](../user-guide/safety.md) before production use.
