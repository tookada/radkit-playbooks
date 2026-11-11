# YAML Syntax & Schema

Playbooks in `radkit_playbook` are declarative YAML files stored under your configured `playbook_dir`. Every playbook follows a structured schema validated at load time.

---

## Minimal Playbook Example

```yaml
name: ping_health_check
description: Simple ping connectivity verification
group: Network
device_type: IOS_XR

variables:
  target_ip:
    type: string
    required: true
    description: IP address to ping
    example: 192.0.2.1

commands:
  - id: ping_step
    command: "ping {{ variables.target_ip }} count 5"
    description: Send 5 ICMP echo requests
    capture:
      success_count:
        regex: 'Success rate is 100 percent'
        match: count
        type: integer
    validations:
      - name: zero_packet_loss
        source: captures.success_count
        condition: equals
        expected: 1
```

---

## Playbook Top-Level Fields

| Field | Type | Required? | Description |
|---|---|:---:|---|
| `name` | string | **Yes** | Unique identifier for the playbook (alphanumeric and underscores). |
| `description` | string | **Yes** | Human-readable explanation of what this playbook does. |
| `group` | string | No | Category grouping for organization (e.g. `IOS-XR`, `Diagnostics`). |
| `device_type` | string | No | Enforces device type compatibility (e.g. `IOS_XR`, `STAR_OS`, `LINUX`). |
| `variables` | mapping | No | Input variables dictionary definition. |
| `commands` | list | **Yes** | Sequential list of command execution steps. |

---

## Command Step Schema (`commands:`)

Each item in `commands` supports the following properties:

| Property | Type | Default | Description |
|---|---|---|---|
| `id` | string | `command_NNN` | Unique step identifier used for referencing captured variables. |
| `command` | string | `""` | CLI command template string to execute. Optional if `type: sleep`. |
| `description` | string | `""` | Documentation explaining the step purpose. |
| `target` | string | `null` | Multi-device override routing expression (e.g. `'{{ variables.k8s_node }}'`). |
| `device_type` | string | `null` | Per-command device type override. |
| `type` | string | `"exec"` | Step type: `"exec"`, `"file_capture"`, or `"sleep"`. |
| `execution_method` | string | `"exec"` | `"exec"` (direct wait) or `"exec_sequence"` (interactive sequence). |
| `timeout` | integer | `600` | Execution timeout in seconds. |
| `capture` | mapping | `{}` | Named regex captures extracting output variables. |
| `validations` | list | `[]` | Assertion checks evaluated against command output or captures. |
| `poll` | mapping | `null` | Declarative polling configuration. |
| `duration` | int / str | `null` | Duration in seconds when `type: sleep`. |
| `generated_path` | mapping | `null` | Remote file path specification for `file_capture`. |
| `cleanup` | bool / str / dict | `false` | Optional cleanup after artifact verification; supported forms depend on the collector. |
| `foreach` | string | `null` | Template expression resolving to a list to iterate over. |
| `as` | string | `"item"` | Variable name assigned to the current loop item. |

`192.0.2.1` is a documentation-only address, not a live connectivity target.
Substitute an authorized destination before executing this example.
See the [complete reference](../PLAYBOOK_YAML_GUIDE.md) for conditional execution,
capture types, validation conditions, collection options, and limits.
