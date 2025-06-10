# GitHub Workflows Setup Guide

This repository has three GitHub Actions workflows for different purposes, now using modern OIDC authentication:

## 📋 Workflow Overview

### 1. **Quick Tests** (`quick-tests.yml`)
- **Trigger**: Every push and pull request
- **Purpose**: Fast feedback with basic tests
- **Duration**: ~2-3 minutes
- **Actions**: 
  - Python syntax check
  - Unit tests
  - Basic validation

### 2. **Azure Container Instance Deploy** (`azure-deploy.yml`)
- **Trigger**: Push to `main` branch only
- **Purpose**: Automatic deployment to Azure Container Instance using OIDC
- **Duration**: ~5-8 minutes
- **Actions**:
  - Run tests
  - OIDC authentication to Azure
  - Create Azure Container Instance
  - Health check verification
  - Cleanup old containers

### 3. **Full CI/CD Pipeline** (`ci.yml`)
- **Trigger**: Manual only (`workflow_dispatch`)
- **Purpose**: Comprehensive testing and multi-environment deployment
- **Duration**: ~10-15 minutes
- **Actions**:
  - Multi-Python version testing
  - Security scans
  - Docker build and push
  - Full test coverage
  - Linting and code quality checks

## 🔑 Required GitHub Secrets (OIDC Authentication)

To enable the Azure deployment workflow, configure these secrets in your GitHub repository:

### Azure OIDC Authentication (Modern & Secure)
```
AZURE_CLIENT_ID            # Application (client) ID: c7c3fceb-a5ae-457d-b9c5-c11bbafd7e22
AZURE_TENANT_ID            # Directory (tenant) ID: 16b3c013-d300-468d-ac64-7eda0820b6d3
AZURE_SUBSCRIPTION_ID      # Azure subscription ID: e930349d-9137-4a7f-af1c-d1cb2221555b
AZURE_RESOURCE_GROUP       # Azure resource group name: betterprompt-rg
```
AZURE_REGISTRY_LOGIN_SERVER # Your ACR login server (e.g., myregistry.azurecr.io)
AZURE_REGISTRY_USERNAME     # ACR username (usually service principal ID)
```

### Application Environment Variables
```
AZURE_OPENAI_ENDPOINT       # Your Azure OpenAI endpoint URL
AZURE_OPENAI_API_KEY        # Your Azure OpenAI API key
```

## 🛠️ OIDC Federated Identity Setup (Already Completed)

### ✅ Azure AD Application Configured
- **Application ID**: `c7c3fceb-a5ae-457d-b9c5-c11bbafd7e22`
- **Service Principal**: Created with Contributor role on resource group
- **Federated Credentials**: Configured for GitHub Actions trust relationships

### ✅ Federated Identity Credentials
- **Main Branch**: `repo:01011011/betterprompt:ref:refs/heads/main`
- **Pull Requests**: `repo:01011011/betterprompt:pull_request`

### 🔐 Security Benefits
- **No Client Secrets**: Eliminates long-lived credential storage
- **Policy Compliant**: Bypasses organizational credential lifetime policies
- **Short-lived Tokens**: Automatic token expiration and renewal
- **Scoped Access**: Limited to specific repository and branches

### 3. Configure GitHub Secrets

1. Go to your repository on GitHub: https://github.com/01011011/betterprompt
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret listed above

## 🚀 How It Works

### On Every Push/PR:
1. **Quick Tests** runs automatically
2. Provides fast feedback on code quality
3. Fails fast if basic tests don't pass

### On Push to Main:
1. **Quick Tests** runs first
2. **Azure Deploy** runs if tests pass
3. Automatically deploys to your Azure Container Instance
4. Performs health checks
5. Cleans up old deployments

### Manual Full Pipeline:
1. Go to **Actions** tab in GitHub
2. Select **CI/CD Pipeline (Manual)**
3. Click **Run workflow**
4. Choose environment and options
5. Full comprehensive testing and deployment

## 📱 Accessing Your Deployed App

After successful deployment, the workflow will output:
- **App URL**: `http://{container-name}-{run-number}.{region}.azurecontainer.io:5000`
- **Health Check**: `http://{container-name}-{run-number}.{region}.azurecontainer.io:5000/health`

## 🔧 Customization

### Modify Container Resources
Edit `azure-deploy.yml` to adjust:
```yaml
--cpu 1 \              # CPU cores (0.1 to 4)
--memory 2 \           # Memory in GB (0.1 to 14)
```

### Change Deployment Frequency
- Modify the `paths-ignore` section to exclude certain file changes
- Add conditions to skip deployment for documentation-only changes

### Environment Variables
Add or modify environment variables in the deployment step:
```yaml
--environment-variables \
  AZURE_OPENAI_ENDPOINT=${{ secrets.AZURE_OPENAI_ENDPOINT }} \
  AZURE_OPENAI_API_KEY=${{ secrets.AZURE_OPENAI_API_KEY }} \
  YOUR_NEW_VAR=${{ secrets.YOUR_NEW_VAR }} \
```

## 🐛 Troubleshooting

### Common Issues:

1. **Missing Secrets**: Ensure all required secrets are configured
2. **Azure Permissions**: Service principal needs Contributor role
3. **Container Registry**: Verify ACR credentials and permissions
4. **Resource Group**: Ensure the resource group exists
5. **Port Configuration**: Container must expose port 5000

### Debug Steps:

1. Check workflow logs in GitHub Actions
2. Verify Azure resource group and permissions
3. Test Docker image locally
4. Validate Azure CLI commands manually

## 📈 Monitoring

The workflow includes:
- ✅ Automated health checks
- 🔄 Container restart on failure
- 🧹 Automatic cleanup of old deployments
- 📊 Deployment status reporting

This setup provides a robust, automated deployment pipeline while keeping the comprehensive testing available when needed manually.
