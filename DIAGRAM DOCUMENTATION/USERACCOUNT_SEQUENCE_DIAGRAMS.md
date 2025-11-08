# User Account Management - Sequence Diagrams

## Overview
This document provides comprehensive sequence diagrams for all User Account Management operations following the BCE (Boundary-Control-Entity) pattern.

---

## Table of Contents
1. [Create User Account](#1-create-user-account)
2. [View All Users](#2-view-all-users)
3. [View Single User](#3-view-single-user)
4. [Update User Account](#4-update-user-account)
5. [Suspend User Account](#5-suspend-user-account)
6. [Activate User Account](#6-activate-user-account)
7. [Delete User Account](#7-delete-user-account)
8. [Search Users](#8-search-users)

---

## 1. Create User Account

### Success Flow (201 Created)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │CreateUserAcc │    │CreateUserAccount     │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ POST /api/      │                        │                      │               │
     │ userAccount     │                        │                      │               │
     │ {username,      │                        │                      │               │
     │  password,      │                        │                      │               │
     │  email,         │                        │                      │               │
     │  full_name,     │                        │                      │               │
     │  role_id}       │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ @require_role(         │                      │               │
     │                 │   USER_ADMIN)          │                      │               │
     │                 │ [Verify JWT token]     │                      │               │
     │                 │                        │                      │               │
     │                 │ request.get_json()     │                      │               │
     │                 │ payload = {data}       │                      │               │
     │                 │                        │                      │               │
     │                 │ create(payload)        │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ 1. Validate HTTP     │               │
     │                 │                        │    format            │               │
     │                 │                        │    if not data:      │               │
     │                 │                        │      return 400      │               │
     │                 │                        │                      │               │
     │                 │                        │ 2. Call validation   │               │
     │                 │                        │    function          │               │
     │                 │                        │                      │               │
     │                 │                        │ validate_create_     │               │
     │                 │                        │   user_data(data)    │               │
     │                 │                        │ ┌──────────────────┐ │               │
     │                 │                        │ │ Validation Steps:│ │               │
     │                 │                        │ │ 1. Check data    │ │               │
     │                 │                        │ │ 2. Required      │ │               │
     │                 │                        │ │    fields        │ │               │
     │                 │                        │ │ 3. Format:       │ │               │
     │                 │                        │ │    - username    │ │               │
     │                 │                        │ │    - password    │ │               │
     │                 │                        │ │    - email       │ │               │
     │                 │                        │ │    - full_name   │ │               │
     │                 │                        │ │    - role_id     │ │               │
     │                 │                        │ └──────────────────┘ │               │
     │                 │                        │                      │               │
     │                 │                        │ username_exists()?   │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT * FROM│
     │                 │                        │                      │ users WHERE  │
     │                 │                        │                      │ username=?   │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ result       │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ False (not exists)   │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ email_exists()?      │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT * FROM│
     │                 │                        │                      │ users WHERE  │
     │                 │                        │                      │ email=?      │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ result       │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ False (not exists)   │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ (True, "")           │               │
     │                 │                        │ [Validation passed]  │               │
     │                 │                        │                      │               │
     │                 │                        │ 3. Sanitize input    │               │
     │                 │                        │    Sanitizers.       │               │
     │                 │                        │    sanitize_user_    │               │
     │                 │                        │    data(data)        │               │
     │                 │                        │                      │               │
     │                 │                        │ 4. Call Entity layer │               │
     │                 │                        │                      │               │
     │                 │                        │ create_user(         │               │
     │                 │                        │   username,          │               │
     │                 │                        │   password,          │               │
     │                 │                        │   email,             │               │
     │                 │                        │   full_name,         │               │
     │                 │                        │   role_id)           │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ 1. Hash      │
     │                 │                        │                      │    password  │
     │                 │                        │                      │    (pbkdf2)  │
     │                 │                        │                      │               │
     │                 │                        │                      │ 2. Prepare   │
     │                 │                        │                      │    user_data │
     │                 │                        │                      │               │
     │                 │                        │                      │ 3. Final     │
     │                 │                        │                      │    safety    │
     │                 │                        │                      │    checks    │
     │                 │                        │                      │               │
     │                 │                        │                      │ INSERT INTO  │
     │                 │                        │                      │ users (...)  │
     │                 │                        │                      │ VALUES (...)  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ created_user │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ {'data':             │               │
     │                 │                        │  created_user}       │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ 5. Log activity      │               │
     │                 │                        │    (best-effort)     │               │
     │                 │                        │                      │               │
     │                 │                        │ log_user_activity()  │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ INSERT INTO  │
     │                 │                        │                      │ activity_log │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ success      │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ logged               │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ 6. Format response   │               │
     │                 │                        │    ResponseHelpers.  │               │
     │                 │                        │    success_response()│               │
     │                 │                        │                      │               │
     │                 │ (response, 201)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │                 │ jsonify(response)      │                      │               │
     │                 │                        │                      │               │
     │ 201 Created     │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  data: {...},   │                        │                      │               │
     │  message: "User │                        │                      │               │
     │  account        │                        │                      │               │
     │  created        │                        │                      │               │
     │  successfully"} │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

### Error Flow: Username Already Exists (409 Conflict)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │CreateUserAcc │    │CreateUserAccount     │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ POST /api/      │                        │                      │               │
     │ userAccount     │                        │                      │               │
     │ {username:      │                        │                      │               │
     │  "existing"}    │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ create(payload)        │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ validate_create_     │               │
     │                 │                        │   user_data(data)    │               │
     │                 │                        │                      │               │
     │                 │                        │ username_exists()?   │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT * FROM│
     │                 │                        │                      │ users WHERE  │
     │                 │                        │                      │ username=?   │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ [user found] │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ True (exists!)       │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ (False, "Username    │               │
     │                 │                        │  already taken")     │               │
     │                 │                        │                      │               │
     │                 │                        │ ResponseHelpers.     │               │
     │                 │                        │   error_response(    │               │
     │                 │                        │   VALIDATION_ERROR)  │               │
     │                 │                        │                      │               │
     │                 │ (response, 400)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 400 Bad Request │                        │                      │               │
     │ {success: false,│                        │                      │               │
     │  message: "The  │                        │                      │               │
     │  username is    │                        │                      │               │
     │  already taken",│                        │                      │               │
     │  error_code:    │                        │                      │               │
     │  "VALIDATION_   │                        │                      │               │
     │  ERROR"}        │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## 2. View All Users

### Success Flow (200 OK)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │ViewUserAcc   │    │ViewUserAccount       │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ GET /api/       │                        │                      │               │
     │ userAccount     │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ @require_role(         │                      │               │
     │                 │   USER_ADMIN)          │                      │               │
     │                 │ [Verify JWT token]     │                      │               │
     │                 │                        │                      │               │
     │                 │ view_all()             │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ get_all_users()      │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *,    │
     │                 │                        │                      │ roles(...)   │
     │                 │                        │                      │ FROM users   │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ [users list] │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ users_list           │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ Build response:      │               │
     │                 │                        │ {success: true,      │               │
     │                 │                        │  data: users,        │               │
     │                 │                        │  count: len(users)}  │               │
     │                 │                        │                      │               │
     │                 │ (response, 200)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │                 │ jsonify(response)      │                      │               │
     │                 │                        │                      │               │
     │ 200 OK          │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  data: [...],   │                        │                      │               │
     │  count: 37}     │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## 3. View Single User

### Success Flow (200 OK)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │ViewUserAcc   │    │ViewUserAccount       │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ GET /api/       │                        │                      │               │
     │ userAccount/42  │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ view_one(42)           │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ get_user_by_id(42)   │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *,    │
     │                 │                        │                      │ roles(...)   │
     │                 │                        │                      │ FROM users   │
     │                 │                        │                      │ WHERE id=42  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ user_data    │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ user_dict            │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │ (response, 200)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 200 OK          │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  data: {...}}   │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

### Error Flow: User Not Found (404)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │ViewUserAcc   │    │ViewUserAccount       │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ GET /api/       │                        │                      │               │
     │ userAccount/999 │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ view_one(999)          │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ get_user_by_id(999)  │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *     │
     │                 │                        │                      │ WHERE id=999 │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ [] (empty)   │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ None                 │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ if not user:         │               │
     │                 │                        │   return 404         │               │
     │                 │                        │                      │               │
     │                 │ (response, 404)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 404 Not Found   │                        │                      │               │
     │ {success: false,│                        │                      │               │
     │  message: "User │                        │                      │               │
     │  account not    │                        │                      │               │
     │  found"}        │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## 4. Update User Account

### Success Flow (200 OK)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │UpdateUserAcc │    │UpdateUserAccount     │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ PUT /api/       │                        │                      │               │
     │ userAccount/42  │                        │                      │               │
     │ {email:         │                        │                      │               │
     │  "new@mail.com",│                        │                      │               │
     │  full_name:     │                        │                      │               │
     │  "New Name"}    │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ @require_role(         │                      │               │
     │                 │   USER_ADMIN)          │                      │               │
     │                 │                        │                      │               │
     │                 │ update(42, payload)    │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ 1. Validate data     │               │
     │                 │                        │    presence          │               │
     │                 │                        │                      │               │
     │                 │                        │ 2. Check user exists │               │
     │                 │                        │                      │               │
     │                 │                        │ get_user_by_id(42)   │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *     │
     │                 │                        │                      │ WHERE id=42  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ user_data    │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ user_dict            │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ 3. Sanitize input    │               │
     │                 │                        │    Sanitizers.       │               │
     │                 │                        │    sanitize_user_    │               │
     │                 │                        │    data()            │               │
     │                 │                        │                      │               │
     │                 │                        │ 4. Validate updates  │               │
     │                 │                        │                      │               │
     │                 │                        │ validate_update_     │               │
     │                 │                        │   user_data(data, 42)│               │
     │                 │                        │ ┌──────────────────┐ │               │
     │                 │                        │ │ - Validate email │ │               │
     │                 │                        │ │   format         │ │               │
     │                 │                        │ │ - Check email    │ │               │
     │                 │                        │ │   uniqueness     │ │               │
     │                 │                        │ │ - Validate       │ │               │
     │                 │                        │ │   full_name      │ │               │
     │                 │                        │ └──────────────────┘ │               │
     │                 │                        │                      │               │
     │                 │                        │ get_by_email()?      │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *     │
     │                 │                        │                      │ WHERE email=?│
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ None or      │
     │                 │                        │                      │ same user    │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ OK (unique or same)  │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ (True, updates_dict) │               │
     │                 │                        │                      │               │
     │                 │                        │ 5. Update in DB      │               │
     │                 │                        │                      │               │
     │                 │                        │ update_user(42,      │               │
     │                 │                        │   updates)           │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ UPDATE users │
     │                 │                        │                      │ SET ...      │
     │                 │                        │                      │ WHERE id=42  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ updated_user │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ updated_user_dict    │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ 6. Log activity      │               │
     │                 │                        │                      │               │
     │                 │                        │ log_user_activity()  │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ INSERT INTO  │
     │                 │                        │                      │ activity_log │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │ logged               │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ 7. Format response   │               │
     │                 │                        │                      │               │
     │                 │ (response, 200)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 200 OK          │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  data: {...},   │                        │                      │               │
     │  message: "User │                        │                      │               │
     │  account updated│                        │                      │               │
     │  successfully"} │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## 5. Suspend User Account

### Success Flow (200 OK)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │SuspendUserAcc│    │SuspendUserAccount    │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ PUT /api/       │                        │                      │               │
     │ userAccount/42/ │                        │                      │               │
     │ suspend         │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ @require_role(         │                      │               │
     │                 │   USER_ADMIN)          │                      │               │
     │                 │                        │                      │               │
     │                 │ suspend(42)            │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ update_user(42,      │               │
     │                 │                        │   {'is_active':      │               │
     │                 │                        │    False})           │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ UPDATE users │
     │                 │                        │                      │ SET          │
     │                 │                        │                      │ is_active=   │
     │                 │                        │                      │ FALSE        │
     │                 │                        │                      │ WHERE id=42  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ updated_user │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ updated_user_dict    │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ Build response       │               │
     │                 │                        │                      │               │
     │                 │ (response, 200)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 200 OK          │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  data: {...},   │                        │                      │               │
     │  message: "User │                        │                      │               │
     │  account        │                        │                      │               │
     │  suspended      │                        │                      │               │
     │  successfully"} │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## 6. Activate User Account

### Success Flow (200 OK)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │SuspendUserAcc│    │SuspendUserAccount    │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ PUT /api/       │                        │                      │               │
     │ userAccount/42/ │                        │                      │               │
     │ activate        │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ activate(42)           │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ update_user(42,      │               │
     │                 │                        │   {'is_active':      │               │
     │                 │                        │    True})            │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ UPDATE users │
     │                 │                        │                      │ SET          │
     │                 │                        │                      │ is_active=   │
     │                 │                        │                      │ TRUE         │
     │                 │                        │                      │ WHERE id=42  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ updated_user │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ updated_user_dict    │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │ (response, 200)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 200 OK          │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  message: "User │                        │                      │               │
     │  account        │                        │                      │               │
     │  activated      │                        │                      │               │
     │  successfully"} │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## 7. Delete User Account

### Success Flow (200 OK)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │SuspendUserAcc│    │SuspendUserAccount    │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ DELETE /api/    │                        │                      │               │
     │ userAccount/42/ │                        │                      │               │
     │ delete          │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ delete(42)             │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ 1. Check user exists │               │
     │                 │                        │                      │               │
     │                 │                        │ get_user_by_id(42)   │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *     │
     │                 │                        │                      │ WHERE id=42  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ user_data    │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ user_dict            │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ 2. Delete user       │               │
     │                 │                        │                      │               │
     │                 │                        │ delete_user(42)      │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ DELETE FROM  │
     │                 │                        │                      │ users        │
     │                 │                        │                      │ WHERE id=42  │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ success      │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ True                 │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │ (response, 200)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 200 OK          │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  message: "User │                        │                      │               │
     │  account deleted│                        │                      │               │
     │  successfully"} │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

### Error Flow: User Not Found (404)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │SuspendUserAcc│    │SuspendUserAccount    │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ DELETE /api/    │                        │                      │               │
     │ userAccount/999/│                        │                      │               │
     │ delete          │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ delete(999)            │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ get_user_by_id(999)  │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *     │
     │                 │                        │                      │ WHERE id=999 │
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ [] (empty)   │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │ None                 │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ if not user:         │               │
     │                 │                        │   return 404         │               │
     │                 │                        │                      │               │
     │                 │ (response, 404)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 404 Not Found   │                        │                      │               │
     │ {success: false,│                        │                      │               │
     │  message: "User │                        │                      │               │
     │  account not    │                        │                      │               │
     │  found"}        │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## 8. Search Users

### Success Flow (200 OK)

```
┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────┐    ┌──────────┐
│  Admin   │    │SearchUserAcc │    │SearchUserAccount     │    │ User     │    │ Supabase │
│  (UI)    │    │Boundary      │    │Controller            │    │ Entity   │    │   DB     │
└────┬─────┘    └──────┬───────┘    └──────────┬───────────┘    └────┬─────┘    └────┬─────┘
     │                 │                        │                      │               │
     │ POST /api/      │                        │                      │               │
     │ userAccount/    │                        │                      │               │
     │ search          │                        │                      │               │
     │ {username:      │                        │                      │               │
     │  "john",        │                        │                      │               │
     │  email: "",     │                        │                      │               │
     │  full_name: ""} │                        │                      │               │
     ├────────────────>│                        │                      │               │
     │                 │                        │                      │               │
     │                 │ search(payload)        │                      │               │
     │                 ├───────────────────────>│                      │               │
     │                 │                        │                      │               │
     │                 │                        │ Extract criteria:    │               │
     │                 │                        │ - username: "john"   │               │
     │                 │                        │ - email: ""          │               │
     │                 │                        │ - full_name: ""      │               │
     │                 │                        │                      │               │
     │                 │                        │ search_users(        │               │
     │                 │                        │   username="john",   │               │
     │                 │                        │   email="",          │               │
     │                 │                        │   full_name="")      │               │
     │                 │                        ├─────────────────────>│               │
     │                 │                        │                      │               │
     │                 │                        │                      │ SELECT *,    │
     │                 │                        │                      │ roles(...)   │
     │                 │                        │                      │ FROM users   │
     │                 │                        │                      │ WHERE        │
     │                 │                        │                      │ username     │
     │                 │                        │                      │ ILIKE '%john%'│
     │                 │                        │                      ├─────────────>│
     │                 │                        │                      │               │
     │                 │                        │                      │ matching_    │
     │                 │                        │                      │ users        │
     │                 │                        │                      │<─────────────┤
     │                 │                        │                      │               │
     │                 │                        │                      │ Client-side  │
     │                 │                        │                      │ filter for   │
     │                 │                        │                      │ email &      │
     │                 │                        │                      │ full_name    │
     │                 │                        │                      │               │
     │                 │                        │ results_list         │               │
     │                 │                        │<─────────────────────┤               │
     │                 │                        │                      │               │
     │                 │                        │ Build response:      │               │
     │                 │                        │ {success: true,      │               │
     │                 │                        │  data: results,      │               │
     │                 │                        │  count: len(results)}│               │
     │                 │                        │                      │               │
     │                 │ (response, 200)        │                      │               │
     │                 │<───────────────────────┤                      │               │
     │                 │                        │                      │               │
     │ 200 OK          │                        │                      │               │
     │ {success: true, │                        │                      │               │
     │  data: [...],   │                        │                      │               │
     │  count: 3}      │                        │                      │               │
     │<────────────────┤                        │                      │               │
     │                 │                        │                      │               │
```

---

## Summary of All Operations

| Operation | HTTP Method | Endpoint | Success Code | Error Codes |
|-----------|-------------|----------|--------------|-------------|
| Create User | POST | `/api/userAccount` | 201 | 400, 409, 500 |
| View All Users | GET | `/api/userAccount` | 200 | 500 |
| View Single User | GET | `/api/userAccount/<id>` | 200 | 404, 500 |
| Update User | PUT | `/api/userAccount/<id>` | 200 | 400, 404, 500 |
| Suspend User | PUT | `/api/userAccount/<id>/suspend` | 200 | 400, 500 |
| Activate User | PUT | `/api/userAccount/<id>/activate` | 200 | 400, 500 |
| Delete User | DELETE | `/api/userAccount/<id>/delete` | 200 | 404, 500 |
| Search Users | POST | `/api/userAccount/search` | 200 | 500 |

---

## Common Patterns

### Authentication Flow (All Endpoints)
1. User sends request with JWT token in Authorization header
2. `@require_role(USER_ADMIN)` decorator intercepts request
3. Token is verified using `User.verify_session_token()`
4. If valid and role matches, request proceeds
5. If invalid, returns 401 Unauthorized

### Validation Pattern (Create/Update)
1. Check data presence (not empty)
2. Validate required fields
3. Format validation (username, email, etc.)
4. Uniqueness checks (database queries)
5. Sanitize input
6. Process in Entity layer

### Error Handling Pattern
1. Try-catch blocks at each layer
2. Specific error codes for different failures
3. Consistent response format via ResponseHelpers
4. Detailed error messages for debugging
5. Generic messages for users (security)

### Activity Logging Pattern
1. Best-effort logging after successful operations
2. Failures don't block main operation
3. Logs include: user_id, activity_type, details
4. Used for audit trail

---

## Notes

- All endpoints require `USER_ADMIN` role
- JWT tokens expire after 24 hours
- Password hashing uses pbkdf2:sha256
- Email uniqueness allows same user to keep their email on update
- Search uses server-side filtering for username, client-side for email/full_name
- Activity logging is best-effort (failures silently ignored)
- All responses follow consistent format via ResponseHelpers

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-08  
**Module**: User Account Management  
**Architecture**: BCE (Boundary-Control-Entity)


