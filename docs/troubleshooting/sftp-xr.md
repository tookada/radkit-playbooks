# SFTP Readiness on IOS XR

Working SSH CLI access does not prove that SFTP transfers are enabled or
authorized. Confirm the platform/release-specific SFTP server configuration,
user permissions, reachable filesystem, and free space before collection.

An authorized operator can inspect the relevant SSH configuration, for example:

```text
show running-config ssh
```

Configuration syntax and VRF behavior vary by platform and release. Follow the
appropriate Cisco IOS XR administration documentation; this project does not
automatically configure or enable a device's SFTP server.

If a transfer fails, inspect the run's step/artifact errors and whether remote
files remain. Do not delete the archive while manual recovery is needed.
Configured file-capture cleanup does not run when required artifact verification
fails. Preview alone does not test the SFTP subsystem.

For Admin-VM collections, also review the active RP/VM discovery and bridge-copy
behavior described in [file capture](../authoring/file-capture.md).
