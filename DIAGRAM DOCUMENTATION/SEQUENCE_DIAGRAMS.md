# Complete Sequence Diagrams

## System: Corporate Social Responsibility (CSR) Platform

---

## Table of Contents
1. [Notation Guide](#notation-guide)
2. [Authentication Sequences](#authentication-sequences)
3. [User Account Management Sequences](#user-account-management-sequences)
4. [Profile Management Sequences](#profile-management-sequences)
5. [Role Management Sequences](#role-management-sequences)
6. [Request Management Sequences](#request-management-sequences)
7. [Shortlist Management Sequences](#shortlist-management-sequences)

---

## Notation Guide

```
Actor → Boundary : HTTP Request
Boundary → Controller : Method Call
Controller → Entity : Method Call
Entity → Database : SQL Operation
Database → Entity : Result
Entity → Controller : Return Value
Controller → Boundary : Response
Boundary → Actor : HTTP Response
```

**Symbols:**
- `→` : Synchronous call
- `-->` : Return value
- `[condition]` : Conditional logic
- `loop` : Iteration
- `alt` / `else` : Alternative paths

---

## Authentication Sequences

### SD-AUTH-001: User Login (Success)

```
┌─────┐          ┌─────────┐        ┌─────────────┐      ┌──────┐      ┌──────────┐
│Actor│          │Boundary │        │  Controller │      │Entity│      │ Database │
└──┬──┘          └────┬────┘        └──────┬──────┘      └───┬──┘      └────┬─────┘
   │                  │                    │                  │              │
   │ POST /api/auth/  │                    │                  │              │
   │ login            │                    │                  │              │
   │ {username,       │                    │                  │              │
   │  password,       │                    │                  │              │
   │  role_name}      │                    │                  │              │
   ├─────────────────>│                    │                  │              │
   │                  │                    │                  │              │
   │                  │ create(request_data)                 │              │
   │                  ├───────────────────>│                  │              │
   │                  │                    │                  │              │
   │                  │                    │ validate_request_data()         │
   │                  │                    ├──────┐           │              │
   │                  │                    │      │           │              │
   │                  │                    │<─────┘           │              │
   │                  │                    │                  │              │
   │                  │                    │ User.authenticate(username,     │
   │                  │                    │      password, role_name)       │
   │                  │                    ├─────────────────>│              │
   │                  │                    │                  │              │
   │                  │                    │                  │ SELECT * FROM│
   │                  │                    │                  │ users WHERE  │
   │                  │                    │                  │ username=?   │
   │                  │                    │                  ├─────────────>│
   │                  │                    │                  │              │
   │                  │                    │                  │ user_data    │
   │                  │                    │                  │<─────────────┤
   │                  │                    │                  │              │
   │                  │                    │                  │ verify_password()
   │                  │                    │                  ├──────┐       │
   │                  │                    │                  │      │       │
   │                  │                    │                  │<─────┘       │
   │                  │                    │                  │              │
   │                  │                    │                  │ verify_role()│
   │                  │                    │                  ├──────┐       │
   │                  │                    │                  │      │       │
   │                  │                    │                  │<─────┘       │
   │                  │                    │                  │              │
   │                  │                    │                  │ UPDATE users │
   │                  │                    │                  │ SET last_login=?
   │                  │                    │                  ├─────────────>│
   │                  │                    │                  │              │
   │                  │                    │                  │ success      │
   │                  │                    │                  │<─────────────┤
   │                  │                    │                  │              │
   │                  │                    │     user object  │              │
   │                  │                    │<─────────────────┤              │
   │                  │                    │                  │              │
   │                  │                    │ user.generate_session_token()   │
   │                  │                    ├─────────────────>│              │
   │                  │                    │                  │              │
   │                  │                    │                  │ encode JWT   │
   │                  │                    │                  ├──────┐       │
   │                  │                    │                  │      │       │
   │                  │                    │                  │<─────┘       │
   │                  │                    │                  │              │
   │                  │                    │      jwt_token   │              │
   │                  │                    │<─────────────────┤              │
   │                  │                    │                  │              │
   │                  │  {success: true,   │                  │              │
   │                  │   token,           │                  │              │
   │                  │   user}            │                  │              │
   │                  │<───────────────────┤                  │              │
   │                  │                    │                  │              │
   │ 200 OK           │                    │                  │              │
   │ {success: true,  │                    │                  │              │
   │  token,          │                    │                  │              │
   │  user}           │                    │                  │              │
   │<─────────────────┤                    │                  │              │
   │                  │                    │                  │              │
```

**Key Steps:**
1. Actor sends login credentials to boundary
2. Boundary creates LoginController with request data
3. Controller validates input data
4. Controller calls User.authenticate() factory method
5. User entity queries database for username
6. User entity verifies password hash
7. User entity checks role match
8. User entity updates last_login timestamp
9. User entity returns user object to controller
10. Controller calls user.generate_session_token()
11. User entity generates JWT token
12. Controller returns success response with token and user data
13. Boundary returns HTTP 200 OK with response

---

### SD-AUTH-002: User Login (Failed - Invalid Credentials)

```
┌─────┐          ┌─────────┐        ┌─────────────┐      ┌──────┐      ┌──────────┐
│Actor│          │Boundary │        │  Controller │      │Entity│      │ Database │
└──┬──┘          └────┬────┘        └──────┬──────┘      └───┬──┘      └────┬─────┘
   │                  │                    │                  │              │
   │ POST /login      │                    │                  │              │
   │ {invalid creds}  │                    │                  │              │
   ├─────────────────>│                    │                  │              │
   │                  │                    │                  │              │
   │                  │ create()           │                  │              │
   │                  ├───────────────────>│                  │              │
   │                  │                    │                  │              │
   │                  │                    │ validate_request_data()         │
   │                  │                    ├──────┐           │              │
   │                  │                    │<─────┘           │              │
   │                  │                    │                  │              │
   │                  │                    │ User.authenticate()              │
   │                  │                    ├─────────────────>│              │
   │                  │                    │                  │              │
   │                  │                    │                  │ SELECT * ...│
   │                  │                    │                  ├─────────────>│
   │                  │                    │                  │              │
   │                  │                    │                  │ user_data    │
   │                  │                    │                  │<─────────────┤
   │                  │                    │                  │              │
   │                  │                    │                  │ verify_password()
   │                  │                    │                  ├──────┐       │
   │                  │                    │                  │      │       │
   │                  │                    │                  │<─────┘ FALSE │
   │                  │                    │                  │              │
   │                  │                    │      None        │              │
   │                  │                    │<─────────────────┤              │
   │                  │                    │                  │              │
   │                  │  {success: false,  │                  │              │
   │                  │   message: "Invalid credentials"}     │              │
   │                  │<───────────────────┤                  │              │
   │                  │                    │                  │              │
   │ 401 Unauthorized │                    │                  │              │
   │<─────────────────┤                    │                  │              │
   │                  │                    │                  │              │
```

---

### SD-AUTH-003: Verify Token

```
┌─────┐          ┌─────────┐        ┌─────────────┐      ┌──────┐      ┌──────────┐
│Actor│          │Boundary │        │  Controller │      │Entity│      │ Database │
└──┬──┘          └────┬────┘        └──────┬──────┘      └───┬──┘      └────┬─────┘
   │                  │                    │                  │              │
   │ GET /verify      │                    │                  │              │
   │ Header:          │                    │                  │              │
   │ Authorization:   │                    │                  │              │
   │ Bearer <token>   │                    │                  │              │
   ├─────────────────>│                    │                  │              │
   │                  │                    │                  │              │
   │                  │ create(token)      │                  │              │
   │                  ├───────────────────>│                  │              │
   │                  │                    │                  │              │
   │                  │                    │ User.verify_token(token)        │
   │                  │                    ├─────────────────>│              │
   │                  │                    │                  │              │
   │                  │                    │                  │ decode JWT   │
   │                  │                    │                  ├──────┐       │
   │                  │                    │                  │      │       │
   │                  │                    │                  │<─────┘       │
   │                  │                    │                  │              │
   │                  │                    │                  │ SELECT * FROM│
   │                  │                    │                  │ users WHERE  │
   │                  │                    │                  │ id=?         │
   │                  │                    │                  ├─────────────>│
   │                  │                    │                  │              │
   │                  │                    │                  │ user_data    │
   │                  │                    │                  │<─────────────┤
   │                  │                    │                  │              │
   │                  │                    │     user object  │              │
   │                  │                    │<─────────────────┤              │
   │                  │                    │                  │              │
   │                  │  {success: true,   │                  │              │
   │                  │   user}            │                  │              │
   │                  │<───────────────────┤                  │              │
   │                  │                    │                  │              │
   │ 200 OK           │                    │                  │              │
   │<─────────────────┤                    │                  │              │
   │                  │                    │                  │              │
```

---

## User Account Management Sequences

### SD-USER-001: Create User Account (Success)

```
┌─────────┐      ┌─────────┐      ┌──────────────┐    ┌──────┐    ┌──────────┐
│UserAdmin│      │Boundary │      │  Controller  │    │Entity│    │ Database │
└────┬────┘      └────┬────┘      └──────┬───────┘    └───┬──┘    └────┬─────┘
     │                │                  │                 │            │
     │ POST /api/     │                  │                 │            │
     │ user-accounts  │                  │                 │            │
     │ {username,     │                  │                 │            │
     │  password,     │                  │                 │            │
     │  email,        │                  │                 │            │
     │  full_name,    │                  │                 │            │
     │  role_id}      │                  │                 │            │
     ├───────────────>│                  │                 │            │
     │                │                  │                 │            │
     │                │ create(request_data)               │            │
     │                ├─────────────────>│                 │            │
     │                │                  │                 │            │
     │                │                  │ validate_request_data()      │
     │                │                  ├──────┐          │            │
     │                │                  │      │ Validate:│            │
     │                │                  │      │ - username            │
     │                │                  │      │ - password            │
     │                │                  │      │ - email              │
     │                │                  │      │ - full_name          │
     │                │                  │      │ - role_id            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ sanitize_data() │            │
     │                │                  ├──────┐          │            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ create_user_object()         │
     │                │                  ├──────┐          │            │
     │                │                  │      │ new User()            │
     │                │                  │      │ set attributes        │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ user.save()     │            │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ validate() │
     │                │                  │                 ├──────┐     │
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ check_uniqueness()
     │                │                  │                 ├──────┐     │
     │                │                  │                 │      │     │
     │                │                  │                 │      │ SELECT * FROM
     │                │                  │                 │      │ users WHERE
     │                │                  │                 │      │ username=?
     │                │                  │                 │      ├────>│
     │                │                  │                 │      │     │
     │                │                  │                 │      │ empty
     │                │                  │                 │      │<────┤
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ hash_password()
     │                │                  │                 ├──────┐     │
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ INSERT INTO│
     │                │                  │                 │ users(...) │
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ new user_id│
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │      true       │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │                  │ user.log_activity()          │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ INSERT INTO│
     │                │                  │                 │ user_activity_log
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ success    │
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │      true       │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │ {success: true,  │                 │            │
     │                │  data: user,     │                 │            │
     │                │  message}        │                 │            │
     │                │<─────────────────┤                 │            │
     │                │                  │                 │            │
     │ 201 Created    │                  │                 │            │
     │<───────────────┤                  │                 │            │
     │                │                  │                 │            │
```

**Key Steps:**
1. User Admin sends user creation data
2. Controller validates all input fields
3. Controller sanitizes data
4. Controller creates User entity and sets attributes
5. Controller calls user.save()
6. User entity validates data
7. User entity checks username/email uniqueness
8. User entity hashes password
9. User entity inserts into database
10. User entity logs activity
11. Controller returns success response
12. Boundary returns HTTP 201 Created

---

### SD-USER-002: Update User Account

```
┌─────────┐      ┌─────────┐      ┌──────────────┐    ┌──────┐    ┌──────────┐
│UserAdmin│      │Boundary │      │  Controller  │    │Entity│    │ Database │
└────┬────┘      └────┬────┘      └──────┬───────┘    └───┬──┘    └────┬─────┘
     │                │                  │                 │            │
     │ PUT /api/      │                  │                 │            │
     │ user-accounts/ │                  │                 │            │
     │ {user_id}      │                  │                 │            │
     │ {updates}      │                  │                 │            │
     ├───────────────>│                  │                 │            │
     │                │                  │                 │            │
     │                │ create(user_id, request_data)      │            │
     │                ├─────────────────>│                 │            │
     │                │                  │                 │            │
     │                │                  │ User.find(user_id)           │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ SELECT *   │
     │                │                  │                 │ WHERE id=? │
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ user_data  │
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │   user object   │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │                  │ validate_request_data()      │
     │                │                  ├──────┐          │            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ sanitize_data() │            │
     │                │                  ├──────┐          │            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ update user attributes       │
     │                │                  ├──────┐          │            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ user.save()     │            │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ validate() │
     │                │                  │                 ├──────┐     │
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ check_uniqueness()
     │                │                  │                 ├──────┐     │
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ UPDATE users
     │                │                  │                 │ SET ... WHERE id=?
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ success    │
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │      true       │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │ {success: true}  │                 │            │
     │                │<─────────────────┤                 │            │
     │                │                  │                 │            │
     │ 200 OK         │                  │                 │            │
     │<───────────────┤                  │                 │            │
     │                │                  │                 │            │
```

---

### SD-USER-003: Suspend User Account

```
┌─────────┐      ┌─────────┐      ┌──────────────┐    ┌──────┐    ┌──────────┐
│UserAdmin│      │Boundary │      │  Controller  │    │Entity│    │ Database │
└────┬────┘      └────┬────┘      └──────┬───────┘    └───┬──┘    └────┬─────┘
     │                │                  │                 │            │
     │ POST /api/     │                  │                 │            │
     │ user-accounts/ │                  │                 │            │
     │ {user_id}/     │                  │                 │            │
     │ suspend        │                  │                 │            │
     ├───────────────>│                  │                 │            │
     │                │                  │                 │            │
     │                │ create(user_id)  │                 │            │
     │                ├─────────────────>│                 │            │
     │                │                  │                 │            │
     │                │                  │ User.find(user_id)           │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ SELECT *   │
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ user_data  │
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │   user object   │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │                  │ user.deactivate()            │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ set is_active=false
     │                │                  │                 ├──────┐     │
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ UPDATE users
     │                │                  │                 │ SET is_active=false
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ success    │
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │      true       │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │ {success: true}  │                 │            │
     │                │<─────────────────┤                 │            │
     │                │                  │                 │            │
     │ 200 OK         │                  │                 │            │
     │<───────────────┤                  │                 │            │
     │                │                  │                 │            │
```

---

### SD-USER-004: Search User Accounts

```
┌─────────┐      ┌─────────┐      ┌──────────────┐    ┌──────┐    ┌──────────┐
│UserAdmin│      │Boundary │      │  Controller  │    │Entity│    │ Database │
└────┬────┘      └────┬────┘      └──────┬───────┘    └───┬──┘    └────┬─────┘
     │                │                  │                 │            │
     │ GET /api/      │                  │                 │            │
     │ user-accounts/ │                  │                 │            │
     │ search?        │                  │                 │            │
     │ username=...   │                  │                 │            │
     ├───────────────>│                  │                 │            │
     │                │                  │                 │            │
     │                │ create(search_criteria)            │            │
     │                ├─────────────────>│                 │            │
     │                │                  │                 │            │
     │                │                  │ User.search(**criteria)      │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ SELECT * FROM
     │                │                  │                 │ users WHERE
     │                │                  │                 │ username ILIKE '%...'
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ users_data │
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │   List[User]    │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │ {success: true,  │                 │            │
     │                │  data: [users]}  │                 │            │
     │                │<─────────────────┤                 │            │
     │                │                  │                 │            │
     │ 200 OK         │                  │                 │            │
     │<───────────────┤                  │                 │            │
     │                │                  │                 │            │
```

---

## Profile Management Sequences

### SD-PROFILE-001: Create User Profile

```
┌─────────┐      ┌─────────┐      ┌──────────────┐    ┌────────┐    ┌──────────┐
│UserAdmin│      │Boundary │      │  Controller  │    │ Profile│    │ Database │
└────┬────┘      └────┬────┘      └──────┬───────┘    └───┬────┘    └────┬─────┘
     │                │                  │                  │             │
     │ POST /api/     │                  │                  │             │
     │ user-profiles  │                  │                  │             │
     │ {profile_name, │                  │                  │             │
     │  description}  │                  │                  │             │
     ├───────────────>│                  │                  │             │
     │                │                  │                  │             │
     │                │ create(request_data)                │             │
     │                ├─────────────────>│                  │             │
     │                │                  │                  │             │
     │                │                  │ validate_request_data()        │
     │                │                  ├──────┐           │             │
     │                │                  │<─────┘           │             │
     │                │                  │                  │             │
     │                │                  │ sanitize_data()  │             │
     │                │                  ├──────┐           │             │
     │                │                  │<─────┘           │             │
     │                │                  │                  │             │
     │                │                  │ create_profile_object()        │
     │                │                  ├──────┐           │             │
     │                │                  │      │ new Profile()            │
     │                │                  │<─────┘           │             │
     │                │                  │                  │             │
     │                │                  │ profile.save()   │             │
     │                │                  ├─────────────────>│             │
     │                │                  │                  │             │
     │                │                  │                  │ validate()  │
     │                │                  │                  ├──────┐      │
     │                │                  │                  │<─────┘      │
     │                │                  │                  │             │
     │                │                  │                  │ check_uniqueness()
     │                │                  │                  ├──────┐      │
     │                │                  │                  │      │      │
     │                │                  │                  │      │ SELECT *
     │                │                  │                  │      │ WHERE
     │                │                  │                  │      │ profile_name=?
     │                │                  │                  │      ├─────>│
     │                │                  │                  │      │      │
     │                │                  │                  │      │ empty│
     │                │                  │                  │      │<─────┤
     │                │                  │                  │<─────┘      │
     │                │                  │                  │             │
     │                │                  │                  │ INSERT INTO │
     │                │                  │                  │ profiles(...)
     │                │                  │                  ├────────────>│
     │                │                  │                  │             │
     │                │                  │                  │ new profile_id
     │                │                  │                  │<────────────┤
     │                │                  │                  │             │
     │                │                  │      true        │             │
     │                │                  │<─────────────────┤             │
     │                │                  │                  │             │
     │                │ {success: true}  │                  │             │
     │                │<─────────────────┤                  │             │
     │                │                  │                  │             │
     │ 201 Created    │                  │                  │             │
     │<───────────────┤                  │                  │             │
     │                │                  │                  │             │
```

---

## Role Management Sequences

### SD-ROLE-001: Create Role

```
┌─────────┐      ┌─────────┐      ┌──────────────┐    ┌──────┐    ┌──────────┐
│UserAdmin│      │Boundary │      │  Controller  │    │ Role │    │ Database │
└────┬────┘      └────┬────┘      └──────┬───────┘    └───┬──┘    └────┬─────┘
     │                │                  │                 │            │
     │ POST /api/roles│                  │                 │            │
     │ {role_name,    │                  │                 │            │
     │  role_code,    │                  │                 │            │
     │  description,  │                  │                 │            │
     │  dashboard_    │                  │                 │            │
     │  route}        │                  │                 │            │
     ├───────────────>│                  │                 │            │
     │                │                  │                 │            │
     │                │ create(request_data)               │            │
     │                ├─────────────────>│                 │            │
     │                │                  │                 │            │
     │                │                  │ validate_request_data()      │
     │                │                  ├──────┐          │            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ sanitize_data() │            │
     │                │                  ├──────┐          │            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ create_role_object()         │
     │                │                  ├──────┐          │            │
     │                │                  │      │ new Role()            │
     │                │                  │<─────┘          │            │
     │                │                  │                 │            │
     │                │                  │ role.save()     │            │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ validate() │
     │                │                  │                 ├──────┐     │
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ check_uniqueness()
     │                │                  │                 ├──────┐     │
     │                │                  │                 │<─────┘     │
     │                │                  │                 │            │
     │                │                  │                 │ INSERT INTO│
     │                │                  │                 │ roles(...) │
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ new role_id│
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │      true       │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │ {success: true}  │                 │            │
     │                │<─────────────────┤                 │            │
     │                │                  │                 │            │
     │ 201 Created    │                  │                 │            │
     │<───────────────┤                  │                 │            │
     │                │                  │                 │            │
```

---

### SD-ROLE-002: Get All Roles

```
┌─────────┐      ┌─────────┐      ┌──────────────┐    ┌──────┐    ┌──────────┐
│UserAdmin│      │Boundary │      │  Controller  │    │ Role │    │ Database │
└────┬────┘      └────┬────┘      └──────┬───────┘    └───┬──┘    └────┬─────┘
     │                │                  │                 │            │
     │ GET /api/roles │                  │                 │            │
     ├───────────────>│                  │                 │            │
     │                │                  │                 │            │
     │                │ create()         │                 │            │
     │                ├─────────────────>│                 │            │
     │                │                  │                 │            │
     │                │                  │ Role.all()      │            │
     │                │                  ├────────────────>│            │
     │                │                  │                 │            │
     │                │                  │                 │ SELECT *   │
     │                │                  │                 │ FROM roles │
     │                │                  │                 ├───────────>│
     │                │                  │                 │            │
     │                │                  │                 │ roles_data │
     │                │                  │                 │<───────────┤
     │                │                  │                 │            │
     │                │                  │   List[Role]    │            │
     │                │                  │<────────────────┤            │
     │                │                  │                 │            │
     │                │ {success: true,  │                 │            │
     │                │  data: [roles]}  │                 │            │
     │                │<─────────────────┤                 │            │
     │                │                  │                 │            │
     │ 200 OK         │                  │                 │            │
     │<───────────────┤                  │                 │            │
     │                │                  │                 │            │
```

---

## Request Management Sequences

### SD-REQUEST-001: Create New PIN Request (Success)

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐
│PIN │      │Boundary │      │  Controller  │    │  User   │    │ Request  │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬────┘    └────┬─────┘    └────┬─────┘
  │              │                  │                   │              │               │
  │ POST /api/   │                  │                   │              │               │
  │ requests     │                  │                   │              │               │
  │ Headers:     │                  │                   │              │               │
  │ Authorization│                  │                   │              │               │
  │ Body:        │                  │                   │              │               │
  │ {title,      │                  │                   │              │               │
  │  description,│                  │                   │              │               │
  │  service_type│                  │                   │              │               │
  │  region,     │                  │                   │              │               │
  │  requested_  │                  │                   │              │               │
  │  by_date,    │                  │                   │              │               │
  │  image}      │                  │                   │              │               │
  ├─────────────>│                  │                   │              │               │
  │              │                  │                   │              │               │
  │              │ create(token, request_data)          │              │               │
  │              ├─────────────────>│                   │              │               │
  │              │                  │                   │              │               │
  │              │                  │ authenticate_user()              │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │      │ User.verify_token()       │               │
  │              │                  │      ├───────────>│              │               │
  │              │                  │      │            │              │               │
  │              │                  │      │            │ decode JWT   │               │
  │              │                  │      │            ├──────┐       │               │
  │              │                  │      │            │<─────┘       │               │
  │              │                  │      │            │              │               │
  │              │                  │      │            │ SELECT * FROM│               │
  │              │                  │      │            │ users WHERE  │               │
  │              │                  │      │            │ id=?         │               │
  │              │                  │      │            ├──────────────────────────────>│
  │              │                  │      │            │              │               │
  │              │                  │      │            │              │ user_data     │
  │              │                  │      │            │<──────────────────────────────┤
  │              │                  │      │            │              │               │
  │              │                  │      │   user     │              │               │
  │              │                  │      │<───────────┤              │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ validate_request_data()          │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ process_image_upload()           │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │      │ save_base64_image()       │               │
  │              │                  │      │ - decode base64           │               │
  │              │                  │      │ - generate filename       │               │
  │              │                  │      │ - save to file system     │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ create_request_object()          │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │      │ new Request()             │               │
  │              │                  │      │ set attributes            │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ request.save()    │              │               │
  │              │                  ├──────────────────────────────────>│               │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ validate()    │
  │              │                  │                   │              ├──────┐        │
  │              │                  │                   │              │<─────┘        │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ validate_pin_user()
  │              │                  │                   │              ├──────┐        │
  │              │                  │                   │              │      │ SELECT *
  │              │                  │                   │              │      │ FROM users
  │              │                  │                   │              │      │ WHERE id=?
  │              │                  │                   │              │      │ AND role_id=2
  │              │                  │                   │              │      ├───────>│
  │              │                  │                   │              │      │        │
  │              │                  │                   │              │      │ user   │
  │              │                  │                   │              │      │<───────┤
  │              │                  │                   │              │<─────┘        │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ validate_service_type()
  │              │                  │                   │              ├──────┐        │
  │              │                  │                   │              │      │ SELECT *
  │              │                  │                   │              │      │ FROM service_types
  │              │                  │                   │              │      │ WHERE service_name=?
  │              │                  │                   │              │      ├───────>│
  │              │                  │                   │              │      │        │
  │              │                  │                   │              │      │ found  │
  │              │                  │                   │              │      │<───────┤
  │              │                  │                   │              │<─────┘        │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ INSERT INTO   │
  │              │                  │                   │              │ requests(...) │
  │              │                  │                   │              ├──────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ new request_id│
  │              │                  │                   │              │<──────────────┤
  │              │                  │                   │              │               │
  │              │                  │        true       │              │               │
  │              │                  │<──────────────────────────────────┤               │
  │              │                  │                   │              │               │
  │              │ {success: true,  │                   │              │               │
  │              │  data: request}  │                   │              │               │
  │              │<─────────────────┤                   │              │               │
  │              │                  │                   │              │               │
  │ 201 Created  │                  │                   │              │               │
  │<─────────────┤                  │                   │              │               │
  │              │                  │                   │              │               │
```

**Key Steps:**
1. PIN user sends request with authentication token
2. Controller verifies token and authenticates user
3. Controller validates all input fields
4. Controller processes base64 image upload
5. Controller creates Request entity and sets attributes
6. Controller calls request.save()
7. Request entity validates data
8. Request entity validates PIN user (role_id = 2)
9. Request entity validates service type exists
10. Request entity inserts into database with status = ACTIVE
11. Controller returns success response
12. Boundary returns HTTP 201 Created

---

### SD-REQUEST-002: View PIN Request

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌─────────┐    ┌──────────┐
│PIN │      │Boundary │      │  Controller  │    │ Request │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬────┘    └────┬─────┘
  │              │                  │                  │             │
  │ GET /api/    │                  │                  │             │
  │ requests/    │                  │                  │             │
  │ {request_id} │                  │                  │             │
  ├─────────────>│                  │                  │             │
  │              │                  │                  │             │
  │              │ create(request_id)                  │             │
  │              ├─────────────────>│                  │             │
  │              │                  │                  │             │
  │              │                  │ Request.find(request_id)        │
  │              │                  ├─────────────────>│             │
  │              │                  │                  │             │
  │              │                  │                  │ SELECT * FROM
  │              │                  │                  │ requests WHERE
  │              │                  │                  │ id=?        │
  │              │                  │                  ├────────────>│
  │              │                  │                  │             │
  │              │                  │                  │ request_data│
  │              │                  │                  │<────────────┤
  │              │                  │                  │             │
  │              │                  │   request object │             │
  │              │                  │<─────────────────┤             │
  │              │                  │                  │             │
  │              │ {success: true,  │                  │             │
  │              │  data: request}  │                  │             │
  │              │<─────────────────┤                  │             │
  │              │                  │                  │             │
  │ 200 OK       │                  │                  │             │
  │<─────────────┤                  │                  │             │
  │              │                  │                  │             │
```

---

### SD-REQUEST-003: Search PIN Requests (CSR User)

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌─────────┐    ┌──────────┐
│CSR │      │Boundary │      │  Controller  │    │ Request │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬────┘    └────┬─────┘
  │              │                  │                  │             │
  │ GET /api/    │                  │                  │             │
  │ requests/    │                  │                  │             │
  │ search?      │                  │                  │             │
  │ service_type=│                  │                  │             │
  │ ...&region=..│                  │                  │             │
  ├─────────────>│                  │                  │             │
  │              │                  │                  │             │
  │              │ create(search_criteria)             │             │
  │              ├─────────────────>│                  │             │
  │              │                  │                  │             │
  │              │                  │ Request.search(**criteria)     │
  │              │                  ├─────────────────>│             │
  │              │                  │                  │             │
  │              │                  │                  │ SELECT * FROM
  │              │                  │                  │ requests WHERE
  │              │                  │                  │ service_type=?
  │              │                  │                  │ AND region=?
  │              │                  │                  │ AND status='ACTIVE'
  │              │                  │                  │ AND is_archived=false
  │              │                  │                  ├────────────>│
  │              │                  │                  │             │
  │              │                  │                  │ requests_data
  │              │                  │                  │<────────────┤
  │              │                  │                  │             │
  │              │                  │   List[Request]  │             │
  │              │                  │<─────────────────┤             │
  │              │                  │                  │             │
  │              │ {success: true,  │                  │             │
  │              │  data: [requests]}                  │             │
  │              │<─────────────────┤                  │             │
  │              │                  │                  │             │
  │ 200 OK       │                  │                  │             │
  │<─────────────┤                  │                  │             │
  │              │                  │                  │             │
```

---

### SD-REQUEST-004: Increment View Count

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌─────────┐    ┌──────────┐
│CSR │      │Boundary │      │  Controller  │    │ Request │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬────┘    └────┬─────┘
  │              │                  │                  │             │
  │ POST /api/   │                  │                  │             │
  │ requests/    │                  │                  │             │
  │ {request_id}/│                  │                  │             │
  │ view         │                  │                  │             │
  ├─────────────>│                  │                  │             │
  │              │                  │                  │             │
  │              │ create(request_id)                  │             │
  │              ├─────────────────>│                  │             │
  │              │                  │                  │             │
  │              │                  │ Request.find(request_id)        │
  │              │                  ├─────────────────>│             │
  │              │                  │                  │             │
  │              │                  │                  │ SELECT *    │
  │              │                  │                  ├────────────>│
  │              │                  │                  │             │
  │              │                  │                  │ request_data│
  │              │                  │                  │<────────────┤
  │              │                  │                  │             │
  │              │                  │   request object │             │
  │              │                  │<─────────────────┤             │
  │              │                  │                  │             │
  │              │                  │ request.increment_view_count()  │
  │              │                  ├─────────────────>│             │
  │              │                  │                  │             │
  │              │                  │                  │ view_count++│
  │              │                  │                  ├──────┐      │
  │              │                  │                  │<─────┘      │
  │              │                  │                  │             │
  │              │                  │                  │ UPDATE requests
  │              │                  │                  │ SET view_count=?
  │              │                  │                  │ WHERE id=?  │
  │              │                  │                  ├────────────>│
  │              │                  │                  │             │
  │              │                  │                  │ success     │
  │              │                  │                  │<────────────┤
  │              │                  │                  │             │
  │              │                  │      true        │             │
  │              │                  │<─────────────────┤             │
  │              │                  │                  │             │
  │              │ {success: true}  │                  │             │
  │              │<─────────────────┤                  │             │
  │              │                  │                  │             │
  │ 200 OK       │                  │                  │             │
  │<─────────────┤                  │                  │             │
  │              │                  │                  │             │
```

---

## Shortlist Management Sequences

### SD-SHORTLIST-001: Add Request to Shortlist (Success)

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│CSR │      │Boundary │      │  Controller  │    │ Shortlist│    │ Request │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬─────┘    └────┬────┘    └────┬─────┘
  │              │                  │                   │              │               │
  │ POST /api/   │                  │                   │              │               │
  │ shortlist    │                  │                   │              │               │
  │ Headers:     │                  │                   │              │               │
  │ Authorization│                  │                   │              │               │
  │ Body:        │                  │                   │              │               │
  │ {request_id, │                  │                   │              │               │
  │  notes}      │                  │                   │              │               │
  ├─────────────>│                  │                   │              │               │
  │              │                  │                   │              │               │
  │              │ create(token, request_data)          │              │               │
  │              ├─────────────────>│                   │              │               │
  │              │                  │                   │              │               │
  │              │                  │ authenticate_user()              │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │      │ User.verify_token()       │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ validate_request_data()          │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ create_shortlist_object()        │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │      │ new Shortlist()           │               │
  │              │                  │      │ set attributes            │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ shortlist.save()  │              │               │
  │              │                  ├──────────────────>│              │               │
  │              │                  │                   │              │               │
  │              │                  │                   │ validate()   │               │
  │              │                  │                   ├──────┐       │               │
  │              │                  │                   │<─────┘       │               │
  │              │                  │                   │              │               │
  │              │                  │                   │ check_duplicate()            │
  │              │                  │                   ├──────┐       │               │
  │              │                  │                   │      │ SELECT * FROM
  │              │                  │                   │      │ shortlist WHERE
  │              │                  │                   │      │ csr_user_id=?
  │              │                  │                   │      │ AND request_id=?
  │              │                  │                   │      ├──────────────────────>│
  │              │                  │                   │      │       │               │
  │              │                  │                   │      │ empty │               │
  │              │                  │                   │      │<──────────────────────┤
  │              │                  │                   │<─────┘       │               │
  │              │                  │                   │              │               │
  │              │                  │                   │ validate_request_active()    │
  │              │                  │                   ├──────┐       │               │
  │              │                  │                   │      │ SELECT * FROM
  │              │                  │                   │      │ requests WHERE
  │              │                  │                   │      │ id=? AND
  │              │                  │                   │      │ status='ACTIVE'
  │              │                  │                   │      ├──────────────────────>│
  │              │                  │                   │      │       │               │
  │              │                  │                   │      │ found │               │
  │              │                  │                   │      │<──────────────────────┤
  │              │                  │                   │<─────┘       │               │
  │              │                  │                   │              │               │
  │              │                  │                   │ INSERT INTO  │               │
  │              │                  │                   │ shortlist(...) │               │
  │              │                  │                   ├──────────────────────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ new shortlist_id
  │              │                  │                   │<──────────────────────────────┤
  │              │                  │                   │              │               │
  │              │                  │                   │ Request.find(request_id)     │
  │              │                  │                   ├─────────────>│               │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ SELECT *      │
  │              │                  │                   │              ├──────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ request_data  │
  │              │                  │                   │              │<──────────────┤
  │              │                  │                   │              │               │
  │              │                  │                   │   request    │               │
  │              │                  │                   │<─────────────┤               │
  │              │                  │                   │              │               │
  │              │                  │                   │ request.increment_shortlist_count()
  │              │                  │                   ├─────────────>│               │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ UPDATE requests
  │              │                  │                   │              │ SET shortlist_count++
  │              │                  │                   │              ├──────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ success       │
  │              │                  │                   │              │<──────────────┤
  │              │                  │                   │              │               │
  │              │                  │                   │      true    │               │
  │              │                  │                   │<─────────────┤               │
  │              │                  │                   │              │               │
  │              │                  │        true       │              │               │
  │              │                  │<──────────────────┤              │               │
  │              │                  │                   │              │               │
  │              │ {success: true,  │                   │              │               │
  │              │  data: shortlist}│                   │              │               │
  │              │<─────────────────┤                   │              │               │
  │              │                  │                   │              │               │
  │ 201 Created  │                  │                   │              │               │
  │<─────────────┤                  │                   │              │               │
  │              │                  │                   │              │               │
```

**Key Steps:**
1. CSR user sends shortlist request with token
2. Controller authenticates user
3. Controller validates request data
4. Controller creates Shortlist entity
5. Controller calls shortlist.save()
6. Shortlist entity validates data
7. Shortlist entity checks for duplicate (same CSR + request)
8. Shortlist entity validates request is ACTIVE
9. Shortlist entity inserts into database with status = SHORTLISTED
10. Shortlist entity loads request and increments shortlist_count
11. Controller returns success response
12. Boundary returns HTTP 201 Created

---

### SD-SHORTLIST-002: Get Shortlist (CSR User)

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌──────────┐    ┌──────────┐
│CSR │      │Boundary │      │  Controller  │    │Shortlist │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬─────┘    └────┬─────┘
  │              │                  │                   │               │
  │ GET /api/    │                  │                   │               │
  │ shortlist    │                  │                   │               │
  │ Headers:     │                  │                   │               │
  │ Authorization│                  │                   │               │
  ├─────────────>│                  │                   │               │
  │              │                  │                   │               │
  │              │ create(token)    │                   │               │
  │              ├─────────────────>│                   │               │
  │              │                  │                   │               │
  │              │                  │ authenticate_user()               │
  │              │                  ├──────┐            │               │
  │              │                  │<─────┘            │               │
  │              │                  │                   │               │
  │              │                  │ Shortlist.by_csr_user(user_id)    │
  │              │                  ├──────────────────>│               │
  │              │                  │                   │               │
  │              │                  │                   │ SELECT * FROM │
  │              │                  │                   │ shortlist     │
  │              │                  │                   │ LEFT JOIN requests
  │              │                  │                   │ WHERE csr_user_id=?
  │              │                  │                   ├──────────────>│
  │              │                  │                   │               │
  │              │                  │                   │ shortlist_data│
  │              │                  │                   │ (with requests)
  │              │                  │                   │<──────────────┤
  │              │                  │                   │               │
  │              │                  │   List[Shortlist] │               │
  │              │                  │<──────────────────┤               │
  │              │                  │                   │               │
  │              │ {success: true,  │                   │               │
  │              │  data: [shortlist]}                  │               │
  │              │<─────────────────┤                   │               │
  │              │                  │                   │               │
  │ 200 OK       │                  │                   │               │
  │<─────────────┤                  │                   │               │
  │              │                  │                   │               │
```

---

### SD-SHORTLIST-003: Update Shortlist Status

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌──────────┐    ┌──────────┐
│CSR │      │Boundary │      │  Controller  │    │Shortlist │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬─────┘    └────┬─────┘
  │              │                  │                   │               │
  │ PUT /api/    │                  │                   │               │
  │ shortlist/   │                  │                   │               │
  │ {shortlist_id}│                 │                   │               │
  │ /status      │                  │                   │               │
  │ Headers:     │                  │                   │               │
  │ Authorization│                  │                   │               │
  │ Body:        │                  │                   │               │
  │ {status,     │                  │                   │               │
  │  notes,      │                  │                   │               │
  │  volunteered_│                  │                   │               │
  │  hours}      │                  │                   │               │
  ├─────────────>│                  │                   │               │
  │              │                  │                   │               │
  │              │ create(token, shortlist_id, data)    │               │
  │              ├─────────────────>│                   │               │
  │              │                  │                   │               │
  │              │                  │ authenticate_user()               │
  │              │                  ├──────┐            │               │
  │              │                  │<─────┘            │               │
  │              │                  │                   │               │
  │              │                  │ Shortlist.find(shortlist_id)      │
  │              │                  ├──────────────────>│               │
  │              │                  │                   │               │
  │              │                  │                   │ SELECT * FROM │
  │              │                  │                   │ shortlist     │
  │              │                  │                   │ WHERE id=?    │
  │              │                  │                   ├──────────────>│
  │              │                  │                   │               │
  │              │                  │                   │ shortlist_data│
  │              │                  │                   │<──────────────┤
  │              │                  │                   │               │
  │              │                  │   shortlist object│               │
  │              │                  │<──────────────────┤               │
  │              │                  │                   │               │
  │              │                  │ verify ownership  │               │
  │              │                  ├──────┐            │               │
  │              │                  │<─────┘            │               │
  │              │                  │                   │               │
  │              │                  │ validate_request_data()           │
  │              │                  ├──────┐            │               │
  │              │                  │<─────┘            │               │
  │              │                  │                   │               │
  │              │                  │ update attributes │               │
  │              │                  ├──────┐            │               │
  │              │                  │      │ shortlist.status = ...     │
  │              │                  │      │ shortlist.notes = ...      │
  │              │                  │      │ shortlist.volunteered_hours = ...
  │              │                  │<─────┘            │               │
  │              │                  │                   │               │
  │              │                  │ shortlist.save()  │               │
  │              │                  ├──────────────────>│               │
  │              │                  │                   │               │
  │              │                  │                   │ validate()    │
  │              │                  │                   ├──────┐        │
  │              │                  │                   │<─────┘        │
  │              │                  │                   │               │
  │              │                  │                   │ UPDATE shortlist
  │              │                  │                   │ SET status=?,
  │              │                  │                   │ notes=?,
  │              │                  │                   │ volunteered_hours=?,
  │              │                  │                   │ updated_at=now()
  │              │                  │                   │ WHERE id=?    │
  │              │                  │                   ├──────────────>│
  │              │                  │                   │               │
  │              │                  │                   │ success       │
  │              │                  │                   │<──────────────┤
  │              │                  │                   │               │
  │              │                  │        true       │               │
  │              │                  │<──────────────────┤               │
  │              │                  │                   │               │
  │              │ {success: true,  │                   │               │
  │              │  data: shortlist}│                   │               │
  │              │<─────────────────┤                   │               │
  │              │                  │                   │               │
  │ 200 OK       │                  │                   │               │
  │<─────────────┤                  │                   │               │
  │              │                  │                   │               │
```

---

### SD-SHORTLIST-004: Remove from Shortlist

```
┌────┐      ┌─────────┐      ┌──────────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│CSR │      │Boundary │      │  Controller  │    │Shortlist │    │ Request │    │ Database │
└─┬──┘      └────┬────┘      └──────┬───────┘    └────┬─────┘    └────┬────┘    └────┬─────┘
  │              │                  │                   │              │               │
  │ DELETE /api/ │                  │                   │              │               │
  │ shortlist/   │                  │                   │              │               │
  │ {shortlist_id}                  │                   │              │               │
  │ Headers:     │                  │                   │              │               │
  │ Authorization│                  │                   │              │               │
  ├─────────────>│                  │                   │              │               │
  │              │                  │                   │              │               │
  │              │ create(token, shortlist_id)          │              │               │
  │              ├─────────────────>│                   │              │               │
  │              │                  │                   │              │               │
  │              │                  │ authenticate_user()              │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ Shortlist.find(shortlist_id)     │               │
  │              │                  ├──────────────────>│              │               │
  │              │                  │                   │              │               │
  │              │                  │                   │ SELECT *     │               │
  │              │                  │                   ├──────────────────────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ shortlist_data│
  │              │                  │                   │<──────────────────────────────┤
  │              │                  │                   │              │               │
  │              │                  │   shortlist object│              │               │
  │              │                  │<──────────────────┤              │               │
  │              │                  │                   │              │               │
  │              │                  │ verify ownership & status         │               │
  │              │                  ├──────┐            │              │               │
  │              │                  │<─────┘            │              │               │
  │              │                  │                   │              │               │
  │              │                  │ shortlist.delete()│              │               │
  │              │                  ├──────────────────>│              │               │
  │              │                  │                   │              │               │
  │              │                  │                   │ DELETE FROM  │               │
  │              │                  │                   │ shortlist    │               │
  │              │                  │                   │ WHERE id=?   │               │
  │              │                  │                   ├──────────────────────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ success       │
  │              │                  │                   │<──────────────────────────────┤
  │              │                  │                   │              │               │
  │              │                  │                   │ Request.find(request_id)     │
  │              │                  │                   ├─────────────>│               │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ SELECT *      │
  │              │                  │                   │              ├──────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ request_data  │
  │              │                  │                   │              │<──────────────┤
  │              │                  │                   │              │               │
  │              │                  │                   │   request    │               │
  │              │                  │                   │<─────────────┤               │
  │              │                  │                   │              │               │
  │              │                  │                   │ request.decrement_shortlist_count()
  │              │                  │                   ├─────────────>│               │
  │              │                  │                   │              │               │
  │              │                  │                   │              │ UPDATE requests
  │              │                  │                   │              │ SET shortlist_count--
  │              │                  │                   │              ├──────────────>│
  │              │                  │                   │              │               │
  │              │                  │                   │              │ success       │
  │              │                  │                   │              │<──────────────┤
  │              │                  │                   │              │               │
  │              │                  │                   │      true    │               │
  │              │                  │                   │<─────────────┤               │
  │              │                  │                   │              │               │
  │              │                  │        true       │              │               │
  │              │                  │<──────────────────┤              │               │
  │              │                  │                   │              │               │
  │              │ {success: true}  │                   │              │               │
  │              │<─────────────────┤                   │              │               │
  │              │                  │                   │              │               │
  │ 200 OK       │                  │                   │              │               │
  │<─────────────┤                  │                   │              │               │
  │              │                  │                   │              │               │
```

---

## Error Handling Sequences

### SD-ERROR-001: Validation Error Example

```
┌─────┐      ┌─────────┐      ┌──────────────┐
│Actor│      │Boundary │      │  Controller  │
└──┬──┘      └────┬────┘      └──────┬───────┘
   │              │                  │
   │ POST /api/   │                  │
   │ (invalid data)                  │
   ├─────────────>│                  │
   │              │                  │
   │              │ create(data)     │
   │              ├─────────────────>│
   │              │                  │
   │              │                  │ validate_request_data()
   │              │                  ├──────┐
   │              │                  │      │ Validation fails
   │              │                  │<─────┘
   │              │                  │
   │              │  {success: false,│
   │              │   error_code:    │
   │              │   'VALIDATION_   │
   │              │   ERROR',        │
   │              │   message: '...'} │
   │              │<─────────────────┤
   │              │                  │
   │ 400 Bad      │                  │
   │ Request      │                  │
   │<─────────────┤                  │
   │              │                  │
```

---

### SD-ERROR-002: Authentication Error Example

```
┌─────┐      ┌─────────┐      ┌──────────────┐    ┌──────┐
│Actor│      │Boundary │      │  Controller  │    │Entity│
└──┬──┘      └────┬────┘      └──────┬───────┘    └───┬──┘
   │              │                  │                 │
   │ POST /api/   │                  │                 │
   │ (invalid token)                 │                 │
   ├─────────────>│                  │                 │
   │              │                  │                 │
   │              │ create(token)    │                 │
   │              ├─────────────────>│                 │
   │              │                  │                 │
   │              │                  │ User.verify_token()
   │              │                  ├────────────────>│
   │              │                  │                 │
   │              │                  │                 │ decode JWT
   │              │                  │                 ├──────┐
   │              │                  │                 │      │ EXPIRED
   │              │                  │                 │<─────┘
   │              │                  │                 │
   │              │                  │      None       │
   │              │                  │<────────────────┤
   │              │                  │                 │
   │              │  {success: false,│                 │
   │              │   error_code:    │                 │
   │              │   'INVALID_TOKEN'│                 │
   │              │   message: '...'} │                 │
   │              │<─────────────────┤                 │
   │              │                  │                 │
   │ 401          │                  │                 │
   │ Unauthorized │                  │                 │
   │<─────────────┤                  │                 │
   │              │                  │                 │
```

---

## Summary of Sequence Patterns

### Common Patterns Across All Sequences

1. **Authentication Flow**:
   - Token extracted from Authorization header
   - User.verify_token() called
   - JWT decoded and validated
   - User loaded from database
   - User object returned or None if invalid

2. **Validation Flow**:
   - Input data validated in controller
   - Data sanitized
   - Business rules checked
   - Database constraints verified

3. **Entity Operations**:
   - Factory methods create/load entities
   - Instance methods perform operations
   - Database operations encapsulated in entities
   - Results returned to controller

4. **Response Flow**:
   - Controller formats response
   - Boundary returns HTTP response
   - Success: 200/201 with data
   - Error: 400/401/500 with error details

5. **Error Handling**:
   - Validation errors: 400 Bad Request
   - Authentication errors: 401 Unauthorized
   - Business logic errors: 409 Conflict
   - System errors: 500 Internal Server Error

---

## End of Sequence Diagrams

