# Deployment Guide

This guide covers various deployment options for BetterPrompt.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployments](#cloud-deployments)
  - [Azure Container Instances](#azure-container-instances)
  - [Azure App Service](#azure-app-service)
  - [AWS ECS](#aws-ecs)
  - [Google Cloud Run](#google-cloud-run)
  - [Heroku](#heroku)

## Local Development

```bash
# Clone repository
git clone <repository-url>
cd betterprompt

# Set up virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Run application
python app.py
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker Commands

```bash
# Build image
docker build -t betterprompt:latest .

# Run container
docker run -d \
  --name betterprompt-app \
  -p 5000:5000 \
  --env-file .env \
  --restart unless-stopped \
  betterprompt:latest

# Check logs
docker logs betterprompt-app

# Stop container
docker stop betterprompt-app
docker rm betterprompt-app
```

## Cloud Deployments

### Azure Container Instances

1. **Build and push to Azure Container Registry**
   ```bash
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name betterprompt-rg --location eastus
   
   # Create container registry
   az acr create --resource-group betterprompt-rg --name betterpromptacr --sku Basic
   
   # Login to ACR
   az acr login --name betterpromptacr
   
   # Build and push
   docker build -t betterpromptacr.azurecr.io/betterprompt:latest .
   docker push betterpromptacr.azurecr.io/betterprompt:latest
   ```

2. **Deploy to Container Instances**
   ```bash
   az container create \
     --resource-group betterprompt-rg \
     --name betterprompt-app \
     --image betterpromptacr.azurecr.io/betterprompt:latest \
     --dns-name-label betterprompt-unique \
     --ports 5000 \
     --environment-variables \
       AZURE_OPENAI_ENDPOINT="your-endpoint" \
       AZURE_OPENAI_API_KEY="your-key"
   ```

### Azure App Service

1. **Create App Service Plan**
   ```bash
   az appservice plan create \
     --name betterprompt-plan \
     --resource-group betterprompt-rg \
     --sku B1 \
     --is-linux
   ```

2. **Create Web App**
   ```bash
   az webapp create \
     --resource-group betterprompt-rg \
     --plan betterprompt-plan \
     --name betterprompt-app \
     --deployment-container-image-name betterpromptacr.azurecr.io/betterprompt:latest
   ```

3. **Configure Environment Variables**
   ```bash
   az webapp config appsettings set \
     --resource-group betterprompt-rg \
     --name betterprompt-app \
     --settings \
       AZURE_OPENAI_ENDPOINT="your-endpoint" \
       AZURE_OPENAI_API_KEY="your-key"
   ```

### AWS ECS

1. **Create ECR repository**
   ```bash
   aws ecr create-repository --repository-name betterprompt
   ```

2. **Build and push to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker build -t betterprompt .
   docker tag betterprompt:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/betterprompt:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/betterprompt:latest
   ```

3. **Deploy using ECS Fargate** (use AWS Console or CLI)

### Google Cloud Run

1. **Build and push to Google Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/betterprompt
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy betterprompt \
     --image gcr.io/PROJECT-ID/betterprompt \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars AZURE_OPENAI_ENDPOINT="your-endpoint",AZURE_OPENAI_API_KEY="your-key"
   ```

### Heroku

1. **Install Heroku CLI and login**
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create betterprompt-app
   ```

3. **Set environment variables**
   ```bash
   heroku config:set AZURE_OPENAI_ENDPOINT="your-endpoint"
   heroku config:set AZURE_OPENAI_API_KEY="your-key"
   ```

4. **Deploy using container registry**
   ```bash
   heroku container:login
   heroku container:push web
   heroku container:release web
   ```

## Environment Variables

Make sure to set these environment variables in your deployment:

- `AZURE_OPENAI_ENDPOINT` (required)
- `AZURE_OPENAI_API_KEY` (required)
- `SECRET_KEY` (recommended for production)
- `FLASK_ENV=production` (for production deployments)

## Health Checks

All deployments should configure health checks using the `/health` endpoint:

```bash
curl http://your-app-url/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "BetterPrompt"
}
```

## SSL/TLS

For production deployments, ensure SSL/TLS is enabled:
- Use cloud provider's built-in SSL/TLS options
- Configure reverse proxy (nginx) with SSL certificates
- Use services like Cloudflare for additional security

## Monitoring

Consider setting up monitoring for:
- Application health (`/health` endpoint)
- Response times
- Error rates
- Resource usage
- Azure OpenAI API usage and costs

## Scaling

For high-traffic deployments:
- Use multiple container instances
- Configure auto-scaling based on CPU/memory
- Implement rate limiting
- Consider caching strategies
- Monitor Azure OpenAI rate limits
