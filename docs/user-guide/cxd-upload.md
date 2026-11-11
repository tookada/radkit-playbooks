# Optional Upload to Cisco TAC

TAC upload is separate from collecting diagnostic files. It sends selected local
artifacts and execution logs through the RADKit client's CXD integration to an
authorized support case. Obtain permission and inspect the files first.

The examples below require a real case number that you are authorized to access;
`<TAC_CASE_NUMBER>` is a placeholder, not a valid destination.

## Upload After Inspection

```python
result = pb.run("star_os_tech_support", target_node="upf-01")
print(result)
# Review the local outputs and obtain approval before the next operation.
upload_result = pb.upload(
    result,
    destination="cxd",
    sr_number="<TAC_CASE_NUMBER>",
)
print(upload_result)
```

Upload uses saved artifacts without repeating collection. It checks recorded
artifact size and SHA-256 before sending them. Existing formatted execution logs
are also included; these logs can contain raw device output.

## Upload at the End of a Run

After confirming authorization, destination, and the data-sharing policy:

```python
result = pb.run(
    "star_os_tech_support",
    target_node="upf-01",
    upload_to_cxd="<TAC_CASE_NUMBER>",
)
print(result.upload_status)
```

This sends files without a separate manual inspection step. Prefer post-run
upload when the content needs review first.

## Authentication and Failures

The integration can require an OIDC user SSO session; certificate-authenticated
sessions can be rejected. Case permissions, network access, and RADKit setup
also affect upload success. See [authentication troubleshooting](../troubleshooting/oidc-cxd.md).

Check `UploadResult.status` and `error_message` or `result.upload_status`.
Upload failure does not invalidate successfully collected local files or erase
them. The native-wheel StarOS pilots did not test TAC upload.
