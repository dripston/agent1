#!/usr/bin/env python3
"""
Test script for Agent1 Web API endpoints
"""
import requests
import base64
import json

# API endpoint (Render deployment)
API_BASE_URL = "https://agent1-v0he.onrender.com"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_verify_endpoint():
    """Test the producer verification endpoint with mock data"""
    print("Testing producer verification endpoint...")
    
    # Create simple mock PDF data as base64
    pdf_base64 = "JVBERi0xLjQKJcOkw7zDtsOfCjEgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDIgMCBSCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9UeXBlIC9QYWdlcwovS2lkcyBbMyAwIFJdCi9Db3VudCAxCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgMiAwIFIKL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KL0NvbnRlbnRzIDQgMCBSCi9SZXNvdXJjZXMgPDwKL1Byb2NTZXQgWy9QREYgL1RleHRdCi9Gb250IDw8Ci9GMSA1IDAgUgo+Pgo+Pgo+PgplbmRvYmoKNCAwIG9iago8PAovTGVuZ3RoIDQ0Cj4+CnN0cmVhbQpCVAovRjEgMTIgVGYKNzIgNzIwIFRkCihIZWxsbywgdGhpcyBpcyBhIG1vY2sgRlNTQUkgZG9jdW1lbnQuKSBUagogRVQKZW5kc3RyZWFtCmVuZG9iago1IDAgb2JqCjw8Ci9UeXBlIC9Gb250Ci9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYQo+PgplbmRvYmoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDAwNjAgMDAwMDAgbiAKMDAwMDAwMDExMSAwMDAwMCBuIAowMDAwMDAwMjM5IDAwMDAwIG4gCjAwMDAwMDAzNTYgMDAwMDAgbiAKdHJhaWxlcgo8PAovU2l6ZSA2Ci9Sb290IDEgMCBSCj4+CnN0YXJ0eHJlZgo0MTYKJSVFT0Y="

    # Prepare the request data
    data = {
        "aadhar": "123456789012",
        "name": "Test Business",
        "fssai_pdf": pdf_base64,
        "annual_income": 1000000
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/verify", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_get_all_producers():
    """Test getting all producers"""
    print("Testing get all producers endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/producers")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("Agent1 Web API Test Script")
    print("=" * 30)
    
    # Test root endpoint
    test_root_endpoint()
    
    # Test health check
    test_health_endpoint()
    
    # Test producer verification
    test_verify_endpoint()
    
    # Test get all producers
    test_get_all_producers()