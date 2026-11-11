# Complete YAML Authoring Reference

This reference describes the public YAML interface for human authors and AI
tools creating RADKit Playbook files. Examples are illustrative, not customer
configurations. Use only documented features and review every command before use.

## Discovery and file placement

- Supported extensions are `.yaml`, `.yml`, and `.json`.
- The configured Playbook directory is searched recursively.
- Product-oriented subdirectories are recommended.
- A Playbook `name` SHOULD be unique across the entire directory tree. If names
  are duplicated, lookup behavior is ambiguous because execution selects the
  first matching file in sorted path order.

Example layout:

```text
~/.radkit/playbooks/
├── cndp/
│   ├── cndp_hc.yaml
│   └── kubernetes_pod_health.yaml
├── smf/
│   └── subscriber_diagnosis.yaml
└── transport/
    └── router_health.yaml
```

## Minimal Playbook

```yaml
name: show_version
description: Collect the software version
group: Common
device_type: LINUX
commands:
  - id: collect_version
    command: uname -a
    description: Display kernel and operating system information
```

The following top-level fields are required:

| Field | Type | Rule |
|---|---|---|
| `name` | string | MUST be non-empty and SHOULD be globally unique. |
| `description` | string | MUST be non-empty. |
| `commands` | list | MUST contain at least one command object. |

Optional top-level fields:

| Field | Type | Default | Meaning |
|---|---|---|---|
| `group` | string | `Ungrouped` | Category shown by `pb.groups` and `pb.list(group=...)`. |
| `device_type` | string | any | Required inventory device type. A mismatch causes `SKIPPED`. |
| `variables` | object | `{}` | User-supplied and default input definitions. |
| `continue_on_error` | boolean | run setting | Overrides the run argument when present. A command can override this setting. |
| `effort` | object | `null` | Productivity baselines (`manual_minutes`, `per_node_minutes`) for offline estimated time savings. |

Directory names do not automatically set `group` or `device_type`. Declare
those fields explicitly when required.

## Variables

Variables are declared as a mapping and supplied to `pb.run()` or
`pb.preview()` through the `variables` argument.

```yaml
variables:
  namespace:
    type: string
    required: false
    default: smf-data
    description: Kubernetes namespace to inspect
    pattern: '^[a-z0-9-]+$'
    choices: []
    example: smf-data
    sensitive: false
commands:
  - command: kubectl get pods -n {{ variables.namespace }}
```

Supported variable types:

- `string`
- `integer`
- `float`
- `boolean`
- `list`

Variable field rules:

| Field | Default | Rule |
|---|---|---|
| `type` | `string` | MUST be one of the supported types. |
| `required` | `false` | Missing required values fail before command execution. |
| `default` | none | Used when the caller does not supply a value. |
| `description` | empty | SHOULD explain purpose and expected format. |
| `pattern` | none | Python regular expression applied as a full-string match. |
| `choices` | `[]` | Converted value MUST equal one listed item. |
| `example` | none | Displayed by `pb.show()` as usage help. |
| `sensitive` | `false` | Masks the value in structured run output and help; does not sanitize raw CLI output or archives. |

Boolean inputs accept `true`, `yes`, `1`, and `up`, or `false`, `no`, `0`, and
`down`, without case sensitivity.

## Commands

```yaml
commands:
  - id: list_pods
    command: kubectl get pods -n {{ variables.namespace }}
    description: List Pods in the selected namespace
    continue_on_error: false
```

| Field | Required | Default | Rule |
|---|---|---|---|
| `command` | yes | none | MUST be a non-empty string. |
| `id` | no | `command_NNN` | MUST be unique within the Playbook. Use an explicit ID when another step references it. |
| `description` | no | empty | SHOULD describe intent rather than repeat the command. |
| `capture` | no | `{}` | Extracts typed values from command output. |
| `validations` | no | `[]` | Evaluates captured values as `OK` or `FAIL`. |
| `foreach` | no | none | Sequentially executes the command for each item in a captured list. |
| `as` | no | `item` | Loop variable name. MUST match `[A-Za-z_][A-Za-z0-9_]*`. |
| `on_empty` | no | `fail` | One of `fail`, `skip`, or `continue`. |
| `max_items` | no | none | Rejects a loop whose resolved list exceeds this size. |
| `continue_on_error` | no | run setting | Overrides run-level behavior for this step. |
| `when` | no | none | Executes only when the referenced value equals the specified literal. |
| `requires_step` | no | none | Skips this step unless the referenced step has a successful command result. |
| `fail_on_cli_error` | no | `false` | Treats recognized CLI error lines as execution failures even if transport reports success. |
| `fail_on_validation` | no | `false` | Treats failed validations as `VALIDATION_FAILED` and prevents file download and cleanup. |

Commands execute sequentially in listed order. Do not reference captures from a
later command.

### Conditional execution

Use `when` to branch in the Playbook rather than sending shell syntax to a
network device CLI:

```yaml
  - id: merge_debug_pkg
    command: tac-debug-pkg merge tac-id {{ variables.tac_id }}
    when:
      source: steps.check_existing_merged_tar.merge_state
      equals: MERGE_NEEDED
```

`when` MUST contain exactly `source` and `equals`. `source` is a dotted
reference without template braces; `equals` is a literal compared using typed
equality. A mismatch records `SKIPPED`; a missing reference is an execution
failure. As with other skipped commands, a run containing both successful and
skipped steps reports `PARTIAL_SUCCESS`. Preview does not evaluate conditions
that depend on runtime captures.

For CEE TAC packages, reuse an existing valid archive instead of merging it
again. An empty or corrupt existing archive must stop the fetch. Copy completion
must be captured from a result line, not from the echoed command, before SFTP
starts. CEE staging commands use `umask 077` and `chmod 600`; package deletion
requires the download step to succeed with a non-empty local file.

## Show Tech and generated diagnostic files

Use the same `type: file_capture` for XR Show Tech, ACI On-Demand TechSupport,
and other generated diagnostic files. There are no platform-specific run APIs.

```yaml
- id: collect_xr_os
  type: file_capture
  command: show tech os
  timeout: 1800
```

The shared workflow generates the diagnostics, identifies the required files and
their source devices, downloads via RADKit SFTP, verifies the files, and records
them in `run.json`. Local collection never depends on CXD availability.

| Command field | Default | Meaning |
|---|---|---|
| `type` | `exec` | Set to `file_capture` to collect generated files. |
| `timeout` | `600` | Positive integer seconds for collection, including preflight, command execution, and completion polling. |
| `generated_path.regex` | platform pattern | First capture group identifies the generated path for non-ACI collectors. |
| `generated_path.path` | none | Explicit rendered path for non-ACI collectors; takes precedence over `regex` when both are supplied. |
| `execution_method` | `exec` | `exec_sequence` is available when a CLI interaction is required. |
| `interactive` | none | Confirmation `prompt` regex and optional `response` (default `y`). |
| `cleanup` | `false` | Optional remote cleanup, only after **all** required files are locally verified. |
| `collection` | defaults below | Optional collection settings; only valid with `file_capture`. |

`collection` fields:

| Field | Default | Meaning |
|---|---|---|
| `collector` | `auto` | One of `auto`, `ios_xr`, `aci`, `generic`. |
| `poll_interval` | `30` | Finite positive number of seconds between ACI status queries. |
| `transfer_timeout` | `600` | Finite positive per-file SFTP time budget, shared by path attempts. Separate from collection timeout. |
| `apic_devices` | `{}` | Optional explicit mapping of APIC ID to RADKit inventory name. |

`auto` recognizes ACI `trigger techsupport switch ...` commands and XR inventory
types containing `XR`. Other platforms use the generic collector, supporting
existing Nexus path detection or an explicit `generated_path.regex`. Inventory
type `LINUX` alone does **not** identify an ACI switch.

For example, StarOS SSD continues to use a custom path expression:

```yaml
- id: collect_ssd
  type: file_capture
  command: show support details to file /sftp/{{ target }}_ssd_{{ timestamp }} compress -n
  generated_path:
    regex: '(/sftp/\S+\.tar\.gz)'
  cleanup: 'delete {{ remote_file_path }} -n'
  timeout: 1200
```

### ACI On-Demand TechSupport

Run against an **APIC** inventory entry, not against the switch entry:

RADKit controller types `APIC` and `ACI_OS` are accepted as equivalent for
playbook/command type matching and storage-controller validation. The inventory
name may differ from the APIC hostname; use `collection.apic_devices` to map
controller IDs to their registered inventory names when needed.

```yaml
name: aci_techsupport
description: Collect all three switch TechSupport files through APIC
device_type: APIC
variables:
  node_id:
    type: integer
    required: true
    example: 101
commands:
  - id: techsupport
    type: file_capture
    command: trigger techsupport switch {{ variables.node_id }} include-upgrade-logs
    timeout: 1800
    collection:
      collector: aci
      poll_interval: 30
      transfer_timeout: 3600
    cleanup: false
```

```python
result = pb.run(
    "aci_on_demand_techsupport", "apic-01",
    variables={"node_id": 101},
)
```

The collector:

1. Reads `show version` to map controller IDs to names. If inventory names are
   aliases, set `collection.apic_devices`, for example `{"4": "controller-alias"}`.
   Explicit maps must include every controller that may store the artifacts.
   Register every possible storage APIC in the RADKit inventory with SFTP access;
   registering only the initiating APIC is insufficient. The mapping identifies
   existing inventory entries; it does not proxy transfers through another APIC
   or control which controller ACI selects as the storage destination.
2. Reads `show techsupport switch <node_id> status` before triggering. A pending
   collection is an error; it is not overwritten or automatically restarted.
3. Triggers collection and polls the same status command. Only a **new**
   `Collection Time` reaching `Status: success` is accepted. Unexpected status,
   job replacement, CLI errors, or timeout are reported as failures.
4. Parses folded Config/Db/Log locations and sizes, including `on APIC <id>`.
   Resolves the actual storage APIC rather than assuming the initiating APIC.
5. Downloads and verifies **all three** archives (`_1of3.tgz`, `_db_2of3.tgz`,
   `_logs_3of3.tgz`). Missing files or size mismatches are failures, even if
   the APIC previously reported success.

Initially supports one switch ID (101-4000) per command, with or without
`include-upgrade-logs`. Ranges, controller-wide collection, and `remotename`
exports are not supported by this collector. Use sequential `foreach` with
`max_items` for multiple switch IDs. A collection timeout does not cancel the job
on APIC; inspect its state before retrying.

#### ACI concurrent collection exclusion

ACI capture automatically acquires a nonblocking local file lock keyed by
**RADKit service ID and switch node ID** before any collection preflight command.
The lock remains held through polling, downloads, verification, and optional
cleanup. A competing attempt returns `FAILURE` with an `already running` error
without sending device commands; it does not queue or join the active run.
No YAML changes are required.

Locks are shared by threads and separate Python processes running as the same
OS user on the same machine, even with different `output_dir` values or different
APIC inventory aliases. Different node IDs and different service IDs use separate
locks. Within one service, identical node IDs are conservatively serialized even
if they belong to different fabrics. A stable RADKit service ID is required;
missing identity or a lock-directory error fails explicitly before triggering.

Lock files are managed by `filelock` under `~/.radkit/playbook/locks/aci/`.
Locks are released after success or failure and by the OS on process termination;
do not delete lock files while captures are active. Remote collection may continue
after a client crash or timeout, so the existing APIC `pending` check still applies.
Run directories are reserved atomically to keep simultaneous runs' local results
separate.

This is not a distributed lock: different machines, OS users, service IDs pointing
to the same fabric, manual CLI operations, and older clients do not participate.
The APIC pending-job and collection-time checks remain as additional safeguards,
not a guarantee against those external races. XR and generic collectors do not
acquire this ACI lock. Parallel collection has not been validated on a live fabric.

The status parser is based on observed APIC 6.1(5e) output. Other release output
formats require validation before use. **Never send `?` help queries in a
`file_capture` command**: APIC may execute the partially entered command after
displaying help. Help queries and multiline collection commands are rejected.

### Local files, results, and cleanup

Artifacts are saved under the configured `output_dir`, within each run's
`files/<execution-target>/<command-result-index>/` directory. A separate
directory per command/iteration prevents repeated filenames from overwriting
earlier results. Incomplete or unverified transfers retain a `.part` suffix and
are never uploaded as collected artifacts.

Verification checks nonzero size, SFTP-reported size when available, ACI's
expected size, gzip integrity for `.tgz`/`.gz`, and readability for `.tar`.
A local SHA-256 is recorded. This is not a remote checksum comparison.
Large archives may take additional time to verify locally.

Each `CommandResult.artifacts` entry contains:

- `diagnostic_target` and `source_device` (different for ACI);
- `remote_path` and `local_path`;
- `status`, `size_bytes`, `expected_size`, and `sha256`;
- `cleanup_status` and `errors`.

The summary table and `run.json` include every artifact. Legacy
`remote_file_path` / `output_file` fields remain available as a view of the first
successfully verified artifact (or the first remote path if none succeeded).
Use `artifacts` for the complete list.

A failed file does not erase successfully downloaded siblings; the collection
is still reported as failed and **no remote cleanup is performed**. Cleanup
errors are explicit (`CLEANUP_FAILED`), while verified local artifacts remain
usable. `cleanup: false` is the default.

- XR Admin files are copied to the active XR VM before download. RP/VM discovery
  errors fail explicitly instead of silently assuming VM1. With cleanup enabled,
  both the XR copy and original Admin file are removed after verification.
- ACI supports `cleanup: true` to delete only this collection's three remote
  files from their storage APICs.
- Other collectors use a cleanup command string or
  `cleanup: {command: "...", interactive: {prompt: "...", response: "..."}}`.
  Only use cleanup when remote file deletion is intended.

`pb.upload(result, destination="cxd", sr_number="...")` uploads saved verified
artifacts and existing run logs without repeating collection. Saved artifacts
are checked against their recorded size and SHA-256 before upload. Optional
`upload_to_cxd` on `pb.run()` reuses this operation. Upload errors never delete
local artifacts or change collection success.

## Template expressions

Only simple dotted references are supported:

```yaml
command: kubectl get pods -n {{ variables.namespace }}
command: show ipam pool {{ pool_name }}
foreach: '{{ steps.discover_pools.pool_names }}'
```

Rules:

- Expressions MUST have the form `{{ identifier.path }}`.
- Arbitrary Python, filters, operators, indexing, and function calls are not
  supported.
- A command expression MUST resolve to a scalar, not a list or object.
- A `foreach` value MUST contain exactly one template expression and resolve to
  a list.
- `variables.<name>` refers to a resolved input variable.
- `steps.<step_id>.<capture_name>` refers to a previous step's capture.
- A loop variable such as `{{ pool_name }}` is available only inside its
  `foreach` command.
- Quote YAML scalar values containing template syntax when needed, especially
  the entire `foreach` expression.

Command-level `target` routing additionally accepts a two-reference fallback,
for example `{{ variables.k8s_node or steps.discover.k8s_ip }}`. This exception
does not enable operators in command strings or `foreach`.

All variable values interpolated into CLI or shell commands must be trusted.
Type checks and `sensitive: true` do not make arbitrary values safe to execute.

## Capturing command output

```yaml
commands:
  - id: discover_pools
    command: show ipam pool
    capture:
      pool_names:
        regex: '^(?P<value>[A-Za-z0-9_.-]+)\s+'
        match: all
        group: value
        type: string
        required: true
        sensitive: false
        flags: []
        transforms:
          - strip
        item_pattern: '^[A-Za-z0-9_.-]+$'
        max_items: 100
```

Capture regular expressions use Python regex syntax. `MULTILINE` and
`IGNORECASE` are always enabled.

| Field | Required | Default | Rule |
|---|---|---|---|
| `regex` | yes | none | Python-compatible regular expression. |
| `match` | no | `first` | One of `first`, `all`, or `count`. |
| `group` | no | `value` | Named regex group to extract for `first` and `all`. |
| `type` | no | `string` | Defaults to `integer` for `count`; otherwise `string`. |
| `required` | no | `true` | A missing match causes `CAPTURE_FAILED` when true. |
| `sensitive` | no | `false` | Masks captured data in structured results. |
| `flags` | no | `[]` | Values may be `IGNORECASE`, `MULTILINE`, or `DOTALL`. |
| `transforms` | no | `[]` | Values may be `strip`, `lower`, `upper`, or `remove_commas`. |
| `item_pattern` | no | none | Full-string regex validation after transforms. |
| `max_items` | no | none | Applies to `match: all`. |

For `match: first` and `match: all`, the regex MUST define the named group
selected by `group`. Prefer `(?P<value>...)` and omit `group`.

For `match: count`, no capture group is required. The result is the number of
regex matches.

Use single-quoted YAML strings for regexes so backslashes such as `\s` and `\d`
remain intact.

## Dynamic `foreach`

```yaml
commands:
  - id: discover_pools
    command: show ipam pool
    capture:
      pool_names:
        regex: '^(?P<value>\S+)\s+'
        match: all
        type: string
        max_items: 100

  - id: inspect_pool
    foreach: '{{ steps.discover_pools.pool_names }}'
    as: pool_name
    on_empty: fail
    max_items: 100
    command: show ipam pool {{ pool_name }}
```

Loop behavior:

- Items execute sequentially and duplicate values are removed.
- Nested loops are not supported.
- `on_empty: fail` marks execution as failed.
- `on_empty: skip` and `on_empty: continue` skip the empty step without adding
  an execution failure.
- Captures produced by a loop are aggregated as lists and can drive a later
  `foreach` through `steps.<id>.<capture>`.
- Use `max_items` on both the source capture and loop to limit unexpected fanout.

## Health validations

Validations belong to the same command as their source capture.

```yaml
commands:
  - id: check_pod_status
    command: kubectl get pods -A
    capture:
      non_running_count:
        regex: '^\S+\s+\S+\s+\d+/\d+\s+(?!Running(?:\s|$))\S+'
        match: count
        type: integer
    validations:
      - name: all_pods_are_running
        source: captures.non_running_count
        condition: equals
        expected: 0
```

Each validation requires all four fields:

| Field | Rule |
|---|---|
| `name` | MUST be non-empty and unique within the command. |
| `source` | MUST be `captures.<name>` and reference a capture in the same command. |
| `condition` | MUST be a supported condition. |
| `expected` | MUST be present and have a type compatible with the captured value. |

Supported conditions:

| Condition | Intended actual value | Meaning |
|---|---|---|
| `equals` | any | `actual == expected` |
| `not_equals` | any | `actual != expected` |
| `less_than` | number | `actual < expected` |
| `less_than_or_equal` | number | `actual <= expected` |
| `greater_than` | number | `actual > expected` |
| `greater_than_or_equal` | number | `actual >= expected` |
| `contains` | string or list | `expected` is contained in `actual` |
| `not_contains` | string or list | `expected` is not contained in `actual` |
| `count_equals` | list or sized value | `len(actual) == expected` |
| `all_less_than` | list of numbers | Every value is less than `expected`. |

Execution status and validation status are independent. A command may have
execution status `SUCCESS` and validation status `FAIL`. A validation failure
does not trigger `continue_on_error` by default. Set `fail_on_validation: true`
to make validation failures execution failures governed by `continue_on_error`.
Failed required captures and validations prevent file download and cleanup.

## Complete example

```yaml
name: namespace_pod_health
description: Validate Pod health in a selected Kubernetes namespace
group: CNDP
device_type: LINUX
variables:
  namespace:
    type: string
    required: true
    description: Kubernetes namespace
    pattern: '^[a-z0-9-]+$'
    example: smf-smf1
commands:
  - id: find_non_running_pods
    command: kubectl get pods -n {{ variables.namespace }} --no-headers
    description: Count Pods that are not Running
    capture:
      non_running_count:
        regex: '^\S+\s+\d+/\d+\s+(?!Running(?:\s|$))\S+'
        match: count
        type: integer
    validations:
      - name: no_non_running_pods
        source: captures.non_running_count
        condition: equals
        expected: 0
```

## AI generation rules

When generating or modifying a Playbook, an AI agent MUST:

1. Preserve existing behavior and fields unless the user requests a change.
2. Use a unique, stable `name` and explicit step `id` values.
3. Keep commands in dependency order.
4. Use only documented template references and validation conditions.
5. Quote regexes with YAML single quotes.
6. Define `(?P<value>...)` for every non-count capture unless another `group`
   is explicitly declared.
7. Add `max_items` to unbounded `match: all` captures and `foreach` loops.
8. Mark credentials, subscriber identifiers, tokens, and other sensitive values
   with `sensitive: true`.
9. Avoid embedding passwords, private keys, access tokens, or environment-specific
   secrets in YAML.
10. Avoid destructive commands unless the user explicitly requests them and the
    Playbook description clearly states the impact.
11. Ensure `expected` uses the correct YAML type. For example, use `0`, not
    `'0'`, when validating an integer capture.
12. Validate the generated file through `pb.show()`, `pb.preview()`, or the
    project test suite before presenting it as complete.

## Common invalid patterns

Do not generate arbitrary expressions:

```yaml
# Invalid: function calls and operators are unsupported.
command: show user {{ variables.name.upper() }}
foreach: '{{ steps.discover.items if steps.discover.items else [] }}'
```

Do not insert a list directly into a command:

```yaml
# Invalid: pool_names is a list.
command: show pools {{ steps.discover.pool_names }}
```

Use `foreach` instead:

```yaml
foreach: '{{ steps.discover.pool_names }}'
as: pool_name
command: show pool {{ pool_name }}
```

Do not reference another command's capture in a validation:

```yaml
# Invalid: validation sources are local captures only.
source: steps.discover.pool_names
```

Do not omit the named group for `first` or `all`:

```yaml
# Invalid: default group "value" is missing.
regex: '^Pool: \S+$'
match: all
```

Correct form:

```yaml
regex: '^Pool: (?P<value>\S+)$'
match: all
```

## Final checklist

- [ ] File extension is `.yaml`, `.yml`, or `.json`.
- [ ] `name`, `description`, and non-empty `commands` are present.
- [ ] Playbook name is unique across all product directories.
- [ ] Every referenced step appears earlier and has an explicit unique `id`.
- [ ] Every template resolves to a documented variable, step capture, or loop variable.
- [ ] Every non-count capture regex defines its selected named group.
- [ ] Every validation references a capture in the same command.
- [ ] Capture and validation types match.
- [ ] Potentially large captures and loops have `max_items`.
- [ ] Sensitive values are marked and no secrets are embedded.
- [ ] Device type and commands match the intended RADKit inventory target.