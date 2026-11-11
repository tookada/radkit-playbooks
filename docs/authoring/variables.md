# Variables & Prompts

Variables allow playbooks to be parameterized across different environments, interface names, timestamps, and customer nodes.

---

## Defining Variables

Variables are defined under the top-level `variables` block:

```yaml
variables:
  interface_name:
    type: string
    required: true
    description: Target physical or bundle interface
    example: TenGigE0/0/0/1

  vlan_id:
    type: integer
    required: false
    default: 100
    description: Sub-interface 802.1Q VLAN tag

  enable_debug:
    type: boolean
    required: false
    default: false
    description: Include verbose debug counters
```

---

## Variable Schema Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `type` | string | `"string"` | Data type: `"string"`, `"integer"`, `"float"`, `"boolean"`, `"list"`. |
| `required` | boolean | `false` | If `true` and no default is provided, user must supply it. |
| `default` | any | `null` | Default fallback value if not specified by user. |
| `description` | string | `""` | Informational prompt text shown in interactive REPLs and `pb.show()`. |
| `pattern` | string | `null` | Regex string validating format (e.g. `'^[0-9]+$'`). |
| `choices` | list | `[]` | Enumerated list of permitted choices. |
| `sensitive` | boolean | `false` | Masks values in structured results and help; raw command output and archives still require review. |

---

## Using Variables in Command Templates

Reference variables inside commands using double curly braces: `{{ variables.<name> }}`:

```yaml
commands:
  - id: check_interface
    command: "show interface {{ variables.interface_name }}"
```

---

## Interactive Prompts

When running a playbook interactively, any `required: true` variable that has no `default` value will trigger an automatic user prompt in the terminal:

```text
The playbook requires input variables:

[1/1] Variable: interface_name (Type: string)
      Description: Target physical or bundle interface
      Enter value: TenGigE0/0/0/1
```

Provide required variables explicitly for unattended execution. Missing required
values fail when interactive input is unavailable.
Never put credentials or real subscriber identifiers into public examples.
Values are interpolated into commands; use only trusted, reviewed inputs.
See [data handling](../user-guide/safety.md) before sharing outputs.
