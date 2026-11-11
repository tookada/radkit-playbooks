# Multi-Device Command Routing

Modern network operations frequently cross infrastructure boundaries—such as diagnosing an edge router, inspecting its connected switch, or querying a Kubernetes cluster manager alongside a 5G core node.

RADKit Playbook supports **per-command multi-device routing** using the `target:` attribute.

---

## Basic Command Routing

By default, every command executes against the primary `target_node` supplied to `pb.run()`. You can override this on any individual step:

```yaml
commands:
  # Step 1: Runs on primary target router
  - id: check_bgp
    command: show bgp summary

  # Step 2: Routed specifically to a different device
  - id: check_switch
    target: "leaf-switch-01"
    command: show interface status
```

---

## Dynamic Routing via Variables

You can bind `target:` to a playbook variable:

```yaml
variables:
  k8s_node:
    type: string
    required: true
    description: Hostname of Kubernetes control plane node

commands:
  - id: get_pods
    target: "{{ variables.k8s_node }}"
    device_type: LINUX
    command: kubectl get pods -A
```

---

## Dynamic Routing via Captured IP or Step Output

You can route a command to an IP address discovered by a previous step:

```yaml
commands:
  # Step 1: Discover VIP from router/CEE
  - id: get_ingress_vip
    command: show running-config k8s ingress-host-name
    capture:
      vip:
        regex: '(?P<value>(?:\d{1,3}\.){3}\d{1,3})'

  # Step 2: Runner resolves IP directly against RADKit inventory host attributes!
  - id: check_k8s_host
    target: "{{ steps.get_ingress_vip.vip }}"
    command: hostname
```

---

## Target Fallback Syntax (`or`)

You can provide an optional override variable with fallback to a captured step value:

```yaml
  - id: run_kubectl
    target: "{{ variables.k8s_node or steps.get_ingress_vip.vip }}"
    command: kubectl get nodes
```
If `variables.k8s_node` is non-empty, it routes to that explicit device; otherwise, it falls back to the discovered IP.
