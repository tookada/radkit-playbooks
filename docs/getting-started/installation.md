# Installation

## Overview

RADKit Playbook runs YAML-defined workflows through Cisco RADKit to automate
device commands, validation, and diagnostic file collection. Install the program
as a Python wheel and download the YAML playbooks separately.

> **Beta for pilot users:** Features and behavior may change. Review the
> playbook and target devices before execution.

## Available Binaries

The pilot version uses **Python 3.14** and **RADKit Client 2.0.15**.
Choose the wheel matching your OS and CPU:

| OS | CPU | Wheel filename |
|---|---|---|
| macOS | Apple Silicon / arm64 | `radkit_playbook-0.1.0-cp314-cp314-macosx_11_0_arm64.whl` |
| Windows | x64 | `radkit_playbook-0.1.0-cp314-cp314-win_amd64.whl` |
| Linux (glibc) | x86_64 | `radkit_playbook-0.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl` |

Use standard CPython 3.14, not the free-threaded build.
Intel Macs and Alpine Linux (musl) are not supported by these wheels.

## Installation

### 1. Download

Download your wheel from
[v0.1.0 pilot beta](https://github.com/tookada/radkit-playbook-releases/releases/tag/v0.1.0).

Download `radkit-playbooks.zip` from the
[v0.1.0 YAML playbook release](https://github.com/tookada/radkit-playbooks/releases/tag/v0.1.0)
and extract it to a directory of your choice. The ZIP contains a `playbooks/`
directory.

### 2. Install RADKit and the Wheel

Install Python 3.14 for your OS and CPU first. Then run the commands below from
the directory containing your downloaded wheel. Use a new `.venv` so an existing
RADKit installation is not changed. Internet access is needed to install
dependencies.

#### macOS (Apple Silicon)

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install --index-url https://radkit.cisco.com/pip/ --extra-index-url https://pypi.org/simple cisco-radkit-client==2.0.15
.venv/bin/python -m pip install ./radkit_playbook-0.1.0-cp314-cp314-macosx_11_0_arm64.whl
.venv/bin/python -m pip check
.venv/bin/python -m radkit_client
```

#### Windows (PowerShell)

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --index-url https://radkit.cisco.com/pip/ --extra-index-url https://pypi.org/simple cisco-radkit-client==2.0.15
.\.venv\Scripts\python.exe -m pip install .\radkit_playbook-0.1.0-cp314-cp314-win_amd64.whl
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m radkit_client
```

#### Linux (x86_64)

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install --index-url https://radkit.cisco.com/pip/ --extra-index-url https://pypi.org/simple cisco-radkit-client==2.0.15
.venv/bin/python -m pip install ./radkit_playbook-0.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
.venv/bin/python -m pip check
.venv/bin/python -m radkit_client
```

Stop if any command fails. Always start RADKit with the environment's Python
command shown above, rather than a shortcut that uses another environment.

### 3. Load the Playbooks

Connect to your service following the [RADKit documentation](https://radkit.cisco.com/).
In that RADKit session, use your connected `service` object:

```python
from pathlib import Path
import radkit_playbook as rpb

pb = rpb.bind(
    service,
    playbook_dir=Path("~/radkit-playbooks/playbooks").expanduser(),
)
print(pb.list())
```

Replace the example path with the extracted `playbooks/` directory.
Continue with the [quickstart](quickstart.md) to preview and run a playbook.

If needed, compare your wheel's SHA-256 hash with its entry in the release's
`SHA256SUMS` using `shasum -a 256` (macOS), `sha256sum` (Linux), or
`Get-FileHash -Algorithm SHA256` (PowerShell).
