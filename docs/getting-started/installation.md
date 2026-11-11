# Installation and Compatibility

## Current Availability

**Public program wheels are not yet released.** This page describes the selected
targets and verified pilot scope, not a completed customer installation procedure.
Binary releases will be available from
[radkit-playbook-releases](https://github.com/tookada/radkit-playbook-releases).

Do not install from an unverified source or use a wheel for a different Python
ABI, operating system, or CPU.

## Initial Targets and Pilot Evidence

All three pilots used standard, GIL-enabled CPython 3.14 and RADKit 2.0.15.
Each passed 105 source tests and 105 installed-wheel tests, plus a limited StarOS
version/SSD-generation/SFTP-download test.

| Target | Pilot interpreter and OS | Program wheel platform |
|---|---|---|
| macOS arm64 | Python 3.14.10; macOS 26.7.3 | `macosx_11_0_arm64` |
| Windows x64 | Python 3.14.9; Windows x64 | `win_amd64` |
| Linux x86_64 | Python 3.14.10; Ubuntu 18.04, glibc 2.27 | `manylinux2014_x86_64` / `manylinux_2_17_x86_64` |

The macOS 11.0 tag reflects checked compilation settings; macOS 11 and every
intervening version were **not** runtime-tested. The Linux program wheel passed
auditwheel's glibc 2.17 policy, which is not validation of every RADKit dependency
or distribution. Ubuntu 18.04 was a legacy lab host, not a recommended customer OS.

Intel macOS, Windows/Linux ARM64, Alpine/musl, other Python versions, and
free-threaded Python are outside this initial target matrix.

The live tests disabled cleanup only in local YAML copies. Live deletion, TAC
upload, other device platforms, and original RADKit installer launcher
integration were not established by these tests. A RADKit certificate
serial-number deprecation warning was observed without preventing collection.

## Installation Requirements

Before customer release, the installation procedure must confirm:

1. A working, authorized [RADKit client](https://radkit.cisco.com/) environment.
2. The exact interpreter that the RADKit session uses and its Python ABI/CPU.
3. Installation of the matching wheel and its runtime dependencies into that
   interpreter's environment, without modifying an unrelated Python installation.
4. Successful import and discovery from the intended client or launcher.

Program wheels contain native modules, not a universal `py3-none-any` package.
The program does not bundle RADKit or all Python dependencies. An offline
installation needs compatible dependency wheels prepared in advance; copying
only the program wheel is not a complete offline-installation procedure.

Exact customer commands will be published after launcher integration, dependency
handling, and license terms are confirmed.

## Download the YAML Collection

From the [latest playbook release](https://github.com/tookada/radkit-playbooks/releases/latest),
download `radkit-playbooks.zip` and `SHA256SUMS`.
Use the named ZIP asset, not GitHub's automatic source archive.

On macOS:

```bash
shasum -a 256 -c SHA256SUMS
unzip radkit-playbooks.zip -d ~/radkit-playbooks
```

On Linux, use `sha256sum -c SHA256SUMS`. On Windows, compare the SHA-256 value
from `Get-FileHash .\radkit-playbooks.zip -Algorithm SHA256` with `SHA256SUMS`,
then extract with `Expand-Archive`.

Extract into a fresh directory when updating, and point `playbook_dir` to the
contained `playbooks/` directory, not the repository root.
Program and collection releases are independent; check each release's
compatibility notes. License terms remain pending.
