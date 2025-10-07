# Agent1 Integration Guide

This document explains how to integrate the Agent1 web API with your Vercel frontend application.

## API Endpoints

The Agent1 web API provides the following endpoints:

### 1. Verify Producer
```
POST /verify
```

**Request Body:**
```json
{
  "aadhar": "string",           // Aadhar number (12 digits)
  "name": "string",             // Business name as it appears on FSSAI document
  "fssai_pdf": "base64_string", // Base64 encoded FSSAI certificate PDF
  "annual_income": number       // Annual income in rupees
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Producer verified successfully",
  "name_details": {
    "provided_name": "string",
    "business_name": "string"
  },
  "certificate_type": "string",
  "format_details": {
    "status": "verified",
    "message": "string"
  },
  "issue_date": "string",
  "expiry_date": "string",
  "address": "string",
  "data_stored": boolean
}
```

**Failure Response (400):**
```json
{
  "status": "failed",
  "stage": "string",            // Stage where verification failed
  "message": "string",          // Clear reason for failure
  "details": {},                // Additional details (varies by stage)
  "issues": ["string"]          // List of issues (format verification stage)
}
```

### 2. Get Producer by Aadhar
```
GET /producers/{aadhar}
```

**Response (200):**
```json
{
  "status": "success",
  "data": {
    "aadhar": "string",
    "name": "string",
    "fssai_license_number": "string",
    "annual_income": number,
    "certificate_type": "string",
    "business_type": "string",
    "issue_date": "string",
    "expiry_date": "string",
    "address": "string"
  }
}
```

### 3. Get All Producers
```
GET /producers
```

**Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "aadhar": "string",
      "name": "string",
      "fssai_license_number": "string",
      "annual_income": number,
      "certificate_type": "string",
      "business_type": "string",
      "issue_date": "string",
      "expiry_date": "string",
      "address": "string"
    }
  ]
}
```

## Frontend Integration Example

### Uploading and Converting PDF to Base64

```javascript
// Function to convert file to base64
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      // Remove the data URL prefix (e.g., "data:application/pdf;base64,")
      const base64String = reader.result.split(',')[1];
      resolve(base64String);
    };
    reader.onerror = error => reject(error);
  });
}

// Handle file upload
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (file && file.type === 'application/pdf') {
    try {
      const base64PDF = await fileToBase64(file);
      // Store base64PDF for later use in verification request
      return base64PDF;
    } catch (error) {
      console.error('Error converting file to base64:', error);
    }
  } else {
    console.error('Please upload a PDF file');
  }
}
```

### Sending Verification Request

```javascript
async function verifyProducer(aadhar, name, fssaiPdfBase64, annualIncome) {
  const verificationData = {
    aadhar: aadhar,
    name: name,
    fssai_pdf: fssaiPdfBase64,
    annual_income: annualIncome
  };

  try {
    const response = await fetch('YOUR_AGENT1_API_URL/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(verificationData)
    });

    const result = await response.json();
    
    if (response.ok && result.status === 'success') {
      // Verification successful
      console.log('Verification successful:', result);
      return { success: true, data: result };
    } else {
      // Verification failed
      console.log('Verification failed:', result);
      return { success: false, error: result.message, stage: result.stage };
    }
  } catch (error) {
    console.error('Network error:', error);
    return { success: false, error: 'Network error occurred' };
  }
}
```

### Handling Response

```javascript
// Example of handling verification response
function handleVerificationResponse(response) {
  if (response.success) {
    // Show success message
    alert('Producer verified successfully!');
    // Display verification details
    displayVerificationDetails(response.data);
  } else {
    // Show error message with clear reason
    alert(`Verification failed at ${response.stage}: ${response.error}`);
  }
}

function displayVerificationDetails(data) {
  // Display the verification details to the user
  document.getElementById('businessName').textContent = data.name_details.provided_name;
  document.getElementById('certificateType').textContent = data.certificate_type;
  document.getElementById('expiryDate').textContent = data.expiry_date;
  // ... display other details
}
```

## Error Handling

The API provides clear error messages for different failure scenarios:

1. **Input Validation Errors**: Missing fields, invalid data formats
2. **Name Verification Errors**: Name mismatch between provided name and document
3. **Document Format Errors**: Missing required fields in FSSAI document
4. **Certificate Type Errors**: Mismatch between certificate type and income
5. **Server Errors**: Internal server issues

Always check the `stage` field in error responses to understand where the verification failed and provide appropriate feedback to users.

## Deployment Considerations

1. **CORS**: Ensure your Vercel frontend domain is allowed in the Agent1 API CORS settings
2. **Environment Variables**: Set proper environment variables for Supabase connection
3. **Security**: Use HTTPS in production and validate all inputs
4. **Rate Limiting**: Implement rate limiting to prevent abuse