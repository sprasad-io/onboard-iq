# test_azure.py
# Diagnostic script to isolate the exact Azure 404 routing error

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load variables from .env file
load_dotenv()

print("=== STEP 1: VERIFYING ENV VARIABLES ===")
print(f"Target Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"Deployment Name: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
print(f"API Key Present: {'Yes' if os.getenv('AZURE_OPENAI_KEY') else 'No'}")

# Initialize client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-06-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

print("\n=== STEP 2: TESTING AZURE HANDSHAKE ===")
try:
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": "Ping"}],
        max_tokens=5
    )
    print("🎯 SUCCESS! Azure connected perfectly.")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print("❌ CONNECTION FAILED!")
    print(f"Exact Error Log: {str(e)}")