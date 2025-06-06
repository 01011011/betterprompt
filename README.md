# BetterPrompt 🚀

A modern, responsive Flask web application that transforms rough or poorly structured prompts into well-formatted, clear, and effective prompts using Azure OpenAI's o1-mini model.

![BetterPrompt](https://img.shields.io/badge/Flask-3.0.0-blue.svg)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-o1--mini-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **🤖 AI-Powered Optimization**: Uses Azure OpenAI o1-mini model for intelligent prompt enhancement
- **📱 Responsive Design**: Beautiful, modern UI that works perfectly on desktop and mobile
- **⚡ Fast & Efficient**: Optimized performance with caching and efficient API calls
- **📋 Copy Functionality**: One-click copying of optimized prompts with visual feedback
- **⌨️ Keyboard Shortcuts**: 
  - `Ctrl+Enter` to submit prompts
  - `Ctrl+C` to copy results when visible
- **🛡️ Security**: Input validation, environment variable protection, and secure deployment
- **🔧 Error Handling**: Comprehensive error handling with user-friendly messages
- **🐳 Dockerized**: Ready for containerization and deployment
- **♿ Accessibility**: WCAG-compliant with proper ARIA labels and keyboard navigation
- **🌙 Dark Mode**: Automatic dark mode support based on system preferences

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ 
- Azure OpenAI account with o1-mini model access
- Git (optional)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd betterprompt
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   
   # Edit .env with your Azure OpenAI credentials
   ```

5. **Set up your Azure OpenAI credentials**
   
   Edit the `.env` file:
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/openai/deployments/your-deployment-name/chat/completions?api-version=2024-02-15-preview
   AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

### 🐳 Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t betterprompt .
   docker run -p 5000:5000 --env-file .env betterprompt
   ```

3. **Access the application**
   Navigate to `http://localhost:5000`

## 🏗️ Project Structure

```
betterprompt/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── start.sh              # Production startup script
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── test_app.py          # Unit tests
├── templates/
│   └── index.html       # Main HTML template
└── static/
    ├── css/
    │   └── style.css    # Stylesheet with responsive design
    ├── js/
    │   └── app.js       # JavaScript functionality
    └── favicon.ico      # Favicon
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL | - | ✅ |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | - | ✅ |
| `SECRET_KEY` | Flask secret key for sessions | `dev-key` | ⚠️ |
| `FLASK_DEBUG` | Enable debug mode | `False` | ❌ |
| `MODEL_NAME` | OpenAI model to use | `o1-mini` | ❌ |
| `MAX_COMPLETION_TOKENS` | Maximum response length | `2048` | ❌ |
| `REQUEST_TIMEOUT` | API request timeout (seconds) | `30` | ❌ |
| `PORT` | Application port | `5000` | ❌ |

### Azure OpenAI Setup

1. **Create an Azure OpenAI resource** in the Azure portal
2. **Deploy the o1-mini model** in Azure OpenAI Studio
3. **Get your endpoint and API key** from the Azure portal
4. **Update the `.env` file** with your credentials

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-mock pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

## 🚢 Deployment

### Docker Production Deployment

1. **Build the production image**
   ```bash
   docker build -t betterprompt:latest .
   ```

2. **Run with environment file**
   ```bash
   docker run -d \
     --name betterprompt-app \
     -p 5000:5000 \
     --env-file .env \
     --restart unless-stopped \
     betterprompt:latest
   ```

### Cloud Deployment

The application is ready for deployment on:
- **Azure Container Instances**
- **Azure App Service**
- **AWS ECS**
- **Google Cloud Run**
- **Heroku**
- **DigitalOcean App Platform**

## 📊 API Reference

### POST `/api/fix-prompt`

Optimize a prompt using Azure OpenAI.

**Request Body:**
```json
{
  "prompt": "write me something about dogs"
}
```

**Response:**
```json
{
  "improved_prompt": "Write a comprehensive article about dogs that covers their history as companions to humans, different breeds and their characteristics, basic care requirements, and the benefits of dog ownership. Include specific examples and organize the content with clear headings for easy reading."
}
```

**Error Response:**
```json
{
  "error": "Error message description"
}
```

### GET `/health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "BetterPrompt"
}
```

## 🛡️ Security

- **Input validation** and length limits
- **Environment variable protection**
- **Non-root Docker user**
- **Security headers** and best practices
- **Rate limiting** ready (add nginx/cloudflare)
- **HTTPS ready** (configure reverse proxy)

## 🎨 UI Features

- **Responsive grid layout** that adapts to screen size
- **Two-column layout** on desktop for side-by-side comparison
- **Modern glassmorphism design** with gradients and backdrop blur
- **Smooth animations** and transitions
- **Copy-to-clipboard** functionality with visual feedback
- **Loading states** and error handling
- **Keyboard accessibility** and screen reader support
- **Dark mode support** based on system preferences

## 🔄 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. **Check the logs** for error messages
2. **Verify your environment variables** are correctly set
3. **Ensure your Azure OpenAI model** is deployed and accessible
4. **Check the health endpoint** at `/health`
5. **Open an issue** on GitHub with details

## 🙏 Acknowledgments

- **Azure OpenAI** for providing the o1-mini model
- **Flask** community for the excellent web framework
- **Microsoft** for Azure cloud services
- **Contributors** and the open-source community

---

Made with ❤️ by [Your Name]

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Environment Configuration

Create a `.env` file based on `.env.example`:

```env
# Required
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2024-02-15-preview
AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here

# Optional
SECRET_KEY=your-secret-key-for-production
FLASK_DEBUG=false
PORT=5000
MODEL_NAME=o1-mini
MAX_COMPLETION_TOKENS=2048
REQUEST_TIMEOUT=30
```

### Azure OpenAI Setup

1. Create an Azure OpenAI resource in the Azure portal
2. Deploy the o1-mini model
3. Get your endpoint URL and API key
4. Update the `.env` file with your credentials

## Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t betterprompt .

# Run the container
docker run -p 5000:5000 --env-file .env betterprompt
```

### Using Docker Compose

```bash
docker-compose up
```

## API Documentation

### POST /api/fix-prompt

Optimize a prompt using AI.

**Request Body:**
```json
{
  "prompt": "write me something about dogs"
}
```

**Response:**
```json
{
  "improved_prompt": "Write a comprehensive 500-word article about domestic dogs that covers the following aspects:\n\n1. Basic characteristics and behavior\n2. Popular breeds and their traits\n3. Health and care requirements\n4. The human-dog relationship\n\nPlease use an informative yet engaging tone suitable for general readers. Include specific examples and ensure the content is well-structured with clear headings."
}
```

**Error Response:**
```json
{
  "error": "Error description"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "BetterPrompt"
}
```

## Project Structure

```
betterprompt/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Environment variables (create from example)
├── .gitignore           # Git ignore rules
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── README.md            # This file
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Application styles
│   └── js/
│       └── app.js       # Client-side JavaScript
├── templates/           # HTML templates
│   └── index.html       # Main page template
└── tests/
    └── test_app.py      # Unit tests
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

### Code Quality

The application follows Python best practices:

- **Type hints** for better code documentation
- **Error handling** with proper logging
- **Configuration management** using environment variables
- **Security** considerations (input validation, secret management)
- **Modular design** with separation of concerns

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Submit a pull request

## Security Considerations

- **Environment Variables**: Sensitive data is stored in environment variables
- **Input Validation**: User input is validated and sanitized
- **Rate Limiting**: Consider implementing rate limiting for production use
- **HTTPS**: Use HTTPS in production environments
- **Secret Management**: Use proper secret management in production

## Troubleshooting

### Common Issues

1. **Azure API Key Error**
   - Verify your Azure OpenAI endpoint and API key
   - Ensure the o1-mini model is deployed and accessible

2. **Port Already in Use**
   - Change the PORT environment variable
   - Kill existing processes using the port

3. **Module Not Found**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

### Error Messages

- **"Service temporarily unavailable"**: Azure API issues
- **"Request timeout"**: Network connectivity issues
- **"Prompt too long"**: Input exceeds 10,000 character limit

## Performance

- **Response Time**: Typically 2-5 seconds depending on prompt complexity
- **Concurrent Users**: Suitable for small to medium workloads
- **Scalability**: Can be scaled horizontally using load balancers

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support, please:
1. Check the troubleshooting section
2. Review the GitHub issues
3. Create a new issue with detailed information

## Acknowledgments

- Azure OpenAI for providing the o1-mini model
- Flask community for the excellent web framework
- Contributors and testers

---

**Made with ❤️ for better AI prompting**
