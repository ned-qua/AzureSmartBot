# Azure OpenAI Chat Application

## Overview
This application is a Flask-based web service that integrates with Azure OpenAI to provide AI consulting services. It offers expert guidance on Azure architecture, cost optimization, security, and best practices.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Local Development](#local-development)
- [Deployment](#deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites
- Python 3.10 or higher
- Azure subscription
- Azure OpenAI service instance
- GitHub account
- Azure Web App Service

## Project Structure
```tree
AzureSmartBot/
├── .github/
│   └── workflows/
│       └── main_webappservice.yml
├── templates/
│   └── index.html
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

## Configuration

### Environment Variables
Create a `.env` file for local development:

```ini name=.env.example
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
PORT=8000
```

### Azure App Service Configuration
Add these settings in Azure Portal > App Service > Configuration > Application settings:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `WEBSITES_CONTAINER_START_TIME_LIMIT=600`
- `PORT=8000`

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Curious4Tech/AzureSmartBot.git
cd AzureSmartBot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your values
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:8000`

## Deployment

### Manual Deployment
1. Create an Azure Web App Service
2. Configure application settings in Azure Portal
3. Deploy using VS Code Azure Tools or Azure CLI

### Startup Command
Set in Azure Portal > Configuration > General settings:
```bash
gunicorn --workers=2 --timeout=120 --access-logfile="-" --error-logfile="-" --bind=0.0.0.0:8000 app:app
```

## CI/CD Pipeline

### GitHub Actions Workflow
Use the azure portal to configure it by authenticating to your github account and choosing your repo, then Azure  will provide a default  workflow that will is enough for this demo but you can also costumize your workflows.


### Setting up GitHub Actions ( Optional for this demo, if you choose to write your own workflows)

1. In Azure Portal:
   - Go to your Web App
   - Download publish profile
   - Copy the content

2. In GitHub:
   - Go to repository settings
   - Add new secret `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Paste the publish profile content

3. Update workflow file:
   - Replace `your-webapp-name` with your actual Azure Web App name

## Monitoring and Maintenance

### Health Check Endpoint
The application includes a health check endpoint at `/health` that verifies:
- Application status
- Azure OpenAI connection

### Logging
- Application logs available in Azure Portal
- Structured logging format:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Azure Monitor Integration
1. Enable Application Insights in Azure Portal
2. Monitor:
   - Response times
   - Failed requests
   - Server errors
   - Container logs

## Troubleshooting

### Common Issues and Solutions

1. Container Startup Issues:
```
Solution: Check startup command and environment variables in Azure Portal
```

2. OpenAI Client Errors:
```
Solution: Verify Azure OpenAI credentials and endpoint configuration
```

3. Connection Timeouts:
```
Solution: Adjust timeout settings in startup command or check network configuration
```

### Key Files

#### app.py
Main application file containing:
- Flask application setup
- Azure OpenAI client initialization
- API endpoints
- Error handling

```python
# Key components
- Flask application initialization
- Azure OpenAI client setup
- System message configuration
- API endpoints for chat and health check
```

#### requirements.txt
```text name=requirements.txt
flask>=2.0.0
python-dotenv>=1.0.0
openai>=1.0.0
gunicorn>=20.1.0
httpx>=0.24.0
```

## Security Considerations

1. Environment Variables:
   - Never commit sensitive data
   - Use Azure Key Vault for production secrets

2. API Security:
   - Rate limiting implemented
   - Input validation on all endpoints
   - Error handling to prevent information disclosure

3. Deployment Security:
   - HTTPS enabled
   - Secure configuration in Azure App Service

## Support and Contact

For issues or questions:
1. Check Azure App Service logs
2. Review GitHub Actions workflow runs
3. Contact system administrator

T
