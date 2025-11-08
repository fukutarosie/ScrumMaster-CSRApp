# User Account Management - BCE Class Diagrams

## Overview
This document provides comprehensive BCE (Boundary-Control-Entity) class diagrams for the User Account Management module, which handles all user account operations including creation, viewing, updating, searching, and suspension/activation/deletion.

---

## Table of Contents
1. [Complete BCE Architecture](#complete-bce-architecture)
2. [Boundary Layer Classes](#boundary-layer-classes)
3. [Control Layer Classes](#control-layer-classes)
4. [Entity Layer Classes](#entity-layer-classes)
5. [Helper Classes](#helper-classes)
6. [Database Schema](#database-schema)

---

## Complete BCE Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER ACCOUNT MODULE                                │
│                         BCE Architecture Overview                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              BOUNDARY LAYER                                  │
│                         (HTTP Request/Response)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐                        │
│  │ CreateUserAccount    │  │ ViewUserAccount      │                        │
│  │ Boundary             │  │ Boundary             │                        │
│  ├──────────────────────┤  ├──────────────────────┤                        │
│  │ POST /api/           │  │ GET /api/            │                        │
│  │   userAccount        │  │   userAccount        │                        │
│  │                      │  │ GET /api/            │                        │
│  │ + create()           │  │   userAccount/:id    │                        │
│  │   : jsonify()        │  │                      │                        │
│  │                      │  │ + view_all()         │                        │
│  │ @require_role(       │  │   : jsonify()        │                        │
│  │   USER_ADMIN)        │  │ + view_one(user_id)  │                        │
│  └──────────────────────┘  │   : jsonify()        │                        │
│                             │                      │                        │
│                             │ @require_role(       │                        │
│                             │   USER_ADMIN)        │                        │
│                             └──────────────────────┘                        │
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐                        │
│  │ UpdateUserAccount    │  │ SuspendUserAccount   │                        │
│  │ Boundary             │  │ Boundary             │                        │
│  ├──────────────────────┤  ├──────────────────────┤                        │
│  │ PUT /api/            │  │ PUT /api/            │                        │
│  │   userAccount/:id    │  │   userAccount/:id/   │                        │
│  │                      │  │   suspend            │                        │
│  │ + update(user_id)    │  │ PUT /api/            │                        │
│  │   : jsonify()        │  │   userAccount/:id/   │                        │
│  │                      │  │   activate           │                        │
│  │ @require_role(       │  │ DELETE /api/         │                        │
│  │   USER_ADMIN)        │  │   userAccount/:id/   │                        │
│  └──────────────────────┘  │   delete             │                        │
│                             │                      │                        │
│  ┌──────────────────────┐  │ + suspend(user_id)   │                        │
│  │ SearchUserAccount    │  │   : jsonify()        │                        │
│  │ Boundary             │  │ + activate(user_id)  │                        │
│  ├──────────────────────┤  │   : jsonify()        │                        │
│  │ POST /api/           │  │ + delete(user_id)    │                        │
│  │   userAccount/search │  │   : jsonify()        │                        │
│  │                      │  │                      │                        │
│  │ + search()           │  │ @require_role(       │                        │
│  │   : jsonify()        │  │   USER_ADMIN)        │                        │
│  │                      │  └──────────────────────┘                        │
│  │ @require_role(       │                                                   │
│  │   USER_ADMIN)        │                                                   │
│  └──────────────────────┘                                                   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ calls
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CONTROL LAYER                                   │
│                         (Business Logic & Validation)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ CreateUserAccountController                                           │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + create(data: dict) -> Tuple[dict, int]                             │  │
│  │   - Validates HTTP format                                             │  │
│  │   - Calls validate_create_user_data()                                 │  │
│  │   - Sanitizes input                                                   │  │
│  │   - Calls User.create_user()                                          │  │
│  │   - Logs user activity                                                │  │
│  │   - Returns formatted response                                        │  │
│  │                                                                        │  │
│  │ Return Codes:                                                          │  │
│  │   - 201: User created successfully                                    │  │
│  │   - 400: EMPTY_BODY, VALIDATION_ERROR, CREATION_FAILED                │  │
│  │   - 409: USERNAME_EXISTS, EMAIL_EXISTS                                │  │
│  │   - 500: SERVER_ERROR                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ validate_create_user_data(data: dict) -> Tuple[bool, str]            │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ Validation Steps:                                                     │  │
│  │   1. Check data presence                                              │  │
│  │   2. Validate required fields (username, password, email,             │  │
│  │      full_name, role_id)                                              │  │
│  │   3. Format validation:                                               │  │
│  │      - Validators.validate_username()                                 │  │
│  │      - Validators.validate_password()                                 │  │
│  │      - Validators.validate_email()                                    │  │
│  │      - Validators.validate_full_name()                                │  │
│  │      - Validators.validate_role_id()                                  │  │
│  │   4. Uniqueness checks:                                               │  │
│  │      - User.username_exists()                                         │  │
│  │      - User.email_exists()                                            │  │
│  │                                                                        │  │
│  │ Returns: (is_valid: bool, error_message: str)                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ ViewUserAccountController                                             │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + view_all() -> Tuple[dict, int]                                     │  │
│  │   - Calls User.get_all_users()                                        │  │
│  │   - Returns list with count                                           │  │
│  │                                                                        │  │
│  │ + view_one(user_id: int) -> Tuple[dict, int]                         │  │
│  │   - Calls User.get_user_by_id()                                       │  │
│  │   - Returns user data or 404                                          │  │
│  │                                                                        │  │
│  │ Return Codes:                                                          │  │
│  │   - 200: Success                                                      │  │
│  │   - 404: User not found                                               │  │
│  │   - 500: SERVER_ERROR                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ UpdateUserAccountController                                           │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + update(user_id: int, data: dict) -> Tuple[dict, int]               │  │
│  │   - Validates data presence                                           │  │
│  │   - Checks user exists (User.get_user_by_id())                        │  │
│  │   - Sanitizes input                                                   │  │
│  │   - Calls validate_update_user_data()                                 │  │
│  │   - Calls User.update_user()                                          │  │
│  │   - Logs activity                                                     │  │
│  │   - Returns formatted response                                        │  │
│  │                                                                        │  │
│  │ Return Codes:                                                          │  │
│  │   - 200: Updated successfully                                         │  │
│  │   - 400: EMPTY_BODY, VALIDATION_ERROR, UPDATE_FAILED                  │  │
│  │   - 404: USER_NOT_FOUND                                               │  │
│  │   - 500: SERVER_ERROR                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ validate_update_user_data(data: dict, current_user_id: int)          │  │
│  │                          -> Tuple[bool, Union[str, dict]]             │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ Validates optional fields:                                            │  │
│  │   - email (format + uniqueness check)                                 │  │
│  │   - full_name (format)                                                │  │
│  │   - role_id (format)                                                  │  │
│  │                                                                        │  │
│  │ Returns:                                                               │  │
│  │   - (True, updates_dict) on success                                   │  │
│  │   - (False, error_message) on failure                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ SuspendUserAccountController                                          │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + suspend(user_id: int) -> Tuple[dict, int]                          │  │
│  │   - Calls User.update_user(user_id, {'is_active': False})            │  │
│  │                                                                        │  │
│  │ + activate(user_id: int) -> Tuple[dict, int]                         │  │
│  │   - Calls User.update_user(user_id, {'is_active': True})             │  │
│  │                                                                        │  │
│  │ + delete(user_id: int) -> Tuple[dict, int]                           │  │
│  │   - Checks user exists                                                │  │
│  │   - Calls User.delete_user()                                          │  │
│  │                                                                        │  │
│  │ Return Codes:                                                          │  │
│  │   - 200: Success                                                      │  │
│  │   - 400: Operation failed                                             │  │
│  │   - 404: User not found (delete only)                                 │  │
│  │   - 500: SERVER_ERROR                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ SearchUserAccountController                                           │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + search(data: dict) -> Tuple[dict, int]                             │  │
│  │   - Extracts search criteria (username, email, full_name)             │  │
│  │   - Calls User.search_users()                                         │  │
│  │   - Returns results with count                                        │  │
│  │                                                                        │  │
│  │ Return Codes:                                                          │  │
│  │   - 200: Success (even if no results)                                 │  │
│  │   - 500: SERVER_ERROR                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ uses
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               ENTITY LAYER                                   │
│                         (Database Operations)                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ User                                                                  │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ Database Table: users                                                 │  │
│  │                                                                        │  │
│  │ Attributes:                                                            │  │
│  │   - id: int                                                           │  │
│  │   - username: str                                                     │  │
│  │   - password: str (hashed)                                            │  │
│  │   - email: str                                                        │  │
│  │   - full_name: str                                                    │  │
│  │   - role_id: int (FK -> roles.id)                                     │  │
│  │   - is_active: bool                                                   │  │
│  │   - last_login: str (ISO datetime)                                    │  │
│  │   - created_at: str (ISO datetime)                                    │  │
│  │                                                                        │  │
│  │ Methods:                                                               │  │
│  │                                                                        │  │
│  │ + create_user(username: str, password: str, email: str,              │  │
│  │               full_name: str, role_id: int) -> Optional[Dict]         │  │
│  │   Description: Create new user account                                │  │
│  │   Process:                                                             │  │
│  │     1. Hash password using pbkdf2:sha256                              │  │
│  │     2. Prepare user_data dict with all fields                         │  │
│  │     3. Final safety checks (username_exists, email_exists)            │  │
│  │     4. Insert into database                                           │  │
│  │     5. Handle duplicate detection                                     │  │
│  │   Returns:                                                             │  │
│  │     - {'data': user_dict} on success                                  │  │
│  │     - {'error': 'USERNAME_EXISTS', 'message': '...'} on dup username  │  │
│  │     - {'error': 'EMAIL_EXISTS', 'message': '...'} on dup email        │  │
│  │     - {'error': 'DB_INSERT_FAILED', 'message': '...'} on DB failure   │  │
│  │     - {'error': 'EXCEPTION', 'message': '...'} on exception           │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + get_user_by_id(user_id: int) -> Optional[Dict]                     │  │
│  │   Description: Retrieve user by ID with role information              │  │
│  │   Returns: User dict with nested roles object, or None                │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + get_user_by_username(username: str) -> Optional[Dict]              │  │
│  │   Description: Retrieve user by username                              │  │
│  │   Uses: execute_with_retry() for connection resilience               │  │
│  │   Returns: User dict or None                                          │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + get_user_by_email(email: str) -> Optional[Dict]                    │  │
│  │   Description: Retrieve user by email                                 │  │
│  │   Uses: execute_with_retry() for connection resilience               │  │
│  │   Returns: User dict or None                                          │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + get_by_email(email: str) -> Optional[Dict]                         │  │
│  │   Description: Compatibility alias for get_user_by_email()            │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + get_all_users() -> List[Dict]                                      │  │
│  │   Description: Retrieve all users with role information               │  │
│  │   Returns: List of user dicts with nested roles                       │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + update_user(user_id: int, updates: Dict) -> Optional[Dict]         │  │
│  │   Description: Update user details                                    │  │
│  │   Process:                                                             │  │
│  │     1. Hash password if being updated                                 │  │
│  │     2. Execute update query                                           │  │
│  │     3. Return updated user or verify user still exists                │  │
│  │   Returns: Updated user dict or None                                  │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + delete_user(user_id: int) -> bool                                  │  │
│  │   Description: Permanently delete user account                        │  │
│  │   Returns: True if successful, False otherwise                        │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + search_users(username: str = '', email: str = '',                  │  │
│  │                full_name: str = '') -> List[Dict]                     │  │
│  │   Description: Search users by multiple criteria                      │  │
│  │   Process:                                                             │  │
│  │     1. Query with username (server-side ilike)                        │  │
│  │     2. Filter email and full_name (client-side)                       │  │
│  │   Returns: List of matching user dicts                                │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + username_exists(username: str) -> bool                             │  │
│  │   Description: Check if username already exists                       │  │
│  │   Returns: True if exists, False otherwise                            │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + email_exists(email: str) -> bool                                   │  │
│  │   Description: Check if email already exists                          │  │
│  │   Returns: True if exists, False otherwise                            │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + activate_user(user_id: int) -> Optional[Dict]                      │  │
│  │   Description: Activate user account                                  │  │
│  │   Calls: update_user(user_id, {'is_active': True})                   │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + deactivate_user(user_id: int) -> Optional[Dict]                    │  │
│  │   Description: Deactivate user account                                │  │
│  │   Calls: update_user(user_id, {'is_active': False})                  │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + log_user_activity(user_id: int, activity_type: str,                │  │
│  │                     activity_details: str) -> None                    │  │
│  │   Description: Log user activity for audit trail                      │  │
│  │   Note: Best-effort logging (failures are silently ignored)           │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + get_user_complete_details(user_id: int) -> Optional[Dict]          │  │
│  │   Description: Get complete user details with role and profile        │  │
│  │   Returns: User with nested role and profile objects                  │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ Authentication Methods (used by LoginController):                     │  │
│  │                                                                        │  │
│  │ + authenticate_user(username: str, password: str,                    │  │
│  │                     role_name: str = None) -> Optional[Dict]          │  │
│  │   Description: Complete authentication with token generation          │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + create_session_token(user_id: int) -> str                          │  │
│  │   Description: Create JWT token (24hr expiry)                         │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + verify_session_token(token: str) -> Optional[Dict]                 │  │
│  │   Description: Verify JWT token and return user                       │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ + invalidate_session_token(token: str) -> bool                       │  │
│  │   Description: Invalidate session token (MVP: stateless JWT)          │  │
│  │   Visibility: Public                                                  │  │
│  │                                                                        │  │
│  │ Helper Functions (module-level):                                      │  │
│  │                                                                        │  │
│  │ + hash_password(password: str) -> str                                │  │
│  │   Description: Hash password using pbkdf2:sha256                      │  │
│  │   Visibility: Public (module-level function)                          │  │
│  │                                                                        │  │
│  │ + verify_password(stored_hash: str, password: str) -> bool           │  │
│  │   Description: Verify password against stored hash                    │  │
│  │   Supports: Both scrypt and pbkdf2 hashes                             │  │
│  │   Visibility: Public (module-level function)                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ uses
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              HELPER CLASSES                                  │
│                         (Utilities & Validation)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Validators                                                            │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + validate_username(username: str) -> Tuple[bool, str]               │  │
│  │   Rules:                                                               │  │
│  │     - 3-50 characters                                                 │  │
│  │     - Alphanumeric and underscores only                               │  │
│  │     - Must start with letter                                          │  │
│  │                                                                        │  │
│  │ + validate_password(password: str) -> Tuple[bool, str]               │  │
│  │   Rules:                                                               │  │
│  │     - Minimum 8 characters (PASSWORD_MIN_LENGTH)                      │  │
│  │     - At least one uppercase letter                                   │  │
│  │     - At least one lowercase letter                                   │  │
│  │     - At least one digit                                              │  │
│  │                                                                        │  │
│  │ + validate_email(email: str) -> Tuple[bool, str]                     │  │
│  │   Rules:                                                               │  │
│  │     - Valid email format (regex)                                      │  │
│  │     - Maximum 255 characters                                          │  │
│  │                                                                        │  │
│  │ + validate_full_name(full_name: str) -> Tuple[bool, str]             │  │
│  │   Rules:                                                               │  │
│  │     - 1-100 characters                                                │  │
│  │     - Letters, spaces, hyphens, apostrophes only                      │  │
│  │                                                                        │  │
│  │ + validate_role_id(role_id: Any) -> Tuple[bool, str]                 │  │
│  │   Rules:                                                               │  │
│  │     - Must be integer                                                 │  │
│  │     - Must be positive                                                │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Sanitizers                                                            │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + sanitize_user_data(data: dict) -> dict                             │  │
│  │   Operations:                                                          │  │
│  │     - Strips whitespace from strings                                  │  │
│  │     - Converts email to lowercase                                     │  │
│  │     - Removes extra spaces from full_name                             │  │
│  │     - Ensures role_id is integer                                      │  │
│  │     - Preserves password as-is (for hashing)                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ RequestHelpers                                                        │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + validate_required_fields(data: dict, required: List[str])          │  │
│  │                           -> Tuple[bool, str, List[str]]              │  │
│  │   Returns: (is_valid, error_message, missing_fields)                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ ResponseHelpers                                                       │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + success_response(data: Any, message: str, status_code: int)        │  │
│  │                   -> Tuple[dict, int]                                 │  │
│  │   Format: {'success': True, 'data': data, 'message': message}        │  │
│  │                                                                        │  │
│  │ + error_response(message: str, error_code: str, status_code: int,    │  │
│  │                  details: dict = None) -> Tuple[dict, int]            │  │
│  │   Format: {'success': False, 'message': message,                      │  │
│  │            'error_code': error_code, 'details': details}              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ DataHelpers                                                           │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ + format_user_response(user: dict) -> dict                           │  │
│  │   Operations:                                                          │  │
│  │     - Removes sensitive fields (password)                             │  │
│  │     - Formats role information                                        │  │
│  │     - Standardizes response structure                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ connects to
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE LAYER                                  │
│                            (Supabase PostgreSQL)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ users TABLE                                                           │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ Columns:                                                               │  │
│  │   - id              SERIAL PRIMARY KEY                                │  │
│  │   - username        VARCHAR(50) UNIQUE NOT NULL                       │  │
│  │   - password        VARCHAR(255) NOT NULL                             │  │
│  │   - email           VARCHAR(255) UNIQUE NOT NULL                      │  │
│  │   - full_name       VARCHAR(100) NOT NULL                             │  │
│  │   - role_id         INTEGER NOT NULL REFERENCES roles(id)             │  │
│  │   - is_active       BOOLEAN DEFAULT TRUE                              │  │
│  │   - last_login      TIMESTAMP                                         │  │
│  │   - created_at      TIMESTAMP DEFAULT NOW()                           │  │
│  │                                                                        │  │
│  │ Indexes:                                                               │  │
│  │   - PRIMARY KEY (id)                                                  │  │
│  │   - UNIQUE (username)                                                 │  │
│  │   - UNIQUE (email)                                                    │  │
│  │   - INDEX (role_id)                                                   │  │
│  │                                                                        │  │
│  │ Relationships:                                                         │  │
│  │   - role_id -> roles.id (FOREIGN KEY)                                 │  │
│  │   - One-to-Many with user_profiles                                    │  │
│  │   - One-to-Many with requests (as creator)                            │  │
│  │   - One-to-Many with shortlist                                        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ roles TABLE                                                           │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ Columns:                                                               │  │
│  │   - id                SERIAL PRIMARY KEY                              │  │
│  │   - role_name         VARCHAR(50) UNIQUE NOT NULL                     │  │
│  │   - role_code         VARCHAR(20) UNIQUE NOT NULL                     │  │
│  │   - dashboard_route   VARCHAR(100)                                    │  │
│  │                                                                        │  │
│  │ Common Roles:                                                          │  │
│  │   - User Admin (USER_ADMIN)                                           │  │
│  │   - PIN (PIN)                                                         │  │
│  │   - CSR Rep (CSR_REP)                                                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Class Descriptions

### 1. Boundary Layer Classes

#### 1.1 CreateUserAccountBoundary
- **File**: `src/controller/userAccount/boundary/create_user_account_boundary.py`
- **Purpose**: Handle HTTP POST requests for user creation
- **Route**: `POST /api/userAccount`
- **Authentication**: Requires `USER_ADMIN` role
- **Methods**:
  - `create()`: Receives JSON payload, calls controller, returns JSON response

#### 1.2 ViewUserAccountBoundary
- **File**: `src/controller/userAccount/boundary/view_user_account_boundary.py`
- **Purpose**: Handle HTTP GET requests for viewing users
- **Routes**: 
  - `GET /api/userAccount` - Get all users
  - `GET /api/userAccount/<id>` - Get specific user
- **Authentication**: Requires `USER_ADMIN` role
- **Methods**:
  - `view_all()`: Returns list of all users
  - `view_one(user_id)`: Returns specific user by ID

#### 1.3 UpdateUserAccountBoundary
- **File**: `src/controller/userAccount/boundary/update_user_account_boundary.py`
- **Purpose**: Handle HTTP PUT requests for user updates
- **Route**: `PUT /api/userAccount/<id>`
- **Authentication**: Requires `USER_ADMIN` role
- **Methods**:
  - `update(user_id)`: Receives JSON payload, calls controller, returns JSON response

#### 1.4 SuspendUserAccountBoundary
- **File**: `src/controller/userAccount/boundary/suspend_user_account_boundary.py`
- **Purpose**: Handle HTTP requests for suspend/activate/delete operations
- **Routes**:
  - `PUT /api/userAccount/<id>/suspend` - Suspend user
  - `PUT /api/userAccount/<id>/activate` - Activate user
  - `DELETE /api/userAccount/<id>/delete` - Delete user
- **Authentication**: Requires `USER_ADMIN` role
- **Methods**:
  - `suspend(user_id)`: Deactivate user account
  - `activate(user_id)`: Reactivate user account
  - `delete(user_id)`: Permanently delete user

#### 1.5 SearchUserAccountBoundary
- **File**: `src/controller/userAccount/boundary/search_user_account_boundary.py`
- **Purpose**: Handle HTTP POST requests for user search
- **Route**: `POST /api/userAccount/search`
- **Authentication**: Requires `USER_ADMIN` role
- **Methods**:
  - `search()`: Receives search criteria, returns matching users

---

### 2. Control Layer Classes

#### 2.1 CreateUserAccountController
- **File**: `src/controller/userAccount/create_user_account_controller.py`
- **Purpose**: Business logic for user creation with comprehensive validation
- **Process Flow**:
  1. Validate HTTP format (body not empty)
  2. Validate data format and uniqueness
  3. Sanitize input
  4. Call Entity layer (User.create_user)
  5. Log user activity
  6. Return formatted response

#### 2.2 ViewUserAccountController
- **File**: `src/controller/userAccount/view_user_account_controller.py`
- **Purpose**: Business logic for retrieving user data
- **Methods**:
  - `view_all()`: Get all users with count
  - `view_one(user_id)`: Get specific user or return 404

#### 2.3 UpdateUserAccountController
- **File**: `src/controller/userAccount/update_user_account_controller.py`
- **Purpose**: Business logic for updating user accounts
- **Process Flow**:
  1. Validate data presence
  2. Check user exists
  3. Sanitize input
  4. Validate update data
  5. Call Entity layer
  6. Log activity
  7. Return formatted response

#### 2.4 SuspendUserAccountController
- **File**: `src/controller/userAccount/suspend_user_account_controller.py`
- **Purpose**: Business logic for suspend/activate/delete operations
- **Methods**:
  - `suspend(user_id)`: Set is_active to False
  - `activate(user_id)`: Set is_active to True
  - `delete(user_id)`: Permanently remove user

#### 2.5 SearchUserAccountController
- **File**: `src/controller/userAccount/search_user_account_controller.py`
- **Purpose**: Business logic for searching users
- **Search Criteria**: username, email, full_name

---

### 3. Entity Layer Classes

#### 3.1 User Entity
- **File**: `src/entity/user.py`
- **Purpose**: Database operations for users table
- **All Methods Are Public** (no private/protected methods)
- **Key Responsibilities**:
  - CRUD operations
  - Password hashing/verification
  - Authentication and token management
  - User search and validation
  - Activity logging

---

## Method Visibility Summary

### User Entity - All Methods Are PUBLIC

**Rationale**: 
- Entity layer methods are designed to be called by any Controller
- No internal-only methods exist
- All methods provide useful database operations
- Python convention: Public methods don't start with underscore

**Public Methods** (25 total):
1. `create_user()` - Create new user
2. `get_user_by_id()` - Get by ID
3. `get_user_by_username()` - Get by username
4. `get_user_by_email()` - Get by email
5. `get_by_email()` - Alias for get_user_by_email
6. `get_all_users()` - Get all users
7. `update_user()` - Update user
8. `delete_user()` - Delete user
9. `search_users()` - Search users
10. `username_exists()` - Check username uniqueness
11. `email_exists()` - Check email uniqueness
12. `activate_user()` - Activate account
13. `deactivate_user()` - Deactivate account
14. `authenticate_user()` - Complete authentication
15. `check_login()` - Validate credentials
16. `create_session_token()` - Generate JWT
17. `verify_session_token()` - Verify JWT
18. `invalidate_session_token()` - Invalidate JWT
19. `log_user_activity()` - Log activity
20. `get_user_complete_details()` - Get full user data

**Module-Level Functions** (also public):
- `hash_password()` - Hash password
- `verify_password()` - Verify password

---

## API Endpoints Summary

| Method | Endpoint | Controller | Purpose | Auth Required |
|--------|----------|------------|---------|---------------|
| POST | `/api/userAccount` | CreateUserAccountController | Create user | USER_ADMIN |
| GET | `/api/userAccount` | ViewUserAccountController | Get all users | USER_ADMIN |
| GET | `/api/userAccount/<id>` | ViewUserAccountController | Get one user | USER_ADMIN |
| PUT | `/api/userAccount/<id>` | UpdateUserAccountController | Update user | USER_ADMIN |
| PUT | `/api/userAccount/<id>/suspend` | SuspendUserAccountController | Suspend user | USER_ADMIN |
| PUT | `/api/userAccount/<id>/activate` | SuspendUserAccountController | Activate user | USER_ADMIN |
| DELETE | `/api/userAccount/<id>/delete` | SuspendUserAccountController | Delete user | USER_ADMIN |
| POST | `/api/userAccount/search` | SearchUserAccountController | Search users | USER_ADMIN |

---

## Response Codes Reference

### Create User
- **201**: User created successfully
- **400**: EMPTY_BODY, VALIDATION_ERROR, CREATION_FAILED
- **409**: USERNAME_EXISTS, EMAIL_EXISTS
- **500**: SERVER_ERROR

### View User
- **200**: Success
- **404**: User not found
- **500**: SERVER_ERROR

### Update User
- **200**: Updated successfully
- **400**: EMPTY_BODY, VALIDATION_ERROR, UPDATE_FAILED
- **404**: USER_NOT_FOUND
- **500**: SERVER_ERROR

### Suspend/Activate/Delete User
- **200**: Success
- **400**: Operation failed
- **404**: User not found (delete only)
- **500**: SERVER_ERROR

### Search User
- **200**: Success (even if no results)
- **500**: SERVER_ERROR

---

## Validation Rules

### Username
- 3-50 characters
- Alphanumeric and underscores only
- Must start with letter
- Must be unique

### Password
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- Hashed using pbkdf2:sha256

### Email
- Valid email format
- Maximum 255 characters
- Must be unique

### Full Name
- 1-100 characters
- Letters, spaces, hyphens, apostrophes only

### Role ID
- Must be integer
- Must be positive
- Must reference existing role

---

## Database Relationships

```
users
  ├─> roles (role_id -> roles.id)
  ├─> user_profiles (one-to-many)
  ├─> requests (one-to-many, as creator)
  └─> shortlist (one-to-many)
```

---

## Security Features

1. **Password Hashing**: pbkdf2:sha256 with 260,000 iterations
2. **Role-Based Access Control**: All endpoints require USER_ADMIN role
3. **JWT Authentication**: 24-hour token expiry
4. **Input Sanitization**: All inputs sanitized before processing
5. **Validation**: Multi-layer validation (format, uniqueness, business rules)
6. **Activity Logging**: User actions logged for audit trail
7. **Sensitive Data Protection**: Passwords never returned in responses

---

## Error Handling Strategy

1. **Validation Errors**: Caught early with detailed messages
2. **Database Errors**: Wrapped in try-catch with generic user messages
3. **Duplicate Detection**: Multiple checks (pre-insert, post-insert, exception handling)
4. **Graceful Degradation**: Activity logging failures don't block operations
5. **Consistent Response Format**: All errors follow ResponseHelpers format

---

## Notes

- All Entity methods are **@staticmethod** (no instance required)
- Password hashing uses pbkdf2:sha256 (no cryptography library needed)
- Token invalidation is stateless (JWT-based, no blacklist in MVP)
- Activity logging is best-effort (failures silently ignored)
- Email uniqueness check allows same user to keep their email on update
- Search uses server-side filtering for username, client-side for others

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-08  
**Module**: User Account Management  
**Architecture**: BCE (Boundary-Control-Entity)

