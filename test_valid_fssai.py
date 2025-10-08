#!/usr/bin/env python3
"""
Test script for Agent1 Web API with a valid FSSAI document
"""
import requests
import base64
import json

# API endpoint (Render deployment)
API_BASE_URL = "https://agent1-v0he.onrender.com"

def test_verify_with_valid_fssai():
    """Test the producer verification endpoint with a valid FSSAI document"""
    print("Testing producer verification endpoint with valid FSSAI document...")
    
    try:
        # Read a real FSSAI certificate PDF
        with open("../442125846-FSSAI-CERTIFICATE-1.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        
        # Prepare the request data
        data = {
            "aadhar": "442125846000",
            "name": "KINgS ROLL",
            "fssai_pdf": pdf_base64,
            "annual_income": 11000
        }
        
        response = requests.post(f"{API_BASE_URL}/verify", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except FileNotFoundError:
        print("FSSAI certificate file not found. Skipping this test.")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("Agent1 Web API Test Script with Valid FSSAI Document")
    print("=" * 50)
    
    # Test producer verification with valid FSSAI document
    test_verify_with_valid_fssai()