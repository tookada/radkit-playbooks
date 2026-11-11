# Operational Safety and Data Handling

## Before Execution

- Obtain authorization for every target, command, file transfer, and upload.
- Use only trusted YAML and trusted variable values. Variables may be inserted
  into shell or device CLI commands.
- Inspect the whole command list, not just its name or description.
- Preview inventory matching and target routing. Preview is not an online
  readiness or device health check.
- Check free space, collection duration, SFTP support, privileges, and acceptable
  CPU/bandwidth impact in a controlled environment.

## Collection and Deletion

Diagnostic collection is not necessarily read-only. It can start asynchronous
jobs, generate large archives, copy files between environments, and delete remote
files after retrieval. The CEE workflows also delete selected debug packages.

File-capture cleanup runs after required local artifacts verify successfully.
A playbook can have additional explicit cleanup command steps. To retain
evidence, review and disable every relevant deletion operation in a trusted local
copy before execution. Preserve the authoritative public YAML unchanged.

The native-wheel StarOS pilots used local copies with cleanup disabled.
They did not verify live deletion or every other playbook/device platform.

## Sensitive Outputs

CLI output and diagnostic archives can contain configurations, addresses,
user/subscriber identifiers, credentials, or customer data. A local SHA-256
establishes a recorded file identity, not confidentiality or permission to share.

`sensitive: true` masks selected structured values. It is not encryption and
must not be relied on to remove sensitive values from raw CLI output, command
strings, archives, or optional upload logs.

Store outputs outside this repository with access controls appropriate to the
environment. Apply your retention policy and review all files before sharing.
TAC upload is optional and requires separate approval and case authorization.

## Public Contributions

Never publish real customer names, inventory identifiers, service IDs, case or
subscriber IDs, credentials, internal links, raw outputs, or diagnostic archives.
Use fictional names, documentation-only addresses, and obvious placeholders.
Only explicitly public-facing documentation and YAML belong in this repository.
