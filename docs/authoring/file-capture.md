# File Capture & Cleanups

Heavy diagnostics—such as `show tech`, StarOS SSDs, and Kubernetes debug archives—generate files on device storage. RADKit Playbook handles the full lifecycle: generation, inter-VM transfer, SFTP download, file verification, and automated cleanup.

---

## 1. Declaring a File Capture Step

Mark the step with `type: file_capture`:

```yaml
  - id: ssd_collection
    type: file_capture
    command: "show support details to file /sftp/{{ target }}_ssd_{{ timestamp }} compress -n"
    description: Generate StarOS SSD bundle
    generated_path:
      regex: '(\/sftp\/\S+\.tar\.gz|\S+_ssd_\S+\.tar\.gz)'
    cleanup: "delete {{ remote_file_path }} -n"
    timeout: 1800
```

---

## 2. Remote Path Resolution (`generated_path:`)

You can specify how the runner resolves the generated file path on the remote device:

### Option A: Via Regex Matching
Inspects the command output and extracts the generated filename:
```yaml
    generated_path:
      regex: 'Show tech output available at (\S+\.tgz)'
```

### Option B: Deterministic Path Template
Explicitly specifies the exact file location without relying on output parsing:
```yaml
    generated_path:
      path: "/tmp/{{ variables.cee_node }}_{{ steps.create_debug_pkg.tac_id }}.tar"
```

---

## 3. Automated Post-Download Cleanup (`cleanup:`)

To prevent filling up flash memory or harddisks on customer nodes, configure `cleanup:`. The file-capture cleanup runs **only after all required artifacts** have been
downloaded and verified. Checks include nonzero size, available expected size,
archive integrity where supported, and a recorded local SHA-256. A local hash is
not a remote checksum comparison. Failed verification prevents cleanup.
Separate explicit cleanup command steps must be reviewed independently.

### Simple Non-Interactive Cleanups:
```yaml
    cleanup: "rm -f {{ remote_file_path }}"
    # Or on StarOS:
    cleanup: "delete {{ remote_file_path }} -n"
```

### Interactive Cleanups with Confirmation Prompts:
```yaml
    cleanup:
      command: "delete {{ remote_file_path }}"
      interactive:
        prompt: 'Delete.*?\[confirm\]'
        response: 'y'
```

---

## 4. Cisco IOS-XR 64-bit Calvados & VM1 Boundaries

On Cisco IOS-XR 64-bit eXR platforms (ASR 9000, NCS 5500, 8000), `admin show tech` commands generate files inside the isolated **Calvados Admin VM**, but SFTP/SCP access only exists inside **XR VM1**.

RADKit Playbook automatically handles this boundary:
1. Detects `admin show tech` commands.
2. Dynamically queries `show platform` and `admin show sdr` to locate the active RP and SDR VM (`VM1` or `VM2`).
3. Executes an internal `admin copy ... location <rp> harddisk: location <rp>/<vm>` to bridge the file into XR VM1.
4. Downloads the file via SFTP.
5. Performs a **Two-Stage Cleanup**:
   * Deletes the bridged copy from XR VM1 (`delete harddisk:/...`).
   * Deletes the original file from the Calvados Admin VM (`admin delete harddisk:/showtech/...`).

The two-stage deletion applies only when cleanup is enabled. RP/VM discovery and
transfer failures are reported explicitly. Review
[operational safety](../user-guide/safety.md), and consult the
[complete reference](../PLAYBOOK_YAML_GUIDE.md) for ACI multi-artifact collection,
timeouts, locking boundaries, partial transfers, and cleanup failures.
