# Azure DevOps MCP templates

These are reviewed templates, not active configuration.

- `remote-readonly.mcp.json.example` uses the official hosted service, selected toolsets, and the
  server-enforced read-only header.
- `remote-write-enabled.mcp.json.example` exposes write operations in those toolsets and must be
  paired with a least-privilege identity and explicit mutation confirmation.

Replace `{organization}` locally. Do not commit credentials or tokens. Copy only the chosen server
entry into the configuration format supported by the target runtime.
