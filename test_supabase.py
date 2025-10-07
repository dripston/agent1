import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def test_supabase_connection():
    """Test Supabase connection and table structure"""
    try:
        # Test connection by getting table info
        print("Testing Supabase connection...")
        
        # Try to insert a simple test record to check if PIN column exists
        test_data = {
            "aadhar": "TEST1234567890",
            "name": "Test User",
            "fssai_license_number": "12345678901234",
            "annual_income": 500000,
            "certificate_type": "registration",
            "business_type": "Test Business",
            "issue_date": "01/01/2020",
            "expiry_date": "01/01/2025",
            "address": "Test Address",
            "pin": 123456  # Test PIN
        }
        
        print("Attempting to insert test data with PIN...")
        result = supabase.table("verified_producers").upsert(test_data).execute()
        print("Insert successful!")
        print(f"Result: {result}")
        
        # Now try to retrieve the data
        print("Retrieving test data...")
        select_result = supabase.table('verified_producers').select('*').eq('aadhar', 'TEST1234567890').execute()
        if select_result.data:
            print("Data retrieved successfully:")
            print(select_result.data[0])
        else:
            print("No data found")
            
        # Clean up test data
        print("Cleaning up test data...")
        supabase.table('verified_producers').delete().eq('aadhar', 'TEST1234567890').execute()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_supabase_connection()