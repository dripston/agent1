import os
import base64
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def debug_database_issue():
    """Debug the database storage issue"""
    try:
        print("Checking if Aadhar already exists in database...")
        
        # Check if there's already a record with this Aadhar
        # You would need to replace this with the actual Aadhar from your test
        test_aadhar = "ACTUAL_AADHAR_FROM_YOUR_TEST"  # Replace with actual Aadhar
        
        result = supabase.table('verified_producers').select('*').eq('aadhar', test_aadhar).execute()
        
        if result.data:
            print(f"Found existing record with Aadhar {test_aadhar}:")
            print(result.data[0])
        else:
            print(f"No existing record found with Aadhar {test_aadhar}")
            
        # Try to insert a minimal record to test the PIN column specifically
        print("\nTesting PIN column with minimal data...")
        test_data = {
            "aadhar": "DEBUG_TEST_001",
            "name": "Debug Test",
            "pin": 123456
        }
        
        print("Inserting test data...")
        insert_result = supabase.table("verified_producers").upsert(test_data, on_conflict=['aadhar']).execute()
        print("Insert result:", insert_result)
        
        # Clean up
        print("Cleaning up test data...")
        supabase.table('verified_producers').delete().eq('aadhar', 'DEBUG_TEST_001').execute()
        print("Debug completed successfully!")
        
    except Exception as e:
        print(f"Error during debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_database_issue()