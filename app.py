import os
import json
import base64
import tempfile
from flask import Flask, request, jsonify
from agent1 import Agent1
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Agent1
agent1 = Agent1()

# Initialize Supabase client for data retrieval
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({
        "message": "Welcome to Sadapurne Agent1 API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "verify": "POST /verify",
            "get_producer": "GET /producers/<aadhar>",
            "get_all_producers": "GET /producers"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Agent1 API is running"}), 200

@app.route('/verify', methods=['POST'])
def verify_producer():
    """Verify producer endpoint"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['aadhar', 'name', 'fssai_pdf', 'annual_income']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "failed",
                    "stage": "input_validation",
                    "message": f"Missing required field: {field}"
                }), 400
        
        aadhar = data['aadhar']
        name = data['name']
        fssai_pdf_base64 = data['fssai_pdf']
        annual_income = data['annual_income']
        
        # Validate Aadhar number
        if not aadhar or not isinstance(aadhar, str) or len(aadhar.strip()) == 0:
            return jsonify({
                "status": "failed",
                "stage": "input_validation",
                "message": "Invalid Aadhar number"
            }), 400
        
        # Validate name
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            return jsonify({
                "status": "failed",
                "stage": "input_validation",
                "message": "Invalid name"
            }), 400
        
        # Validate annual income
        try:
            income = float(annual_income)
            if income < 0:
                return jsonify({
                    "status": "failed",
                    "stage": "input_validation",
                    "message": "Annual income must be a positive number"
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                "status": "failed",
                "stage": "input_validation",
                "message": "Invalid annual income format"
            }), 400
        
        # Validate and decode PDF data
        if not fssai_pdf_base64 or not isinstance(fssai_pdf_base64, str):
            return jsonify({
                "status": "failed",
                "stage": "input_validation",
                "message": "Invalid FSSAI PDF data"
            }), 400
        
        try:
            # Decode base64 PDF data
            pdf_data = base64.b64decode(fssai_pdf_base64)
        except Exception as e:
            return jsonify({
                "status": "failed",
                "stage": "input_validation",
                "message": f"Failed to decode FSSAI PDF data: {str(e)}"
            }), 400
        
        # Perform verification using Agent1 with PDF data
        result = agent1.verify_producer_with_pdf_data(name, pdf_data, income, aadhar)
        
        # Return result as JSON
        return jsonify(result), 200 if result["status"] == "success" else 400
                
    except Exception as e:
        return jsonify({
            "status": "failed",
            "stage": "server_error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/producers/<aadhar>', methods=['GET'])
def get_producer_by_aadhar(aadhar):
    """Get verified producer by Aadhar number"""
    try:
        # Query Supabase for producer data
        result = supabase.table('verified_producers').select('*').eq('aadhar', aadhar).execute()
        
        if result.data:
            return jsonify({
                "status": "success",
                "data": result.data[0]
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "message": "No verified producer found with this Aadhar number"
            }), 404
            
    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": f"Error retrieving producer data: {str(e)}"
        }), 500

@app.route('/producers', methods=['GET'])
def get_all_producers():
    """Get all verified producers"""
    try:
        # Query Supabase for all producer data
        result = supabase.table('verified_producers').select('*').execute()
        
        return jsonify({
            "status": "success",
            "data": result.data
        }), 200
            
    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": f"Error retrieving producer data: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)), debug=False)