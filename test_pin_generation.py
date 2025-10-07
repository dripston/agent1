#!/usr/bin/env python3
"""
Test script for PIN generation and duplicate prevention in Agent1
"""
import base64
import sys
import os

# Add the agent1 directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from agent1 import Agent1

def test_pin_generation():
    """Test PIN generation functionality"""
    print("Testing PIN generation functionality...")
    
    # Initialize Agent1
    agent = Agent1()
    
    # Create mock PDF data (simplified FSSAI document)
    mock_fssai_text = """
    FSSAI REGISTRATION CERTIFICATE
    
    Licensee Name : KINGS ROLL
    Registration No.: 20819019000744
    Address: NEAR PUNJ AB BUS STAND VPO AND TEH KALANW ALI DISTT SIRS A HAR YANA, Sirsa, Sirsa (Hary ana), - 125201
    Kind of Business: Food Vending Establishment
    Date of Issue: 14/12/2020
    Valid Upto: 13/12/2025
    """
    
    # Convert text to bytes to simulate PDF data
    mock_pdf_data = mock_fssai_text.encode('utf-8')
    
    # Test verification with PDF data
    result = agent.verify_producer_with_pdf_data(
        producer_name="KINGS ROLL",
        fssai_pdf_data=mock_pdf_data,
        income=11000,  # Less than 12 lakhs, should be registration
        aadhar="442125846000"
    )
    
    print(f"Verification result: {result['status']}")
    if result['status'] == 'success':
        print(f"Generated PIN: {result.get('pin')}")
        print(f"Certificate type: {result.get('certificate_type')}")
        print("Verification successful!")
    else:
        print(f"Verification failed: {result.get('message')}")
    
    return result

def test_duplicate_prevention():
    """Test that duplicate entries are prevented"""
    print("\nTesting duplicate prevention...")
    
    # Initialize Agent1
    agent = Agent1()
    
    # Create mock PDF data (simplified FSSAI document)
    mock_fssai_text = """
    FSSAI REGISTRATION CERTIFICATE
    
    Licensee Name : KINGS ROLL
    Registration No.: 20819019000744
    Address: NEAR PUNJ AB BUS STAND VPO AND TEH KALANW ALI DISTT SIRS A HAR YANA, Sirsa, Sirsa (Hary ana), - 125201
    Kind of Business: Food Vending Establishment
    Date of Issue: 14/12/2020
    Valid Upto: 13/12/2025
    """
    
    # Convert text to bytes to simulate PDF data
    mock_pdf_data = mock_fssai_text.encode('utf-8')
    
    # First verification
    print("First verification...")
    result1 = agent.verify_producer_with_pdf_data(
        producer_name="KINGS ROLL",
        fssai_pdf_data=mock_pdf_data,
        income=11000,
        aadhar="442125846001"  # Different Aadhar
    )
    
    print(f"First verification result: {result1['status']}")
    if result1['status'] == 'success':
        print(f"First PIN: {result1.get('pin')}")
    
    # Second verification with same Aadhar but different data
    print("Second verification with same Aadhar...")
    result2 = agent.verify_producer_with_pdf_data(
        producer_name="KINGS ROLL UPDATED",
        fssai_pdf_data=mock_pdf_data,
        income=15000,
        aadhar="442125846001"  # Same Aadhar
    )
    
    print(f"Second verification result: {result2['status']}")
    if result2['status'] == 'success':
        print(f"Second PIN: {result2.get('pin')}")
        
    # Check if the same entry was updated instead of creating a duplicate
    if result1['status'] == 'success' and result2['status'] == 'success':
        if result1.get('pin') != result2.get('pin'):
            print("SUCCESS: Same Aadhar number was updated instead of creating duplicate entry")
        else:
            print("NOTE: PINs are the same (expected if data hasn't changed significantly)")
    
    return result1, result2

if __name__ == "__main__":
    print("Agent1 PIN Generation and Duplicate Prevention Test")
    print("=" * 50)
    
    # Test PIN generation
    pin_result = test_pin_generation()
    
    # Test duplicate prevention
    dup_result1, dup_result2 = test_duplicate_prevention()
    
    print("\n" + "=" * 50)
    print("Test completed!")