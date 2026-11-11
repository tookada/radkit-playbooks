# Captures & Chaining

Captures allow playbooks to extract dynamic values from command CLI outputs using regular expressions and chain them into subsequent steps or loops.

---

## Defining Named Captures

Use the `capture:` block inside any command step:

```yaml
commands:
  - id: process_lookup
    command: "show process bgp"
    description: Extract Job ID (JID) of the BGP daemon
    capture:
      jid:
        regex: '(?i)Job\s+Id\s*[:=]\s*(?P<value>\d+)'
        match: first
        type: string
        required: true
```

### Capture Attributes:
* **`regex`**: A Python regular expression. `first` and `all` require the named
  group selected by `group`, which defaults to `value`; prefer `(?P<value>...)`.
* **`match`**:
  * `"first"`: Returns the first matching string scalar.
  * `"all"`: Returns a list of all matching items across the output buffer.
* **`required`**: Defaults to `true`; a missing required capture fails the step.
* **`sensitive`**: Masks structured captured values, not raw CLI output or archives.
* **`match: count`**: Counts regex matches and does not require a capture group.

---

## Chaining Captured Values into Next Steps

Reference captured values in subsequent steps using `{{ steps.<step_id>.<capture_name> }}`:

```yaml
  # Step 1 captured JID:
  # steps.process_lookup.jid = "1023"

  # Step 2 uses the captured JID:
  - id: memory_heap_drilldown
    command: "show memory heap {{ steps.process_lookup.jid }}"
    description: Inspect heap chunks for the resolved Job ID
```

---

## Iterating with `foreach`

When a capture uses `match: all`, it yields a list. You can loop over that list using `foreach:`:

```yaml
commands:
  # 1. Discover all CPU locations
  - id: discover_locations
    command: show platform
    capture:
      locations:
        regex: '^(?P<value>\d+/(?:RSP\d+|RP\d+|\d+)/CPU\d+)\b'
        match: all
        max_items: 16

  # 2. Iterate over each location
  - id: check_memory_per_location
    foreach: "{{ steps.discover_locations.locations }}"
    as: cpu_node
    max_items: 16
    command: "show memory summary location {{ cpu_node }}"
```
* **`as`**: Defines the loop variable name (`cpu_node`), accessible inside the command string.

Bound both captures and loops to avoid unexpectedly large diagnostic fanout.
