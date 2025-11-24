# HyreBuy API Testing Guide

## Authentication Endpoints (Day 4)

### Prerequisites

1. Start the FastAPI server:
```bash
cd /home/koans/projects/hyrebuy/hyrebuy-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Database must be running with migrations applied:
```bash
alembic upgrade head
```

---

## 1. User Registration (P1-F01)

**Endpoint**: `POST /api/v1/auth/register`

**Request Body**:
```json
{
  "email": "test@example.com",
  "password": "test1234",
  "name": "Test User",
  "phone": "+91-9876543210",
  "company_id": null
}
```

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test1234",
    "name": "Test User",
    "phone": "+91-9876543210"
  }'
```

**Expected Response** (201 Created):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "test@example.com",
    "name": "Test User",
    "phone": "+91-9876543210",
    "company_id": null,
    "is_group_admin": "false",
    "total_rewards_earned": "0",
    "created_at": "2025-11-24T12:00:00Z"
  }
}
```

**Error Cases**:
- Email already registered: `400 Bad Request`
- Invalid email format: `422 Unprocessable Entity`
- Password too short (<8 chars): `422 Unprocessable Entity`

---

## 2. User Login (P1-F02)

**Endpoint**: `POST /api/v1/auth/login`

**Request Body**:
```json
{
  "email": "test@example.com",
  "password": "test1234"
}
```

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test1234"
  }'
```

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "test@example.com",
    "name": "Test User",
    "phone": "+91-9876543210",
    "company_id": null,
    "is_group_admin": "false",
    "total_rewards_earned": "0",
    "created_at": "2025-11-24T12:00:00Z"
  }
}
```

**Error Cases**:
- Incorrect email or password: `401 Unauthorized`
- Invalid email format: `422 Unprocessable Entity`

---

## 3. Get Current User

**Endpoint**: `GET /api/v1/auth/me`

**Headers**:
```
Authorization: Bearer {access_token}
```

**cURL Command**:
```bash
# Replace YOUR_TOKEN with the access_token from login/register
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "test@example.com",
  "name": "Test User",
  "phone": "+91-9876543210",
  "company_id": null,
  "is_group_admin": "false",
  "total_rewards_earned": "0",
  "created_at": "2025-11-24T12:00:00Z"
}
```

**Error Cases**:
- Missing token: `403 Forbidden`
- Invalid token: `401 Unauthorized`
- Expired token (>7 days): `401 Unauthorized`

---

## Interactive API Documentation

FastAPI provides interactive API documentation:

1. **Swagger UI**: http://localhost:8000/docs
   - Interactive UI to test endpoints
   - Click "Try it out" to test each endpoint
   - Authorize button to add Bearer token

2. **ReDoc**: http://localhost:8000/redoc
   - Clean, readable documentation
   - Good for sharing with frontend team

---

## Complete Authentication Flow Test

**Step 1**: Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "secure123",
    "name": "John Doe",
    "phone": "+91-9876543210"
  }' | jq
```

**Step 2**: Save the access_token from response

**Step 3**: Use token to get user info
```bash
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq
```

**Step 4**: Login with same credentials
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "secure123"
  }' | jq
```

**Step 5**: Verify duplicate registration fails
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "secure123",
    "name": "John Doe"
  }' | jq
```
Expected: `400 Bad Request - Email already registered`

---

## Token Validation Test

**Test with invalid token**:
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer invalid_token" | jq
```
Expected: `401 Unauthorized - Could not validate credentials`

---

## Password Security Verification

**Verify password is hashed** (manual check):
1. Register a user
2. Check database: `SELECT email, password_hash FROM users WHERE email='john@example.com';`
3. Password hash should start with `$2b$` (bcrypt)
4. Password hash should be ~60 characters long
5. Original password should NOT be visible

---

## JWT Token Inspection

**Decode token** (use jwt.io):
1. Copy access_token from login/register response
2. Go to https://jwt.io/
3. Paste token in "Encoded" section
4. Verify payload contains:
   - `sub`: user email
   - `exp`: expiration timestamp (7 days from now)

---

## Performance Benchmarks (Phase 1 Targets)

- Registration: <500ms
- Login: <500ms
- Get current user: <200ms

**Benchmark with Apache Bench**:
```bash
# Login endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 -p login.json -T "application/json" \
  http://localhost:8000/api/v1/auth/login
```

---

## Day 4 Validation Checklist

### P1-F01: User Registration
- [ ] User can submit registration form
- [ ] Password is hashed (bcrypt)
- [ ] JWT token is generated
- [ ] User data stored in database
- [ ] Duplicate email returns error
- [ ] Invalid data returns 422

### P1-F02: User Login
- [ ] User can login with correct credentials
- [ ] JWT token is generated (7-day expiry)
- [ ] Invalid credentials return 401
- [ ] Token can be used for authenticated requests

### Additional Validation
- [ ] GET /auth/me works with valid token
- [ ] GET /auth/me fails with invalid token
- [ ] Token expires after 7 days
- [ ] Password stored as hash (not plaintext)
- [ ] API documentation accessible (/docs)

---

**Status**: Ready for Day 5 (Frontend integration)
