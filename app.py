import os
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import AzureOpenAI
import httpx

# Load environment variables
load_dotenv()

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Azure OpenAI configuration with error handling
try:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
    api_version = "2023-12-01-preview"
    
    if not all([endpoint, api_key, deployment]):
        raise ValueError("Missing required Azure OpenAI configuration")
        
    logger.info("Successfully loaded Azure OpenAI configuration")
except KeyError as e:
    logger.error(f"Missing environment variable: {str(e)}")
    raise
except Exception as e:
    logger.error(f"Error in configuration: {str(e)}")
    raise

# Initialize Azure OpenAI client with proper error handling
try:
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )
    logger.info("Successfully initialized Azure OpenAI client")
except Exception as e:
    logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
    raise

# System message to define chatbot personality and expertise
SYSTEM_MESSAGE = """
You are an expert Azure consultant and architect with extensive experience in Azure cloud solutions.
You can provide detailed guidance on:
- Azure architecture best practices
- Cost optimization strategies
- Security and compliance in Azure
- Migration planning and execution
- Infrastructure as Code (IaC) implementation
- Azure services selection and configuration
- Performance optimization
- High availability and disaster recovery planning

Provide clear, concise, and practical advice based on current Azure best practices.
"""

# Rest of your code (routes, etc.)...

# Add health check endpoint
@app.route('/health')
def health_check():
    try:
        # Basic API test
        client.chat.completions.create(
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1,
            model=deployment
        )
        return jsonify({"status": "healthy", "message": "Azure OpenAI connection successful"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "message": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_message = data.get('message')
        chat_history = data.get('history', [])
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Prepare messages for the API call
        messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_message})
        
        # Call Azure OpenAI with timeout handling
        response = client.chat.completions.create(
            messages=messages,
            temperature=0.7,
            max_tokens=800,
            model=deployment,
            timeout=30  # Add timeout
        )
        
        assistant_message = response.choices[0].message.content
        
        return jsonify({
            "response": assistant_message,
            "newMessage": {"role": "assistant", "content": assistant_message}
        })
        
    except httpx.TimeoutException:
        logger.error("Request to Azure OpenAI timed out")
        return jsonify({"error": "Request timed out"}), 504
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)