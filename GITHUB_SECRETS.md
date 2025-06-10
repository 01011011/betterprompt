# GitHub Secrets Configuration Guide

## 🔑 Required Secrets for Azure Container Instance Deployment

To enable the Azure deployment workflow, you need to configure these secrets in your GitHub repository:

### **Step 1: Go to Repository Settings**
1. Navigate to: https://github.com/01011011/betterprompt
2. Click **Settings** tab
3. Go to **Secrets and variables** → **Actions**
4. Click **New repository secret**

### **Step 2: Add Required Secrets**

#### **Azure Authentication**
```
Secret Name: AZURE_CREDENTIALS
Secret Value: {
  "clientId": "your-service-principal-client-id",
  "clientSecret": "your-service-principal-secret", 
  "subscriptionId": "your-azure-subscription-id",
  "tenantId": "your-azure-tenant-id"
}
```

#### **Azure Resource Configuration**
```
Secret Name: AZURE_RESOURCE_GROUP
Secret Value: your-resource-group-name

Secret Name: AZURE_LOCATION  
Secret Value: East US
(or your preferred Azure region)
```

#### **Azure Container Registry**
```
Secret Name: AZURE_REGISTRY_LOGIN_SERVER
Secret Value: youracr.azurecr.io

Secret Name: AZURE_REGISTRY_USERNAME
Secret Value: your-acr-username

Secret Name: AZURE_REGISTRY_PASSWORD
Secret Value: your-acr-password
```

#### **Azure OpenAI Configuration**
```
Secret Name: AZURE_OPENAI_ENDPOINT
Secret Value: https://your-resource.openai.azure.com/

Secret Name: AZURE_OPENAI_API_KEY
Secret Value: your-azure-openai-api-key
```

## 🛠️ How to Get These Values

### **1. Create Service Principal for GitHub Actions**
```bash
# Login to Azure
az login

# Create service principal (replace with your subscription and resource group)
az ad sp create-for-rbac \
  --name "github-actions-betterprompt" \
  --role contributor \
  --scopes /subscriptions/{your-subscription-id}/resourceGroups/{your-resource-group} \
  --sdk-auth
```

Copy the entire JSON output and use it as the `AZURE_CREDENTIALS` secret.

### **2. Get Azure Container Registry Details**
```bash
# Create ACR if you don't have one
az acr create \
  --name youracr \
  --resource-group your-resource-group \
  --sku Basic \
  --admin-enabled true

# Get ACR login server
az acr show --name youracr --query loginServer --output tsv

# Get ACR credentials
az acr credential show --name youracr
```

### **3. Get Azure OpenAI Details**
- **Endpoint**: Found in Azure Portal → Your OpenAI Resource → Keys and Endpoint
- **API Key**: Found in Azure Portal → Your OpenAI Resource → Keys and Endpoint

### **4. Resource Group and Location**
```bash
# List your resource groups
az group list --query "[].{Name:name, Location:location}" --output table

# Choose your preferred location
az account list-locations --query "[].{Name:name, DisplayName:displayName}" --output table
```

## 🚨 Current Workflow Status

### **Working Workflows:**
- ✅ **Quick Tests**: Runs on every push/PR (no secrets needed)
- ✅ **CI/CD Pipeline**: Manual trigger only (comprehensive testing)

### **Azure Deployment Workflow:**
❌ **Currently failing** due to missing secrets
✅ **Will work** once you configure the secrets above

## 🎯 Next Steps

1. **Configure all secrets** using the guide above
2. **Test the deployment** by pushing a small change
3. **Monitor the workflow** in GitHub Actions tab
4. **Check your Azure Container Instance** after successful deployment

## 🔍 Troubleshooting

### Common Issues:
- **"Secret not found"**: Double-check secret names (case-sensitive)
- **Azure login failed**: Verify service principal has correct permissions
- **ACR push failed**: Ensure ACR admin is enabled and credentials are correct
- **Container creation failed**: Check resource group exists and location is valid

### Debug Commands:
```bash
# Test Azure CLI login locally
az login --service-principal -u CLIENT_ID -p CLIENT_SECRET --tenant TENANT_ID

# Test ACR access
az acr login --name youracr

# List container instances
az container list --resource-group your-resource-group --output table
```

## 📱 Expected Results

Once configured, the workflow will:
1. ✅ Run tests automatically 
2. 🔨 Build Docker image
3. 📤 Push to Azure Container Registry  
4. 🚀 Deploy to Azure Container Instance
5. 🔍 Perform health checks
6. 🧹 Clean up old deployments
7. 📋 Provide deployment URL in workflow logs

Your app will be accessible at:
`http://betterprompt-{run-number}.{region}.azurecontainer.io:5000`
