# GitHub Secrets Configuration

This document outlines the GitHub secrets required for the automated CI/CD workflows using modern OpenID Connect (OIDC) federated identity.

## Required Secrets

The following secrets need to be configured in your GitHub repository settings:

### Azure Authentication (OIDC Federated Identity)

- `AZURE_CLIENT_ID` - Application (client) ID of the Azure AD app registration
- `AZURE_TENANT_ID` - Directory (tenant) ID of your Azure AD tenant  
- `AZURE_SUBSCRIPTION_ID` - Your Azure subscription ID

### Azure Resources

- `AZURE_RESOURCE_GROUP` - Name of the Azure resource group (e.g., `betterprompt-rg`)
- `AZURE_CONTAINER_INSTANCE_NAME` - Name of the Azure Container Instance (e.g., `betterprompt-container`)

### Application Configuration

- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI service endpoint
- `AZURE_OPENAI_API_KEY` - API key for Azure OpenAI service

## Current Configuration Values

Based on the setup completed on June 10, 2025:

```text
AZURE_CLIENT_ID: c7c3fceb-a5ae-457d-b9c5-c11bbafd7e22
AZURE_TENANT_ID: 16b3c013-d300-468d-ac64-7eda0820b6d3
AZURE_SUBSCRIPTION_ID: e930349d-9137-4a7f-af1c-d1cb2221555b
AZURE_RESOURCE_GROUP: betterprompt-rg
AZURE_CONTAINER_INSTANCE_NAME: betterprompt-container
```

## How to Set Up Secrets

1. Navigate to your GitHub repository: <https://github.com/01011011/betterprompt>
2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret" for each secret listed above
4. Enter the secret name and value from the configuration above

## OIDC Federated Identity Setup

We've configured federated identity credentials that eliminate the need for long-lived secrets:

- **Main Branch**: `repo:01011011/betterprompt:ref:refs/heads/main`
- **Pull Requests**: `repo:01011011/betterprompt:pull_request`

This approach is more secure as it uses short-lived tokens instead of permanent secrets.

## Security Advantages

- **No Long-lived Secrets**: Uses temporary tokens that expire quickly
- **Policy Compliant**: Bypasses organizational credential lifetime policies
- **Principle of Least Privilege**: Scoped to specific repository and branches
- **Audit Trail**: All authentication is logged and traceable

## Getting Other Values

- **Subscription ID**: `az account show --query id --output tsv`
- **Tenant ID**: `az account show --query tenantId --output tsv` 
- **Resource Group**: The name you created (e.g., `betterprompt-rg`)
- **Container Instance**: The name you used (e.g., `betterprompt-container`)

## Security Notes

- Federated identity eliminates the need for rotating client secrets
- Monitor authentication events in Azure AD logs
- Review federated credential configurations periodically
- Ensure repository access is properly controlled
