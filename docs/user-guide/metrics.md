# Local Utilization and Estimated Time Savings

The program can record local execution metrics under
`~/.radkit/playbook_metrics/`. This metrics feature does not send its events to
a telemetry service. RADKit connectivity and optional TAC upload have separate
network behavior; do not describe the entire system as air-gapped.

```python
pb.metrics()  # pb.stats() is an alias
pb.metrics(playbook="star_os_tech_support")
pb.metrics(since="2026-10-01", until="2026-11-01")
```

Dates without a timezone are UTC. Both bounds are inclusive; a date-only value
denotes midnight UTC. Invalid dates raise `ValueError`.

## Estimated, Not Measured Savings

Authors can declare estimates:

```yaml
effort:
  manual_minutes: 25
  per_node_minutes: 0
```

The manual baseline adds `per_node_minutes` for additional targets.
Estimated savings are the nonnegative difference between that baseline and
automated runtime. Only fully successful runs with a declared baseline receive
savings credit. These are author-provided estimates, not measured engineering
effort or an operational SLA.

Reports can be exported:

```python
pb.metrics().export("playbook_usage.csv")
pb.metrics().export("playbook_usage.md")
```

Treat reports as private operational records, especially when playbook names
or optional identity fields identify an environment.

## Privacy and Configuration

```python
pb.configure(metrics_enabled=False)
pb.show_config()
```

The `RADKIT_PLAYBOOK_METRICS=0` environment variable disables recording even on
an already-bound client. `false`, `no`, and `off` also disable it.

Identity collection is opt-in:

```python
pb.configure(metrics_include_identities=True)
```

When enabled, events can include the OS username, RADKit client identity,
inventory names, and local hostname. Do not enable this unless permitted by
your data-handling policy.

POSIX metric directories/files use restrictive permissions where supported.
Those mode checks do not establish Windows ACL privacy guarantees; review
Windows permissions separately. Metrics privacy settings do not sanitize raw
run logs or diagnostic archives.
