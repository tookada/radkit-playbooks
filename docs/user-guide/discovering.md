# Discovering and Inspecting Playbooks

Playbooks are discovered recursively under the configured `playbook_dir`.
Point to the extracted collection's `playbooks/` directory, not the repository
root, which contains unrelated workflow and site configuration YAML.

```python
print(pb.list())
print(pb.list("Diagnostics"))
print(pb.list("EPC"))
```

The list shows each playbook's name, group, device type, command count, and
description. Group names come from YAML, not directory names.
Use unique playbook names across the whole directory tree.

## Inspect Before Execution

```python
print(pb.show("star_os_tech_support"))
print(pb.show("cee_tac_debug_fetch"))
```

Inspect the required variables, target routing, command sequence, collection
settings, and deletion steps. `pb.show()` is not permission to run the playbook.
The [public catalog](../catalog/index.md) describes the seven downloadable
playbooks; other workflows mentioned in old examples are not part of this release.

If discovery fails, confirm the directory, YAML syntax, unique names, and the
installed program version. The repository's static validator is not the complete
runtime schema. See the [complete YAML reference](../PLAYBOOK_YAML_GUIDE.md).
