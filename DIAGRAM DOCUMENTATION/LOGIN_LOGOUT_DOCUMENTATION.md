# Login and Logout - Complete Documentation

## Table of Contents
1. [Login Sequence Diagram](#login-sequence-diagram)
2. [Logout Sequence Diagram](#logout-sequence-diagram)
3. [Login BCE Class Diagrams](#login-bce-class-diagrams)
4. [Logout BCE Class Diagrams](#logout-bce-class-diagrams)

---

## Login Sequence Diagram

### Success Flow

```
Client                LoginBoundary           LoginController          User Entity           Database
  |                         |                         |                      |                    |
  |--POST /api/auth/login-->|                         |                      |                    |
  |  {username, password,   |                         |                      |                    |
  |   role_name}            |                         |                      |                    |
  |                         |                         |                      |                    |
  |                         |--LoginController(payload)------------------>   |                    |
  |                         |                         |                      |                    |
  |                         |                         |--execute()           |                    |
  |                         |                         |                      |                    |
  |                         |                         |--validate_request_data()                  |
  |                         |                         |                      |                    |
  |                         |                         |<--True---------------|                    |
  |                         |                         |                      |                    |
  |                         |                         |--authenticate_user() |                    |
  |                         |                         |                      |                    |
  |                         |                         |--User.authenticate(username, password, role_name)
  |                         |                         |                      |                    |
  |                         |                         |                      |--find_by_username(username)
  |                         |                         |                      |                    |
  |                         |                         |                      |--SELECT * FROM users WHERE username=?-->
  |                         |                         |                      |                    |
  |                         |                         |                      |<--user_data--------|
  |                         |                         |                      |                    |
  |                         |                         |                      |--User(user_data)   |
  |                         |                         |                      |                    |
  |                         |                         |                      |--verify_password(password)
  |                         |                         |                      |                    |
  |                         |                         |                      |<--True-------------|
  |                         |                         |                      |                    |
  |                         |                         |                      |--update_last_login()|
  |                         |                         |                      |                    |
  |                         |                         |                      |--UPDATE users SET last_login=now()-->
  |                         |                         |                      |                    |
  |                         |                         |                      |<--True-------------|
  |                         |                         |                      |                    |
  |                         |                         |<--User object--------|                    |
  |                         |                         |                      |                    |
  |                         |                         |<--True---------------|                    |
  |                         |                         |                      |                    |
  |                         |                         |--user.generate_session_token()           |
  |                         |                         |                      |                    |
  |                         |                         |<--token (JWT string)-|                    |
  |                         |                         |                      |                    |
  |                         |                         |--ResponseHelpers.success_response(data, message, status_code)
  |                         |                         |                      |                    |
  |                         |                         |<--(Dict, int)--------|                    |
  |                         |                         |                      |                    |
  |                         |<--(response, status)----|                      |                    |
  |                         |                         |                      |                    |
  |                         |--jsonify(response), status                     |                    |
  |                         |                         |                      |                    |
  |<--200 OK, JSON----------|                         |                      |                    |
  |  {success: True,        |                         |                      |                    |
  |   data: {token, user}}  |                         |                      |                    |
```

### Validation Failure Flow

```
Client                LoginBoundary           LoginController          User Entity
  |                         |                         |                      |
  |--POST /api/auth/login-->|                         |                      |
  |  {username, password,   |                         |                      |
  |   role_name}            |                         |                      |
  |                         |                         |                      |
  |                         |--LoginController(payload)------------------>   |
  |                         |                         |                      |
  |                         |                         |--execute()           |
  |                         |                         |                      |
  |                         |                         |--validate_request_data()
  |                         |                         |                      |
  |                         |                         |<--False (validation error)
  |                         |                         |                      |
  |                         |                         |--ResponseHelpers.error_response(message, error_code, status_code)
  |                         |                         |                      |
  |                         |                         |<--(Dict, 400)--------|
  |                         |                         |                      |
  |                         |<--(response, status)----|                      |
  |                         |                         |                      |
  |<--400 Bad Request-------|                         |                      |
  |  {success: False,       |                         |                      |
  |   error_code: "VALIDATION_ERROR"}                 |                      |
```

### Authentication Failure Flow

```
Client                LoginBoundary           LoginController          User Entity           Database
  |                         |                         |                      |                    |
  |--POST /api/auth/login-->|                         |                      |                    |
  |  {username, password,   |                         |                      |                    |
  |   role_name}            |                         |                      |                    |
  |                         |                         |                      |                    |
  |                         |--LoginController(payload)------------------>   |                    |
  |                         |                         |                      |                    |
  |                         |                         |--execute()           |                    |
  |                         |                         |                      |                    |
  |                         |                         |--validate_request_data()                  |
  |                         |                         |                      |                    |
  |                         |                         |<--True---------------|                    |
  |                         |                         |                      |                    |
  |                         |                         |--authenticate_user() |                    |
  |                         |                         |                      |                    |
  |                         |                         |--User.authenticate(username, password, role_name)
  |                         |                         |                      |                    |
  |                         |                         |                      |--find_by_username(username)
  |                         |                         |                      |                    |
  |                         |                         |                      |--SELECT * FROM users WHERE username=?-->
  |                         |                         |                      |                    |
  |                         |                         |                      |<--user_data--------|
  |                         |                         |                      |                    |
  |                         |                         |                      |--verify_password(password)
  |                         |                         |                      |                    |
  |                         |                         |                      |<--False (wrong password)
  |                         |                         |                      |                    |
  |                         |                         |<--None---------------|                    |
  |                         |                         |                      |                    |
  |                         |                         |<--False--------------|                    |
  |                         |                         |                      |                    |
  |                         |                         |--ResponseHelpers.error_response(message, error_code, status_code)
  |                         |                         |                      |                    |
  |                         |                         |<--(Dict, 401)--------|                    |
  |                         |                         |                      |                    |
  |                         |<--(response, status)----|                      |                    |
  |                         |                         |                      |                    |
  |<--401 Unauthorized------|                         |                      |                    |
  |  {success: False,       |                         |                      |                    |
  |   error_code: "AUTH_FAILED"}                      |                      |                    |
```

---

## Logout Sequence Diagram

### Success Flow

```
Client                LogoutBoundary          User Entity              Database
  |                         |                      |                        |
  |--POST /api/auth/logout->|                      |                        |
  |  Authorization: Bearer {token}                 |                        |
  |                         |                      |                        |
  |                         |--extract token       |                        |
  |                         |  from headers        |                        |
  |                         |                      |                        |
  |                         |--User.verify_token(token)                     |
  |                         |                      |                        |
  |                         |                      |--jwt.decode(token, key, algorithms)
  |                         |                      |                        |
  |                         |                      |<--payload (user_id, username, role_id)
  |                         |                      |                        |
  |                         |                      |--User.find(user_id)    |
  |                         |                      |                        |
  |                         |                      |--SELECT * FROM users WHERE id=?------------>
  |                         |                      |                        |
  |                         |                      |<--user_data------------|
  |                         |                      |                        |
  |                         |                      |--User(user_data)       |
  |                         |                      |                        |
  |                         |<--User object--------|                        |
  |                         |                      |                        |
  |                         |--jsonify({success: True, message: "Logout successful"})
  |                         |                      |                        |
  |<--200 OK, JSON----------|                      |                        |
  |  {success: True,        |                      |                        |
  |   message: "Logout successful"}                |                        |
  |                         |                      |                        |
  |--Clear token from       |                      |                        |
  |  localStorage           |                      |                        |
```

### Token Invalid Flow

```
Client                LogoutBoundary          User Entity
  |                         |                      |
  |--POST /api/auth/logout->|                      |
  |  Authorization: Bearer {invalid_token}         |
  |                         |                      |
  |                         |--extract token       |
  |                         |  from headers        |
  |                         |                      |
  |                         |--User.verify_token(token)
  |                         |                      |
  |                         |                      |--jwt.decode(token, key, algorithms)
  |                         |                      |                        |
  |                         |                      |<--Exception (InvalidTokenError/ExpiredSignatureError)
  |                         |                      |
  |                         |<--None (token invalid)
  |                         |                      |
  |                         |--jsonify({success: False, message: "Invalid or expired token"})
  |                         |                      |
  |<--401 Unauthorized------|                      |
  |  {success: False,       |                      |
  |   message: "Invalid or expired token"}         |
```

---

## Login BCE Class Diagrams

### Boundary Layer

```
┌─────────────────────────────────────────────────┐
│           login_boundary (Flask Blueprint)      │
├─────────────────────────────────────────────────┤
│ Responsibilities:                               │
│ - Handle HTTP requests/responses                │
│ - Extract request payload                       │
│ - Return JSON responses                         │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│ - name: 'login'                                 │
│ - url_prefix: '/api/auth'                       │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│ + login() -> (jsonify, int)                     │
│   ├─ request.get_json() -> Dict                 │
│   ├─ Creates LoginController(payload)           │
│   ├─ Calls controller.execute()                 │
│   ├─ Returns jsonify(response), status          │
│   └─ Handles exceptions -> 500 error            │
├─────────────────────────────────────────────────┤
│ Route:                                          │
│ POST /api/auth/login                            │
├─────────────────────────────────────────────────┤
│ Request Format:                                 │
│ {                                               │
│   "username": string,                           │
│   "password": string,                           │
│   "role_name": string                           │
│ }                                               │
├─────────────────────────────────────────────────┤
│ Success Response (200):                         │
│ {                                               │
│   "success": true,                              │
│   "message": "Login successful",                │
│   "data": {                                     │
│     "token": string (JWT),                      │
│     "user": {                                   │
│       "id": int,                                │
│       "username": string,                       │
│       "full_name": string,                      │
│       "email": string,                          │
│       "role_id": int,                           │
│       "role": {                                 │
│         "id": int,                              │
│         "role_name": string,                    │
│         "dashboard_route": string               │
│       }                                         │
│     }                                           │
│   }                                             │
│ }                                               │
├─────────────────────────────────────────────────┤
│ Error Responses:                                │
│ - 400: Validation error                         │
│ - 401: Authentication failed                    │
│ - 500: Server error                             │
└─────────────────────────────────────────────────┘
```

### Control Layer

```
┌─────────────────────────────────────────────────┐
│           LoginController (Class)               │
├─────────────────────────────────────────────────┤
│ Responsibilities:                               │
│ - Orchestrate login authentication process      │
│ - Validate and sanitize request data            │
│ - Coordinate with User entity                   │
│ - Format response data                          │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│ - request_data: Dict                            │
│ - user: User | None                             │
│ - errors: List[str]                             │
│ - sanitized_data: Dict                          │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│ + __init__(request_data: Dict)                  │
│   └─ Initializes instance variables             │
│                                                 │
│ + validate_request_data() -> bool               │
│   ├─ Check request body exists                  │
│   ├─ RequestHelpers.validate_required_fields()  │
│   │   (username, password, role_name)           │
│   ├─ Sanitizers.sanitize_username()             │
│   ├─ Sanitizers.sanitize_string()               │
│   ├─ Validators.validate_username()             │
│   ├─ Validators.validate_password()             │
│   └─ Returns True/False                         │
│                                                 │
│ + authenticate_user() -> bool                   │
│   ├─ Calls User.authenticate(username,          │
│   │   password, role_name)                      │
│   ├─ Stores User object in self.user            │
│   └─ Returns True/False                         │
│                                                 │
│ + execute() -> Tuple[Dict, int]                 │
│   ├─ Step 1: validate_request_data()            │
│   │   └─ If False: return error (400)           │
│   ├─ Step 2: authenticate_user()                │
│   │   └─ If False: return error (401)           │
│   ├─ Step 3: user.generate_session_token()      │
│   ├─ Step 4: Build response_data dict           │
│   ├─ Step 5: ResponseHelpers.success_response() │
│   └─ Returns (Dict, int)                        │
├─────────────────────────────────────────────────┤
│ Dependencies:                                   │
│ - User (Entity)                                 │
│ - Role (Entity)                                 │
│ - Validators (Utils)                            │
│ - Sanitizers (Utils)                            │
│ - ResponseHelpers (Utils)                       │
│ - RequestHelpers (Utils)                        │
└─────────────────────────────────────────────────┘
```

### Entity Layer

```
┌─────────────────────────────────────────────────┐
│              User (Entity Class)                │
├─────────────────────────────────────────────────┤
│ Responsibilities:                               │
│ - Represent user data in memory (OOP)           │
│ - Authenticate user credentials                 │
│ - Verify password hashes                        │
│ - Generate JWT tokens                           │
│ - Interact with database                        │
├─────────────────────────────────────────────────┤
│ Attributes (Instance Variables):                │
│ - id: int | None                                │
│ - username: str | None                          │
│ - password: str | None (hashed)                 │
│ - email: str | None                             │
│ - full_name: str | None                         │
│ - role_id: int | None                           │
│ - is_active: bool                               │
│ - created_at: str | None                        │
│ - last_login: str | None                        │
│ - roles: Dict | None (joined data)              │
├─────────────────────────────────────────────────┤
│ Instance Methods:                               │
│ + verify_password(password: str) -> bool        │
│   ├─ Compares plain text password with hash     │
│   ├─ Uses check_password_hash()                 │
│   └─ Returns True if match                      │
│                                                 │
│ + generate_session_token() -> str               │
│   ├─ Creates JWT payload with user data         │
│   ├─ Sets expiration (24 hours)                 │
│   ├─ jwt.encode(payload, SECRET_KEY, 'HS256')   │
│   └─ Returns JWT token string                   │
│                                                 │
│ + update_last_login() -> bool                   │
│   ├─ Updates last_login timestamp               │
│   ├─ Saves to database                          │
│   └─ Returns True if successful                 │
├─────────────────────────────────────────────────┤
│ Class Methods (Factory Methods):                │
│ + authenticate(username: str, password: str,    │
│     role_name: str | None) -> User | None       │
│   ├─ Calls find_by_username(username)           │
│   ├─ If not found: return None                  │
│   ├─ Calls user.verify_password(password)       │
│   ├─ If wrong password: return None             │
│   ├─ Checks is_active status                    │
│   ├─ If inactive: return None                   │
│   ├─ Verifies role_name if provided             │
│   │   └─ Role.find_by_name(role_name)           │
│   ├─ If role mismatch: return None              │
│   ├─ Calls user.update_last_login()             │
│   └─ Returns User object                        │
│                                                 │
│ + find_by_username(username: str) -> User|None  │
│   ├─ Query: SELECT * FROM users                 │
│   │         WHERE username = ?                  │
│   ├─ Joins with roles table                     │
│   ├─ If found: return User(user_data)           │
│   └─ If not found: return None                  │
│                                                 │
│ + verify_token(token: str) -> User | None       │
│   ├─ jwt.decode(token, SECRET_KEY, ['HS256'])   │
│   ├─ Extract user_id from payload               │
│   ├─ Calls find(user_id)                        │
│   └─ Returns User object or None                │
├─────────────────────────────────────────────────┤
│ Database Table: users                           │
│ - id (PK, serial)                               │
│ - username (unique, not null)                   │
│ - password (not null, hashed)                   │
│ - email (unique, not null)                      │
│ - full_name (not null)                          │
│ - role_id (FK -> roles.id)                      │
│ - is_active (default true)                      │
│ - created_at (timestamp)                        │
│ - last_login (timestamp)                        │
└─────────────────────────────────────────────────┘
```

### Helper Classes (Utils)

```
┌─────────────────────────────────────────────────┐
│             Validators (Static Class)           │
├─────────────────────────────────────────────────┤
│ + validate_username(username: str)              │
│   -> Tuple[bool, str]                           │
│   ├─ Checks length (3-50 chars)                 │
│   ├─ Checks allowed characters (alphanumeric_)  │
│   └─ Returns (True, "") or (False, error_msg)   │
│                                                 │
│ + validate_password(password: str)              │
│   -> Tuple[bool, str]                           │
│   ├─ Checks length (8+ chars)                   │
│   └─ Returns (True, "") or (False, error_msg)   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│             Sanitizers (Static Class)           │
├─────────────────────────────────────────────────┤
│ + sanitize_username(username: str) -> str       │
│   ├─ Strips whitespace                          │
│   ├─ Converts to lowercase                      │
│   └─ Returns cleaned username                   │
│                                                 │
│ + sanitize_string(text: str) -> str             │
│   ├─ Strips whitespace                          │
│   ├─ Removes dangerous characters               │
│   └─ Returns cleaned string                     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│          ResponseHelpers (Static Class)         │
├─────────────────────────────────────────────────┤
│ + success_response(data: Dict, message: str,    │
│     status_code: int) -> Tuple[Dict, int]       │
│   └─ Returns formatted success response         │
│                                                 │
│ + error_response(message: str, error_code: str, │
│     status_code: int) -> Tuple[Dict, int]       │
│   └─ Returns formatted error response           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│          RequestHelpers (Static Class)          │
├─────────────────────────────────────────────────┤
│ + validate_required_fields(data: Dict,          │
│     required: List[str])                        │
│   -> Tuple[bool, str, List[str]]                │
│   ├─ Checks if all required fields present      │
│   └─ Returns (is_valid, error_msg, missing)     │
└─────────────────────────────────────────────────┘
```

---

## Logout BCE Class Diagrams

### Boundary Layer

```
┌─────────────────────────────────────────────────┐
│          logout_boundary (Flask Blueprint)      │
├─────────────────────────────────────────────────┤
│ Responsibilities:                               │
│ - Handle HTTP logout requests                   │
│ - Extract JWT token from headers                │
│ - Verify token validity                         │
│ - Return JSON responses                         │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│ - name: 'logout'                                │
│ - url_prefix: '/api/auth'                       │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│ + logout() -> (jsonify, int)                    │
│   ├─ request.headers.get('Authorization')       │
│   ├─ Extract token (remove 'Bearer ' prefix)    │
│   ├─ Calls User.verify_token(token)             │
│   ├─ If None: return 401 error                  │
│   ├─ If User: return success 200                │
│   └─ Handles exceptions -> 500 error            │
├─────────────────────────────────────────────────┤
│ Route:                                          │
│ POST /api/auth/logout                           │
├─────────────────────────────────────────────────┤
│ Request Format:                                 │
│ Headers:                                        │
│   Authorization: Bearer <JWT_TOKEN>             │
│ Body: (empty)                                   │
├─────────────────────────────────────────────────┤
│ Success Response (200):                         │
│ {                                               │
│   "success": true,                              │
│   "message": "Logout successful"                │
│ }                                               │
├─────────────────────────────────────────────────┤
│ Error Responses:                                │
│ - 401: Invalid or expired token                 │
│ - 500: Server error                             │
├─────────────────────────────────────────────────┤
│ Note:                                           │
│ Logout is primarily CLIENT-SIDE:               │
│ - Client removes token from localStorage        │
│ - This endpoint validates token before logout   │
│ - No server-side session invalidation needed    │
│   (JWT is stateless)                            │
└─────────────────────────────────────────────────┘
```

### Entity Layer

```
┌─────────────────────────────────────────────────┐
│              User (Entity Class)                │
├─────────────────────────────────────────────────┤
│ Responsibilities (for Logout):                  │
│ - Verify JWT token validity                     │
│ - Decode token and extract user_id              │
│ - Load user data from database                  │
├─────────────────────────────────────────────────┤
│ Class Methods Used:                             │
│ + verify_token(token: str) -> User | None       │
│   ├─ jwt.decode(token, SECRET_KEY, ['HS256'])   │
│   │   ├─ Validates signature                    │
│   │   ├─ Checks expiration                      │
│   │   └─ Returns payload or raises exception    │
│   ├─ Extract user_id from payload               │
│   ├─ Calls find(user_id)                        │
│   │   ├─ SELECT * FROM users WHERE id=?         │
│   │   └─ Returns User(user_data)                │
│   └─ Returns User object or None                │
│                                                 │
│ + find(user_id: int) -> User | None             │
│   ├─ Query: SELECT * FROM users                 │
│   │         WHERE id = ?                        │
│   ├─ Joins with roles table                     │
│   ├─ If found: return User(user_data)           │
│   └─ If not found: return None                  │
├─────────────────────────────────────────────────┤
│ JWT Token Structure:                            │
│ {                                               │
│   "user_id": int,                               │
│   "username": string,                           │
│   "role_id": int,                               │
│   "exp": timestamp (24 hours from issue)        │
│ }                                               │
├─────────────────────────────────────────────────┤
│ Token Verification Errors:                      │
│ - jwt.ExpiredSignatureError                     │
│   └─ Token has expired (>24 hours old)          │
│ - jwt.InvalidTokenError                         │
│   └─ Token signature invalid or malformed       │
│ - Exception                                     │
│   └─ Other decoding errors                      │
│                                                 │
│ All errors return None                          │
└─────────────────────────────────────────────────┘
```

### No Control Layer

```
┌─────────────────────────────────────────────────┐
│              NO CONTROLLER LAYER                │
├─────────────────────────────────────────────────┤
│ Design Decision:                                │
│ Logout is BOUNDARY-ONLY (simplified)            │
│                                                 │
│ Reasons:                                        │
│ 1. Minimal business logic                       │
│ 2. Single responsibility: verify token          │
│ 3. No data validation/sanitization needed       │
│ 4. No complex orchestration required            │
│ 5. Direct Entity method call (User.verify_token)│
│                                                 │
│ Flow:                                           │
│ Boundary → Entity (User.verify_token)           │
│                                                 │
│ Contrast with Login:                            │
│ Login requires Controller because:              │
│ - Multi-step validation                         │
│ - Data sanitization                             │
│ - Complex authentication logic                  │
│ - Response formatting                           │
│ - Error handling across multiple steps          │
└─────────────────────────────────────────────────┘
```

---

## Data Flow Summary

### Login Data Flow

```
1. Client sends credentials
   ↓
2. Boundary extracts JSON
   ↓
3. Controller validates format
   ↓
4. Controller sanitizes data
   ↓
5. Entity authenticates (DB query)
   ↓
6. Entity verifies password hash
   ↓
7. Entity updates last_login
   ↓
8. Entity generates JWT token
   ↓
9. Controller formats response
   ↓
10. Boundary returns JSON + token
   ↓
11. Client stores token in localStorage
```

### Logout Data Flow

```
1. Client sends token in header
   ↓
2. Boundary extracts token
   ↓
3. Entity decodes and verifies JWT
   ↓
4. Entity loads user from DB
   ↓
5. Boundary returns success
   ↓
6. Client removes token from localStorage
```

---

## Key Design Patterns

### 1. **Factory Pattern** (Entity Layer)
- `User.authenticate()` - Creates authenticated User object
- `User.find_by_username()` - Creates User object from username
- `User.verify_token()` - Creates User object from JWT token

### 2. **Strategy Pattern** (Validation)
- Multiple validation strategies: format, business rules, database constraints
- Validators and Sanitizers as separate utility classes

### 3. **True OOP Pattern** (Controller)
- Controller holds state (request_data, user, errors)
- Methods operate on instance state
- Clear lifecycle: create → validate → authenticate → respond

### 4. **Stateless Authentication** (JWT)
- No server-side session storage
- Token contains all necessary user info
- Logout is client-side only (remove token)

### 5. **Separation of Concerns** (BCE)
- **Boundary**: HTTP interface only
- **Control**: Business logic orchestration
- **Entity**: Data and database operations

---

## Security Measures

### Login Security
1. **Password Hashing**: pbkdf2:sha256 (Werkzeug)
2. **Input Sanitization**: Username/role_name cleaned
3. **Input Validation**: Format checks before DB query
4. **Role Verification**: Ensures user has correct role
5. **Active Status Check**: Prevents inactive users from logging in
6. **JWT Expiration**: Tokens expire after 24 hours
7. **Error Messages**: Generic "Invalid credentials" (no username leakage)

### Logout Security
1. **Token Verification**: Validates JWT signature and expiration
2. **User Existence Check**: Ensures user still exists in DB
3. **Client-Side Cleanup**: Token removed from localStorage
4. **Stateless Design**: No server-side session to clean up

---

## Error Handling

### Login Errors
| Error Code | Status | Cause |
|------------|--------|-------|
| VALIDATION_ERROR | 400 | Missing fields, invalid format |
| AUTH_FAILED | 401 | Wrong credentials, inactive user, role mismatch |
| SERVER_ERROR | 500 | Database error, unexpected exception |

### Logout Errors
| Status | Cause |
|--------|-------|
| 401 | Invalid token, expired token, user not found |
| 500 | Token decode error, unexpected exception |

---

## Testing Checklist

### Login Tests
- ✅ Valid credentials with correct role
- ✅ Valid credentials with wrong role
- ✅ Invalid username format
- ✅ Invalid password format
- ✅ Wrong password
- ✅ Non-existent username
- ✅ Inactive user account
- ✅ Missing required fields
- ✅ Token generation successful
- ✅ last_login timestamp updated

### Logout Tests
- ✅ Valid token logout
- ✅ Expired token
- ✅ Invalid token signature
- ✅ Malformed token
- ✅ Missing Authorization header
- ✅ Token for non-existent user

---

## Performance Considerations

### Login
1. **Database Queries**: 2 queries per login
   - Find user by username (with role join)
   - Update last_login
2. **Password Hashing**: ~100ms for bcrypt/pbkdf2
3. **JWT Generation**: ~1ms
4. **Total**: ~150-200ms typical response time

### Logout
1. **Database Queries**: 1 query per logout
   - Find user by ID (from token)
2. **JWT Decode**: <1ms
3. **Total**: ~50-100ms typical response time

---





