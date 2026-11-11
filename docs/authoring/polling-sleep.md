# Polling & Timed Observation

Diagnostic workflows often require waiting for an asynchronous background task to complete (e.g. log gathering) or pausing to observe metrics over time (e.g. memory leak progression or route convergence).

---

## 1. Declarative Polling (`poll:`)

When a command initiates background work (like `tac-debug-pkg create`), subsequent status queries must be polled repeatedly until complete.

Instead of writing procedural Python while-loops, configure a declarative `poll:` block:

```yaml
  # Step 1: Initiate background log creation
  - id: create_debug_pkg
    command: "tac-debug-pkg create last 15m"
    capture:
      tac_id:
        regex: '(?i)id\s*[:=]\s*(?P<value>\d+)'

  # Step 2: Poll status until gathering completes
  - id: wait_debug_ready
    command: tac-debug-pkg status
    description: Check status every 10 seconds until microservices finish
    poll:
      until_pattern: "No active tac debug session"
      interval: 10   # poll every 10 seconds
      timeout: 900   # maximum 15-minute safety threshold
```

### How Polling Operates:
1. Executes `command`.
2. Searches output using the `until_pattern` regular expression.
3. If not matched, pauses for `interval` seconds and repeats.
4. Emits real-time progress:
   `[node] Polling condition '...' not yet met (40s/900s). Waiting 10s...`
5. If `timeout` expires without matching, the step fails with a clear timeout message.

---

## 2. Timed Observation Windows (`type: sleep`)

For differential diagnostics—such as memory leak comparison or CRC error rate observation—you must establish a baseline, pause for a fixed window, and measure the delta.

Use `type: sleep`:

```yaml
  # 1. Baseline start
  - id: memory_compare_start
    command: show memory compare start

  # 2. Timed observation window
  - id: memory_compare_wait
    type: sleep
    duration: "{{ variables.wait_time_seconds }}"
    description: "Observation interval: waiting for memory drift and leak progression"

  # 3. Capture delta report
  - id: memory_compare_report
    command: show memory compare report
```

### Sleep Step Features:
* **Dynamic Durations**: Supports variables (e.g. `duration: "{{ variables.wait_time_seconds }}"`).
* **Duration Validation**: Uses 300 seconds when omitted. Explicit durations must resolve to positive integer seconds; invalid values fail the step and follow `continue_on_error` rather than silently using a default.
* **Execution Guards**: Honors `when`, `requires_step`, target inventory checks, and per-step `device_type` before waiting.
* **Non-Blocking Countdown**: Loops in 1-second increments, printing progress every 30 seconds (`[router] Sleeping: 180s remaining...`).
* **Clean Audit Recording**: Generates a standard `CommandResult(status="SUCCESS", command="sleep 300s")` in your session log.
