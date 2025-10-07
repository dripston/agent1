# Sadapurne Agent1 Web API

This is a web API wrapper for Agent1 that provides RESTful endpoints for producer verification.

## Endpoints

### Health Check
```
GET /health
```
Returns the health status of the API.

### Verify Producer
```
POST /verify
```
Verifies a producer's identity using their Aadhar number, name, FSSAI certificate, and annual income.

**Request Body:**
```json
{
  "aadhar": "string",
  "name": "string",
  "fssai_pdf": "base64_encoded_pdf_data",
  "annual_income": number
}
```

**Response:**
```json
{
  "status": "success|failed",
  "message": "string",
  "details": {}
}
```

### Get Producer by Aadhar
```
GET /producers/{aadhar}
```
Retrieves verified producer information by Aadhar number.

### Get All Producers
```
GET /producers
```
Retrieves all verified producers.

## Deployment

This API is designed to be deployed on Render. It uses a Dockerfile for containerization.

## Environment Variables

The following environment variables must be set:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key