# Azure DevOps MCP integration

Reviewed source: `microsoft/azure-devops-mcp` commit
[`7f2a6b9fae78903682f4c6328cab17986f3f1cc5`](https://github.com/microsoft/azure-devops-mcp/commit/7f2a6b9fae78903682f4c6328cab17986f3f1cc5),
package 2.11.0. Microsoft recommends the hosted remote server when the client supports it.

## Read-only configuration

The remote server's `X-MCP-Readonly: true` header is an enforceable server-side operation filter.
Combine it with `X-MCP-Toolsets` to reduce exposed functionality:

```json
{
  "servers": {
    "ado-remote-mcp": {
      "url": "https://mcp.dev.azure.com/{organization}",
      "type": "http",
      "headers": {
        "X-MCP-Toolsets": "repos,wit,work,pipelines,wiki",
        "X-MCP-Readonly": "true"
      }
    }
  },
  "inputs": []
}
```

The matching template is in `integrations/azure-devops-mcp/remote-readonly.mcp.json.example`.

Read-only tools cover project/team discovery, repositories, branches, pull requests and comments,
builds and logs, work items, queries, backlogs, iterations, capacity, test results, wiki, and search.
The exact catalog can change; inspect the server's advertised tools.

## Write-enabled configuration

Removing the read-only header allows the exposed write tools, including work-item creation and
updates, comments and links, PR creation/review actions, branch creation, pipeline execution, test
plan changes, iteration/capacity changes, and wiki updates.

Use the separate write-enabled template only with:

1. an identity limited by Azure DevOps organization, project, repository, and work-item ACLs;
2. only the needed toolsets or individual tools;
3. human preview/confirmation before mutations; and
4. no token or PAT stored in source control.

Toolsets and individual-tool filters reduce exposed operations but **do not** narrow OAuth scopes,
PAT scope, or Azure DevOps resource ACLs. They are defense in depth, not authorization isolation.

## Authentication boundaries

Remote uses Microsoft Entra OAuth and requires an Entra-backed Azure DevOps organization, project
membership, and resource access. Standalone Microsoft-account-only organizations are unsupported.

The local Node.js 20+ server supports interactive OAuth, Azure CLI credentials,
`DefaultAzureCredential`, a bearer-token environment variable, and a base64-encoded PAT environment
variable. Secrets must stay outside repository files. For Codex, the official local command is:

```text
codex mcp add azure-devops -- npx -y @azure-devops/mcp {organization}
```

Local `-d` domain selection controls registered tools only. It is not read-only authorization, and
invalid or empty domain selection can fall back to all domains. Use a least-privilege identity.

## Current platform state

The templates are packaged but not activated. No MCP configuration, authentication, identity,
permissions, or external service was changed. When Azure DevOps is unavailable, planning and review
skills emit provider-neutral Markdown or JSON and must not claim remote objects were created.
