#!/usr/bin/env python3
"""
Test script for Agent1 Web API
"""
import requests
import base64
import json

# API endpoint (adjust as needed for your deployment)
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_verify_producer():
    """Test the producer verification endpoint"""
    print("Testing producer verification endpoint...")
    
    # Read a sample PDF file and encode it as base64
    # Replace 'sample_fssai.pdf' with an actual FSSAI certificate PDF file
    try:
        with open("sample_fssai.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
            pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
    except FileNotFoundError:
        print("Sample PDF file not found. Creating a mock request...")
        pdf_base64 = "JVBERi0xLjQKJcOkw7zDtsO"  # Mock base64 data
    
    # Prepare the request data
    data = {
        "aadhar": "123456789012",
        "name": "Sample Business Name",
        "fssai_pdf": pdf_base64,
        "annual_income": 1000000
    }
    
    # Send the request
    response = requests.post(f"{API_BASE_URL}/verify", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_producer(aadhar):
    """Test getting producer by Aadhar number"""
    print(f"Testing get producer by Aadhar: {aadhar}...")
    response = requests.get(f"{API_BASE_URL}/producers/{aadhar}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_all_producers():
    """Test getting all producers"""
    print("Testing get all producers...")
    response = requests.get(f"{API_BASE_URL}/producers")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("Agent1 Web API Test Script")
    print("=" * 30)
    
    # Test health check
    test_health_check()
    
    # Test producer verification
    test_verify_producer()
    
    # Test get producer by Aadhar
    test_get_producer("123456789012")
    
    # Test get all producers
    test_get_all_producers()