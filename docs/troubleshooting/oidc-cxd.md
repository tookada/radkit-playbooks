# Authentication and TAC Upload

An authenticated RADKit device session does not automatically grant permission
to upload files to a TAC case.

The CXD integration can reject certificate-authenticated sessions with an OIDC
SSO requirement. Follow the [RADKit documentation](https://radkit.cisco.com/) for
the supported user SSO flow and confirm that the connected service uses the
intended client session. Do not paste credentials, tokens, or authorization URLs
into this repository or issue reports.

Also verify case authorization and required network access. Successful SSO alone
does not guarantee upload success.

Inspect the upload result and its error message. Successfully collected local
files remain available if upload fails. Once approved, use `pb.upload()` to retry
from saved files rather than regenerating diagnostics unnecessarily, or use an
authorized manual support-case upload process.

See [optional TAC upload](../user-guide/cxd-upload.md) for API examples.
