# CSR Application - Complete Sequence Diagrams Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Authentication Sequences](#authentication-sequences)
3. [User Management Sequences](#user-management-sequences)
4. [Request Management Sequences](#request-management-sequences)
5. [Shortlist Management Sequences](#shortlist-management-sequences)
6. [Common Patterns](#common-patterns)
7. [Error Handling Sequences](#error-handling-sequences)

---

## 🎯 Overview

This document provides detailed sequence diagrams for all major user stories and use cases in the CSR Application. Each sequence shows the complete flow from user action through all BCE layers to the database and back.

### Notation Guide
```
Actor       User/System initiating action
→           Synchronous message/method call
- - ->      Response/Return value
[condition] Conditional flow
alt/else    Alternative paths
loop        Repeated actions
```

---

## 🔐 Authentication Sequences

### 1. User Login Sequence

```
Actor: User
Components: Browser → Login Boundary → Login Controller → User Entity → Database

┌──────┐       ┌─────────┐      ┌─────────┐      ┌──────────┐      ┌──────┐      ┌──────────┐
│ User │       │ Browser │      │ Boundary│      │Controller│      │Entity│      │ Database │
└──┬───┘       └────┬────┘      └────┬────┘      └────┬─────┘      └──┬───┘      └────┬─────┘
   │                │                 │                │               │               │
   │ 1. Enter credentials            │                │               │               │
   │ (username, password, role)      │                │               │               │
   ├────────────────>│                │                │               │               │
   │                 │                │                │               │               │
   │                 │ 2. POST /api/auth/login         │               │               │
   │                 │ Body: {username, password, role_name}           │               │
   │                 ├────────────────>│                │               │               │
   │                 │                 │                │               │               │
   │                 │                 │ 3. login(data) │               │               │
   │                 │                 ├────────────────>│               │               │
   │                 │                 │                │               │               │
   │                 │                 │                │ 4. Extract & sanitize data    │
   │                 │                 │                ├───────────────>               │
   │                 │                 │                │               │               │
   │                 │                 │                │ 5. Validate username format   │
   │                 │                 │                ├───────────────>               │
   │                 │                 │                │<───────────────               │
   │                 │                 │                │ is_valid: true                │
   │                 │                 │                │               │               │
   │                 │                 │                │ 6. Validate password format   │
   │                 │                 │                ├───────────────>               │
   │                 │                 │                │<───────────────               │
   │                 │                 │                │ is_valid: true                │
   │                 │                 │                │               │               │
   │                 │                 │                │ 7. authenticate_user()        │
   │                 │                 │                │  (username, password, role)   │
   │                 │                 │                ├───────────────>│               │
   │                 │                 │                │                │               │
   │                 │                 │                │                │ 8. SELECT * FROM users
   │                 │                 │                │                │    WHERE username = ?
   │                 │                 │                │                │    AND is_active = true
   │                 │                 │                │                ├──────────────>│
   │                 │                 │                │                │<──────────────│
   │                 │                 │                │                │ user_record   │
   │                 │                 │                │                │               │
   │                 │                 │                │                │ 9. Verify password hash
   │                 │                 │                │                ├───────────────>
   │                 │                 │                │                │ (werkzeug.check_password_hash)
   │                 │                 │                │                │               │
   │                 │                 │                │                │ 10. SELECT * FROM roles
   │                 │                 │                │                │     WHERE id = user.role_id
   │                 │                 │                │                ├──────────────>│
   │                 │                 │                │                │<──────────────│
   │                 │                 │                │                │ role_record   │
   │                 │                 │                │                │               │
   │                 │                 │                │                │ 11. Check role_name matches
   │                 │                 │                │                │               │
   │                 │                 │                │                │ 12. Generate JWT token
   │                 │                 │                │                ├───────────────>
   │                 │                 │                │                │ (jwt.encode)  │
   │                 │                 │                │<───────────────│               │
   │                 │                 │                │ {token, user_data, role}       │
   │                 │                 │                │               │               │
   │                 │                 │                │ 13. log_user_activity()        │
   │                 │                 │                │    (user_id, "login", details) │
   │                 │                 │                ├───────────────>│               │
   │                 │                 │                │                │ INSERT INTO user_activity
   │                 │                 │                │                ├──────────────>│
   │                 │                 │                │                │<──────────────│
   │                 │                 │<────────────────                │               │
   │                 │                 │ {success: true, token, user}    │               │
   │                 │<────────────────│                │               │               │
   │                 │ 200 OK          │                │               │               │
   │                 │ {success: true, token, user}     │               │               │
   │<────────────────│                 │                │               │               │
   │                 │                 │                │               │               │
   │ 14. Store token in localStorage   │                │               │               │
   │ 15. Store user data in localStorage                │               │               │
   │ 16. Redirect to dashboard (based on role)          │               │               │
   │ (e.g., /csr for CSR Rep, /pin for PIN)             │               │               │
   │                 │                 │                │               │               │
```

**Key Steps:**
1. User enters credentials in login form
2. Frontend sends POST request with credentials
3. Boundary passes to Controller
4. Controller sanitizes and validates input
5. Entity checks database for user
6. Password hash verification
7. Role verification
8. JWT token generation
9. Activity logging
10. Response with token and user data
11. Frontend stores auth data
12. User redirected to role-specific dashboard

**Error Cases:**
- Invalid username format → 400 Bad Request
- Invalid password format → 400 Bad Request
- User not found → 401 Unauthorized
- Password mismatch → 401 Unauthorized
- Role mismatch → 401 Unauthorized
- Inactive user → 401 Unauthorized

---

### 2. Token Verification Sequence

```
Browser → Verify Boundary → Login Controller → User Entity → Database

┌─────────┐      ┌─────────┐      ┌──────────┐      ┌──────┐      ┌──────────┐
│ Browser │      │ Boundary│      │Controller│      │Entity│      │ Database │
└────┬────┘      └────┬────┘      └────┬─────┘      └──┬───┘      └────┬─────┘
     │                │                │               │               │
     │ 1. GET /api/auth/verify         │               │               │
     │    Authorization: Bearer {token}│               │               │
     ├────────────────>│                │               │               │
     │                 │                │               │               │
     │                 │ 2. verify(token)               │               │
     │                 ├────────────────>│               │               │
     │                 │                │               │               │
     │                 │                │ 3. Extract token from header  │
     │                 │                │               │               │
     │                 │                │ 4. verify_session_token(token)│
     │                 │                ├───────────────>│               │
     │                 │                │                │               │
     │                 │                │                │ 5. jwt.decode(token)
     │                 │                │                ├───────────────>
     │                 │                │                │ payload: {user_id, exp}
     │                 │                │                │               │
     │                 │                │                │ 6. Check expiration
     │                 │                │                │ if exp < now() → Invalid
     │                 │                │                │               │
     │                 │                │                │ 7. SELECT * FROM users
     │                 │                │                │    WHERE id = payload.user_id
     │                 │                │                │    AND is_active = true
     │                 │                │                ├──────────────>│
     │                 │                │                │<──────────────│
     │                 │                │                │ user_record   │
     │                 │                │                │               │
     │                 │                │                │ 8. SELECT * FROM roles
     │                 │                │                │    WHERE id = user.role_id
     │                 │                │                ├──────────────>│
     │                 │                │                │<──────────────│
     │                 │                │<───────────────│               │
     │                 │                │ {user_data, role}              │
     │                 │<────────────────                │               │
     │                 │ {success: true, user}           │               │
     │<────────────────│                │               │               │
     │ 200 OK          │                │               │               │
     │                 │                │               │               │
```

**Used By:**
- Protected routes (middleware)
- Page load authentication checks
- Session refresh

---

## 👥 User Management Sequences

### 3. Create New User Account

```
Admin → Browser → Create Boundary → Create Controller → User Entity → Database

┌───────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────┐    ┌──────────┐
│ Admin │    │ Browser │    │ Boundary│    │Controller│    │Entity│    │ Database │
└───┬───┘    └────┬────┘    └────┬────┘    └────┬─────┘    └──┬───┘    └────┬─────┘
    │             │              │              │              │             │
    │ 1. Fill user form          │              │              │             │
    │    (username, password, email, full_name, role_id)       │             │
    ├────────────>│              │              │              │             │
    │             │              │              │              │             │
    │             │ 2. POST /api/users          │              │             │
    │             │    Authorization: Bearer {token}           │             │
    │             │    Body: {username, password, ...}         │             │
    │             ├─────────────>│              │              │             │
    │             │              │              │              │             │
    │             │              │ 3. create_user(data)         │             │
    │             │              ├─────────────>│              │             │
    │             │              │              │              │             │
    │             │              │              │ 4. Validate required fields
    │             │              │              ├──────────────>             │
    │             │              │              │ (username, password, email, full_name, role_id)
    │             │              │              │              │             │
    │             │              │              │ 5. Validate username format
    │             │              │              ├──────────────>             │
    │             │              │              │<──────────────             │
    │             │              │              │ is_valid: true             │
    │             │              │              │              │             │
    │             │              │              │ 6. Validate password strength
    │             │              │              ├──────────────>             │
    │             │              │              │<──────────────             │
    │             │              │              │ is_valid: true (≥8 chars)  │
    │             │              │              │              │             │
    │             │              │              │ 7. Validate email format    │
    │             │              │              ├──────────────>             │
    │             │              │              │<──────────────             │
    │             │              │              │              │             │
    │             │              │              │ 8. check_username_exists()  │
    │             │              │              ├──────────────>│             │
    │             │              │              │              │ SELECT COUNT(*)
    │             │              │              │              │ FROM users
    │             │              │              │              │ WHERE username = ?
    │             │              │              │              ├────────────>│
    │             │              │              │              │<────────────│
    │             │              │              │<──────────────│ count: 0    │
    │             │              │              │ exists: false              │
    │             │              │              │              │             │
    │             │              │              │ 9. check_email_exists()     │
    │             │              │              ├──────────────>│             │
    │             │              │              │              │ SELECT COUNT(*)
    │             │              │              │              │ FROM users
    │             │              │              │              │ WHERE email = ?
    │             │              │              │              ├────────────>│
    │             │              │              │              │<────────────│
    │             │              │              │<──────────────│ count: 0    │
    │             │              │              │              │             │
    │             │              │              │ 10. create_user()           │
    │             │              │              │  (username, hashed_password, ...)
    │             │              │              ├──────────────>│             │
    │             │              │              │              │             │
    │             │              │              │              │ 11. Hash password
    │             │              │              │              ├─────────────>
    │             │              │              │              │ (werkzeug.generate_password_hash)
    │             │              │              │              │             │
    │             │              │              │              │ 12. INSERT INTO users
    │             │              │              │              │ (username, password, email, ...)
    │             │              │              │              │ VALUES (?, ?, ?, ...)
    │             │              │              │              ├────────────>│
    │             │              │              │              │<────────────│
    │             │              │              │<──────────────│ new_user    │
    │             │              │<─────────────│              │             │
    │             │              │ {success: true, user}       │             │
    │             │<─────────────│              │              │             │
    │             │ 201 Created  │              │              │             │
    │<────────────│              │              │              │             │
    │             │              │              │              │             │
    │ 13. Show success message   │              │              │             │
    │ 14. Refresh user list      │              │              │             │
    │             │              │              │              │             │
```

**Validation Rules:**
- Username: 3-20 characters, alphanumeric, underscore, hyphen
- Password: ≥8 characters, at least one alphanumeric
- Email: Valid email format
- Username unique constraint
- Email unique constraint

---

## 📋 Request Management Sequences

### 4. Create New PIN Request

```
PIN User → Browser → Create Boundary → Create Controller → Request Entity → Database

┌──────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────┐  ┌──────────┐
│PIN User  │  │ Browser │  │ Boundary│  │Controller│  │Entity│  │ Database │
└────┬─────┘  └────┬────┘  └────┬────┘  └────┬─────┘  └──┬───┘  └────┬─────┘
     │             │            │            │            │           │
     │ 1. Fill request form     │            │            │           │
     │ (title, description, service_type, region, date, image)       │
     ├────────────>│            │            │            │           │
     │             │            │            │            │           │
     │             │ 2. Upload image (if provided)        │           │
     │             │    POST /api/upload    │            │           │
     │             ├───────────>│            │            │           │
     │             │            │ Save to /static/uploads/requests/   │
     │             │<───────────│            │            │           │
     │             │ {image_url}│            │            │           │
     │             │            │            │            │           │
     │             │ 3. POST /api/requests  │            │           │
     │             │    Authorization: Bearer {token}    │           │
     │             │    Body: {title, description, ...}  │           │
     │             ├───────────>│            │            │           │
     │             │            │            │            │           │
     │             │            │ 4. create_request(data, token)     │
     │             │            ├───────────>│            │           │
     │             │            │            │            │           │
     │             │            │            │ 5. verify_session_token()
     │             │            │            ├────────────>│           │
     │             │            │            │            │ Decode JWT
     │             │            │            │            │ Get user_id: 39
     │             │            │            │<────────────│           │
     │             │            │            │ user_data  │           │
     │             │            │            │            │           │
     │             │            │            │ 6. Validate required fields
     │             │            │            │ (title, description, service_type)
     │             │            │            │            │           │
     │             │            │            │ 7. Sanitize inputs      │
     │             │            │            │ (title, description)    │
     │             │            │            │            │           │
     │             │            │            │ 8. create_request()     │
     │             │            │            │ (pin_user_id: 39, title, ...)
     │             │            │            ├────────────>│           │
     │             │            │            │            │           │
     │             │            │            │            │ 9. INSERT INTO requests
     │             │            │            │            │ (pin_user_id, title, description,
     │             │            │            │            │  service_type, region, requested_by_date,
     │             │            │            │            │  image_url, status, created_at)
     │             │            │            │            │ VALUES (39, ?, ?, ?, ?, ?, ?, 'ACTIVE', NOW())
     │             │            │            │            ├──────────>│
     │             │            │            │            │<──────────│
     │             │            │            │            │ new_request (id: 15)
     │             │            │            │<────────────│           │
     │             │            │<───────────│            │           │
     │             │            │ {success: true, request}│           │
     │             │<───────────│            │            │           │
     │             │ 201 Created│            │            │           │
     │<────────────│            │            │            │           │
     │             │            │            │            │           │
     │ 10. Show success message │            │            │           │
     │ 11. Redirect to /pin/dashboard        │            │           │
     │             │            │            │            │           │
```

**Image Upload Process:**
1. Frontend validates file (size, type)
2. File uploaded to `/static/uploads/requests/`
3. Unique filename generated: `{timestamp}_{random}.{ext}`
4. URL returned: `/static/uploads/requests/{filename}`
5. URL stored in database

---

### 5. Browse Active Requests (CSR View)

```
CSR Rep → Browser → Get Requests Boundary → Search Controller → Request Entity → Database

┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────┐  ┌──────────┐
│CSR Rep  │  │ Browser │  │ Boundary│  │Controller│  │Entity│  │ Database │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬─────┘  └──┬───┘  └────┬─────┘
     │            │           │           │           │          │
     │ 1. Navigate to /csr/browse         │           │          │
     ├───────────>│           │           │           │          │
     │            │           │           │           │          │
     │            │ 2. useEffect() runs   │           │          │
     │            │    fetchRequests()    │           │          │
     │            │           │           │           │          │
     │            │ 3. GET /api/requests?status=ACTIVE&page=1&limit=50
     │            │    Authorization: Bearer {token}  │          │
     │            ├──────────>│           │           │          │
     │            │           │           │           │          │
     │            │           │ 4. search_requests()  │          │
     │            │           │    (query, filters)   │          │
     │            │           ├──────────>│           │          │
     │            │           │           │           │          │
     │            │           │           │ 5. Build query filters│
     │            │           │           │ - status = 'ACTIVE'   │
     │            │           │           │ - is_archived = false │
     │            │           │           │ - pagination          │
     │            │           │           │           │          │
     │            │           │           │ 6. search_requests()  │
     │            │           │           ├──────────>│          │
     │            │           │           │           │          │
     │            │           │           │           │ 7. SELECT r.*, u.full_name as pin_name
     │            │           │           │           │    FROM requests r
     │            │           │           │           │    LEFT JOIN users u ON r.pin_user_id = u.id
     │            │           │           │           │    WHERE r.status = 'ACTIVE'
     │            │           │           │           │    AND r.is_archived = false
     │            │           │           │           │    ORDER BY r.created_at DESC
     │            │           │           │           │    LIMIT 50 OFFSET 0
     │            │           │           │           ├─────────>│
     │            │           │           │           │<─────────│
     │            │           │           │           │ [11 requests]
     │            │           │           │<──────────│          │
     │            │           │<──────────│           │          │
     │            │           │ {success: true, data: [11 requests]}
     │            │<──────────│           │           │          │
     │            │ 200 OK    │           │           │          │
     │            │           │           │           │          │
     │            │ 8. Parallel: fetchShortlistedIds() │          │
     │            │    GET /api/shortlist │           │          │
     │            ├──────────>│           │           │          │
     │            │           │ [See Shortlist Sequence]         │
     │            │<──────────│           │           │          │
     │            │ [request_ids: 8,10,11,12,13,14,7]│          │
     │            │           │           │           │          │
     │            │ 9. Render request cards           │          │
     │            │    - Mark shortlisted items with ⭐          │
     │            │    - Show SHORTLISTED badge       │          │
     │<───────────│           │           │           │          │
     │            │           │           │           │          │
```

**Filtering Options:**
- Status: ACTIVE, COMPLETED, SUSPENDED
- Service Type: Meal Delivery, Companionship Visit, etc.
- Region: Dropdown of regions
- Date Range: requested_by_date filter
- Search Query: Title/description text search

---

## ⭐ Shortlist Management Sequences

### 6. Add Request to Shortlist

```
CSR Rep → Browser → Add Shortlist Boundary → Add Controller → Shortlist Entity → Database

┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────┐  ┌──────────┐
│CSR Rep  │  │ Browser │  │ Boundary│  │Controller│  │Entity│  │ Database │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬─────┘  └──┬───┘  └────┬─────┘
     │            │           │           │           │          │
     │ 1. Click star (☆) on request card │           │          │
     │    request_id: 13     │           │           │          │
     ├───────────>│           │           │           │          │
     │            │           │           │           │          │
     │            │ 2. handleToggleShortlist(13)      │          │
     │            │           │           │           │          │
     │            │ 3. POST /api/shortlist            │          │
     │            │    Authorization: Bearer {token}  │          │
     │            │    Body: {request_id: 13}         │          │
     │            ├──────────>│           │           │          │
     │            │           │           │           │          │
     │            │           │ 4. add_shortlist(token, data)    │
     │            │           ├──────────>│           │          │
     │            │           │           │           │          │
     │            │           │           │ 5. verify_session_token()
     │            │           │           ├──────────>│          │
     │            │           │           │           │ Decode JWT
     │            │           │           │           │ user_id: 42
     │            │           │           │<──────────│          │
     │            │           │           │           │          │
     │            │           │           │ 6. Validate required field
     │            │           │           │ (request_id)         │
     │            │           │           │           │          │
     │            │           │           │ 7. Check request exists & ACTIVE
     │            │           │           ├──────────>│          │
     │            │           │           │           │ SELECT status
     │            │           │           │           │ FROM requests
     │            │           │           │           │ WHERE id = 13
     │            │           │           │           ├─────────>│
     │            │           │           │           │<─────────│
     │            │           │           │<──────────│ status: ACTIVE
     │            │           │           │           │          │
     │            │           │           │ 8. check_already_shortlisted()
     │            │           │           ├──────────>│          │
     │            │           │           │           │ SELECT COUNT(*)
     │            │           │           │           │ FROM shortlist
     │            │           │           │           │ WHERE csr_user_id=42
     │            │           │           │           │ AND request_id=13
     │            │           │           │           ├─────────>│
     │            │           │           │           │<─────────│
     │            │           │           │<──────────│ count: 0 
     │            │           │           │           │          │
     │            │           │           │ 9. add_to_shortlist()│
     │            │           │           │ (csr_user_id: 42, request_id: 13)
     │            │           │           ├──────────>│          │
     │            │           │           │           │          │
     │            │           │           │           │ 10. INSERT INTO shortlist
     │            │           │           │           │ (csr_user_id, request_id, status, shortlisted_at)
     │            │           │           │           │ VALUES (42, 13, 'SHORTLISTED', NOW())
     │            │           │           │           ├─────────>│
     │            │           │           │           │<─────────│
     │            │           │           │           │ {id: 19, ...}
     │            │           │           │           │          │
     │            │           │           │           │ 11. UPDATE requests
     │            │           │           │           │ SET shortlist_count = shortlist_count + 1
     │            │           │           │           │ WHERE id = 13
     │            │           │           │           ├─────────>│
     │            │           │           │           │<─────────│
     │            │           │           │<──────────│          │
     │            │           │<──────────│           │          │
     │            │           │ {success: true, data: shortlist_entry}
     │            │<──────────│           │           │          │
     │            │ 201 Created           │           │          │
     │            │           │           │           │          │
     │            │ 12. Update local state             │          │
     │            │ setShortlistedIds([...prev, 13])   │          │
     │            │           │           │           │          │
     │            │ 13. Re-fetch shortlist for sync    │          │
     │            │ fetchShortlistedIds()  │           │          │
     │            │           │           │           │          │
     │<───────────│           │           │           │          │
     │ Star changes to ⭐     │           │           │          │
     │ Purple badge appears   │           │           │          │
     │            │           │           │           │          │
```

**Constraints:**
- Request must exist and be ACTIVE
- CSR must not have already shortlisted (UNIQUE constraint)
- JWT token must be valid
- CSR Rep role required

---

### 7. Update Shortlist Status to Completed

```
CSR Rep → Browser → Update Boundary → Update Controller → Shortlist Entity → Database

┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────┐  ┌──────────┐
│CSR Rep  │  │ Browser │  │ Boundary│  │Controller│  │Entity│  │ Database │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬─────┘  └──┬───┘  └────┬─────┘
     │            │           │           │           │          │
     │ 1. Navigate to /csr/shortlist      │           │          │
     │ View shortlisted items │           │           │          │
     ├───────────>│           │           │           │          │
     │            │           │           │           │          │
     │            │ 2. Click "Update Status" on item  │          │
     │            │ shortlist_id: 19      │           │          │
     ├───────────>│           │           │           │          │
     │            │           │           │           │          │
     │            │ 3. Select status: COMPLETED       │          │
     │            │ Enter notes: "Successfully helped"│          │
     │            │ Enter hours: 5.5      │           │          │
     ├───────────>│           │           │           │          │
     │            │           │           │           │          │
     │            │ 4. PATCH /api/shortlist/19/status │          │
     │            │    Authorization: Bearer {token}  │          │
     │            │    Body: {status: "COMPLETED",    │          │
     │            │           notes: "...",            │          │
     │            │           volunteered_hours: 5.5}  │          │
     │            ├──────────>│           │           │          │
     │            │           │           │           │          │
     │            │           │ 5. update_status(token, id, data)│
     │            │           ├──────────>│           │          │
     │            │           │           │           │          │
     │            │           │           │ 6. verify_session_token()
     │            │           │           ├──────────>│          │
     │            │           │           │<──────────│          │
     │            │           │           │ user_id: 42         │
     │            │           │           │           │          │
     │            │           │           │ 7. Validate status value
     │            │           │           │ (SHORTLISTED, IN_PROGRESS, COMPLETED, DECLINED)
     │            │           │           │           │          │
     │            │           │           │ 8. Validate volunteered_hours
     │            │           │           │ (must be > 0)       │
     │            │           │           │           │          │
     │            │           │           │ 9. update_shortlist_status()
     │            │           │           │ (shortlist_id: 19,  │
     │            │           │           │  csr_user_id: 42,   │
     │            │           │           │  status: COMPLETED, │
     │            │           │           │  notes, hours)      │
     │            │           │           ├──────────>│          │
     │            │           │           │           │          │
     │            │           │           │           │ 10. UPDATE shortlist
     │            │           │           │           │ SET status = 'COMPLETED',
     │            │           │           │           │     notes = '...',
     │            │           │           │           │     volunteered_hours = 5.5,
     │            │           │           │           │     completion_date = NOW(),
     │            │           │           │           │     updated_at = NOW()
     │            │           │           │           │ WHERE id = 19
     │            │           │           │           │ AND csr_user_id = 42
     │            │           │           │           ├─────────>│
     │            │           │           │           │<─────────│
     │            │           │           │<──────────│          │
     │            │           │<──────────│           │          │
     │            │           │ {success: true}       │          │
     │            │<──────────│           │           │          │
     │            │ 200 OK    │           │           │          │
     │            │           │           │           │          │
     │            │ 11. Re-fetch shortlist             │          │
     │            │ fetchShortlist()      │           │          │
     │            │           │           │           │          │
     │<───────────│           │           │           │          │
     │ Badge changes to green "COMPLETED" │           │          │
     │ Shows "⏰ 5.5 hours volunteered"    │           │          │
     │            │           │           │           │          │
```

**Status Transitions:**
```
SHORTLISTED → IN_PROGRESS → COMPLETED
            ↘ DECLINED
```

**Business Rules:**
- volunteered_hours required when status = COMPLETED
- completion_date automatically set when COMPLETED
- Only owner (csr_user_id match) can update

---

## 🔄 Common Patterns

### Authentication Flow (Used in All Protected Routes)

```
1. Extract JWT from Authorization header
2. Decode JWT to get user_id and expiration
3. Check if token expired (exp < now())
4. Query database for user by user_id
5. Check if user is_active = true
6. Return user data or error
```

### Pagination Pattern

```
Request: GET /api/endpoint?page=2&limit=20

1. Extract page (default: 1) and limit (default: 50)
2. Calculate offset = (page - 1) * limit
3. Query with LIMIT and OFFSET
4. Return:
   {
     data: [...],
     pagination: {
       page: 2,
       limit: 20,
       total_count: 150,
       total_pages: 8
     }
   }
```

### Error Response Format

```json
{
  "success": false,
  "message": "User-friendly error message",
  "error_code": "INVALID_TOKEN",
  "details": {
    "field": "additional context"
  }
}
```

---

## ❌ Error Handling Sequences

### Invalid Token Error

```
Browser → Boundary → Controller
   │         │           │
   │         │ 1. Extract token
   │         │           │
   │         │ 2. verify_session_token(token)
   │         │           ├──> jwt.decode() → InvalidTokenError
   │         │           │
   │         │<──────────│ {success: false, error_code: "INVALID_TOKEN"}
   │<────────│ 401 Unauthorized
   │
   │ 3. Clear localStorage
   │ 4. Redirect to login page
```

### Duplicate Shortlist Error

```
Browser → Boundary → Controller → Entity → Database
   │         │           │           │         │
   │         │           │           │ INSERT INTO shortlist (UNIQUE constraint)
   │         │           │           │         ├──> IntegrityError: duplicate key
   │         │           │           │<────────│
   │         │           │<──────────│ {success: false, error_code: "ALREADY_SHORTLISTED"}
   │<────────│ 409 Conflict
   │
   │ Show: "You've already shortlisted this request"
```

---

## 📝 Sequence Diagram Tips

### For Creating Diagrams:

1. **Tools**:
   - PlantUML (text-based)
   - Mermaid (markdown-based)
   - draw.io / Lucidchart (visual)
   - Enterprise Architect (professional)

2. **Best Practices**:
   - Show all layers (even if just passing through)
   - Include return values with data types
   - Mark asynchronous calls clearly
   - Show error paths with `alt/else` blocks
   - Use activation bars to show processing time
   - Number steps for easy reference

3. **Common Mistakes**:
   - Skipping middleware/authentication steps
   - Not showing database queries
   - Missing return arrows
   - Unclear lifeline boundaries

---

**Document Version**: 1.0  
**Last Updated**: November 8, 2025  
**Purpose**: Complete sequence diagram documentation for all major flows in CSR Application





