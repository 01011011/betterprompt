# GitHub Workflows Setup Guide

This repository now has three separate GitHub Actions workflows for different purposes:

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
- **Purpose**: Automatic deployment to Azure Container Instance
- **Duration**: ~5-8 minutes
- **Actions**:
  - Run tests
  - Build Docker image
  - Push to Azure Container Registry
  - Deploy to Azure Container Instance
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

## 🔑 Required GitHub Secrets

To enable the Azure deployment workflow, you need to configure these secrets in your GitHub repository:

### Azure Authentication
```
AZURE_CREDENTIALS          # Service principal JSON for Azure login
AZURE_RESOURCE_GROUP        # Azure resource group name
AZURE_LOCATION             # Azure region (e.g., "East US", "West US 2")
```

### Azure Container Registry
```
AZURE_REGISTRY_LOGIN_SERVER # Your ACR login server (e.g., myregistry.azurecr.io)
AZURE_REGISTRY_USERNAME     # ACR username (usually service principal ID)
AZURE_REGISTRY_PASSWORD     # ACR password (service principal secret)
```

### Application Environment Variables
```
AZURE_OPENAI_ENDPOINT       # Your Azure OpenAI endpoint URL
AZURE_OPENAI_API_KEY        # Your Azure OpenAI API key
```

## 🛠️ Setting Up Azure Credentials

### 1. Create a Service Principal

```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "github-actions-betterprompt" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

Copy the JSON output and add it as the `AZURE_CREDENTIALS` secret.

### 2. Create Azure Container Registry (if needed)

```bash
# Create ACR
az acr create \
  --name betterpromptregistry \
  --resource-group your-resource-group \
  --sku Basic \
  --location "East US"

# Get ACR credentials
az acr credential show --name betterpromptregistry
```

### 3. Configure GitHub Secrets

1. Go to your repository on GitHub
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
