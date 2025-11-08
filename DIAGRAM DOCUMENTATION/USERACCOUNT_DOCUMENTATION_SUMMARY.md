# User Account Management - Documentation Summary

## Overview
This document serves as the index and summary for the complete User Account Management module documentation.

---

## Documentation Files

### 1. BCE Class Diagrams
**File**: `USERACCOUNT_BCE_CLASS_DIAGRAMS.md`

**Contents**:
- Complete BCE Architecture Overview
- Boundary Layer Classes (5 classes)
- Control Layer Classes (5 classes + 2 validation functions)
- Entity Layer Classes (User entity with 20+ methods)
- Helper Classes (Validators, Sanitizers, RequestHelpers, ResponseHelpers, DataHelpers)
- Database Schema (users and roles tables)
- Method Visibility Summary (all methods are public)
- API Endpoints Summary (8 endpoints)
- Response Codes Reference
- Validation Rules
- Database Relationships
- Security Features
- Error Handling Strategy

**Key Highlights**:
- All User entity methods are **public** (no private/protected methods)
- 8 API endpoints, all requiring `USER_ADMIN` role
- Comprehensive validation at multiple layers
- Password hashing using pbkdf2:sha256
- JWT-based authentication with 24-hour expiry

---

### 2. Sequence Diagrams
**File**: `USERACCOUNT_SEQUENCE_DIAGRAMS.md`

**Contents**:
- 8 Complete Sequence Diagrams:
  1. Create User Account (Success + Error flows)
  2. View All Users
  3. View Single User (Success + Error flows)
  4. Update User Account
  5. Suspend User Account
  6. Activate User Account
  7. Delete User Account (Success + Error flows)
  8. Search Users

**Key Highlights**:
- Detailed interaction flows between all layers
- Success and error scenarios
- Authentication flow at each endpoint
- Validation patterns
- Database operations
- Activity logging

---

## Module Architecture

### BCE Pattern Implementation

```
┌─────────────────────────────────────────┐
│         BOUNDARY LAYER                  │
│    (HTTP Request/Response Handling)     │
│                                         │
│  - CreateUserAccountBoundary            │
│  - ViewUserAccountBoundary              │
│  - UpdateUserAccountBoundary            │
│  - SuspendUserAccountBoundary           │
│  - SearchUserAccountBoundary            │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         CONTROL LAYER                   │
│    (Business Logic & Validation)        │
│                                         │
│  - CreateUserAccountController          │
│  - ViewUserAccountController            │
│  - UpdateUserAccountController          │
│  - SuspendUserAccountController         │
│  - SearchUserAccountController          │
│  - validate_create_user_data()          │
│  - validate_update_user_data()          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         ENTITY LAYER                    │
│      (Database Operations)              │
│                                         │
│  - User Entity (20+ methods)            │
│    * CRUD operations                    │
│    * Authentication                     │
│    * Token management                   │
│    * Search & validation                │
│    * Activity logging                   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         DATABASE LAYER                  │
│       (Supabase PostgreSQL)             │
│                                         │
│  - users table                          │
│  - roles table                          │
│  - user_profiles table                  │
│  - activity_log table                   │
└─────────────────────────────────────────┘
```

---

## API Endpoints Reference

| # | Method | Endpoint | Controller | Purpose | Auth |
|---|--------|----------|------------|---------|------|
| 1 | POST | `/api/userAccount` | CreateUserAccountController | Create new user | USER_ADMIN |
| 2 | GET | `/api/userAccount` | ViewUserAccountController | Get all users | USER_ADMIN |
| 3 | GET | `/api/userAccount/<id>` | ViewUserAccountController | Get specific user | USER_ADMIN |
| 4 | PUT | `/api/userAccount/<id>` | UpdateUserAccountController | Update user | USER_ADMIN |
| 5 | PUT | `/api/userAccount/<id>/suspend` | SuspendUserAccountController | Suspend user | USER_ADMIN |
| 6 | PUT | `/api/userAccount/<id>/activate` | SuspendUserAccountController | Activate user | USER_ADMIN |
| 7 | DELETE | `/api/userAccount/<id>/delete` | SuspendUserAccountController | Delete user | USER_ADMIN |
| 8 | POST | `/api/userAccount/search` | SearchUserAccountController | Search users | USER_ADMIN |

---

## Response Codes Summary

### Success Codes
- **200 OK**: View, Update, Suspend, Activate, Delete, Search operations
- **201 Created**: User creation

### Error Codes
- **400 Bad Request**: EMPTY_BODY, VALIDATION_ERROR, CREATION_FAILED, UPDATE_FAILED
- **404 Not Found**: User not found (View, Update, Delete)
- **409 Conflict**: USERNAME_EXISTS, EMAIL_EXISTS
- **500 Internal Server Error**: SERVER_ERROR (unexpected errors)

---

## User Entity Methods

### CRUD Operations (8 methods)
1. `create_user()` - Create new user with validation
2. `get_user_by_id()` - Retrieve by ID
3. `get_user_by_username()` - Retrieve by username
4. `get_user_by_email()` - Retrieve by email
5. `get_all_users()` - Retrieve all users
6. `update_user()` - Update user details
7. `delete_user()` - Permanently delete user
8. `search_users()` - Search by multiple criteria

### Authentication & Token Management (5 methods)
9. `authenticate_user()` - Complete authentication with token
10. `check_login()` - Validate credentials
11. `create_session_token()` - Generate JWT token
12. `verify_session_token()` - Verify JWT token
13. `invalidate_session_token()` - Invalidate token

### Validation & Checks (3 methods)
14. `username_exists()` - Check username uniqueness
15. `email_exists()` - Check email uniqueness
16. `get_by_email()` - Alias for get_user_by_email

### Account Management (2 methods)
17. `activate_user()` - Activate account
18. `deactivate_user()` - Deactivate account

### Additional Utilities (2 methods)
19. `log_user_activity()` - Log user actions
20. `get_user_complete_details()` - Get full user data with relations

### Module-Level Functions (2 functions)
- `hash_password()` - Hash password using pbkdf2:sha256
- `verify_password()` - Verify password against hash

**Total**: 20 methods + 2 functions = **22 public functions**

**Visibility**: All methods are **PUBLIC** (no private/protected methods)

---

## Validation Rules

### Username
- **Length**: 3-50 characters
- **Format**: Alphanumeric and underscores only
- **Start**: Must start with a letter
- **Uniqueness**: Must be unique in database

### Password
- **Length**: Minimum 8 characters
- **Complexity**: 
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
- **Storage**: Hashed using pbkdf2:sha256 with 260,000 iterations

### Email
- **Format**: Valid email format (regex validation)
- **Length**: Maximum 255 characters
- **Uniqueness**: Must be unique in database
- **Storage**: Lowercase

### Full Name
- **Length**: 1-100 characters
- **Format**: Letters, spaces, hyphens, apostrophes only

### Role ID
- **Type**: Must be integer
- **Value**: Must be positive
- **Reference**: Must reference existing role in roles table

---

## Security Features

1. **Password Security**
   - pbkdf2:sha256 hashing with 260,000 iterations
   - Passwords never returned in API responses
   - Password validation enforces strong passwords

2. **Authentication**
   - JWT-based authentication
   - 24-hour token expiry
   - Token verification on every protected endpoint

3. **Authorization**
   - Role-Based Access Control (RBAC)
   - All endpoints require `USER_ADMIN` role
   - `@require_role` decorator enforces authorization

4. **Input Validation**
   - Multi-layer validation (format, uniqueness, business rules)
   - Input sanitization before processing
   - SQL injection prevention via parameterized queries

5. **Audit Trail**
   - Activity logging for user actions
   - Logs include: user_id, activity_type, details, timestamp

6. **Error Handling**
   - Generic error messages for users (security)
   - Detailed error logging for debugging
   - Consistent error response format

---

## Database Schema

### users Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-generated user ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | User's username |
| password | VARCHAR(255) | NOT NULL | Hashed password |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email |
| full_name | VARCHAR(100) | NOT NULL | User's full name |
| role_id | INTEGER | NOT NULL, FK | Reference to roles.id |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |
| last_login | TIMESTAMP | NULLABLE | Last login timestamp |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |

### Indexes
- PRIMARY KEY (id)
- UNIQUE (username)
- UNIQUE (email)
- INDEX (role_id)

### Relationships
- `role_id` → `roles.id` (FOREIGN KEY)
- One-to-Many with `user_profiles`
- One-to-Many with `requests` (as creator)
- One-to-Many with `shortlist`

---

## Helper Classes

### Validators
**File**: `src/utils/validators.py`

**Methods**:
- `validate_username()` - Username format validation
- `validate_password()` - Password strength validation
- `validate_email()` - Email format validation
- `validate_full_name()` - Full name format validation
- `validate_role_id()` - Role ID type validation

### Sanitizers
**File**: `src/utils/sanitizers.py`

**Methods**:
- `sanitize_user_data()` - Clean and normalize user input

### RequestHelpers
**File**: `src/utils/helpers.py`

**Methods**:
- `validate_required_fields()` - Check for missing required fields

### ResponseHelpers
**File**: `src/utils/helpers.py`

**Methods**:
- `success_response()` - Format success responses
- `error_response()` - Format error responses

### DataHelpers
**File**: `src/utils/helpers.py`

**Methods**:
- `format_user_response()` - Format user data for API response

---

## Common Patterns

### 1. Validation Pattern
```
1. Check data presence
2. Validate required fields
3. Format validation (username, email, etc.)
4. Uniqueness checks (database queries)
5. Sanitize input
6. Process in Entity layer
```

### 2. Error Handling Pattern
```
1. Try-catch blocks at each layer
2. Specific error codes for different failures
3. Consistent response format via ResponseHelpers
4. Detailed error messages for debugging
5. Generic messages for users (security)
```

### 3. Authentication Flow
```
1. User sends request with JWT token
2. @require_role decorator intercepts
3. Token verified using User.verify_session_token()
4. If valid and role matches, proceed
5. If invalid, return 401 Unauthorized
```

### 4. Activity Logging Pattern
```
1. Best-effort logging after successful operations
2. Failures don't block main operation
3. Logs include: user_id, activity_type, details
4. Used for audit trail
```

---

## File Structure

```
csr_app/
├── src/
│   ├── controller/
│   │   └── userAccount/
│   │       ├── boundary/
│   │       │   ├── create_user_account_boundary.py
│   │       │   ├── view_user_account_boundary.py
│   │       │   ├── update_user_account_boundary.py
│   │       │   ├── suspend_user_account_boundary.py
│   │       │   └── search_user_account_boundary.py
│   │       ├── create_user_account_controller.py
│   │       ├── view_user_account_controller.py
│   │       ├── update_user_account_controller.py
│   │       ├── suspend_user_account_controller.py
│   │       └── search_user_account_controller.py
│   ├── entity/
│   │   └── user.py
│   └── utils/
│       ├── validators.py
│       ├── sanitizers.py
│       └── helpers.py
└── DIAGRAM DOCUMENTATION/
    ├── USERACCOUNT_BCE_CLASS_DIAGRAMS.md
    ├── USERACCOUNT_SEQUENCE_DIAGRAMS.md
    └── USERACCOUNT_DOCUMENTATION_SUMMARY.md (this file)
```

---

## Testing Recommendations

### Unit Tests
- Test each validation function independently
- Test User entity methods with mock database
- Test sanitization functions
- Test password hashing/verification

### Integration Tests
- Test complete create user flow
- Test update with uniqueness checks
- Test search with various criteria
- Test suspend/activate/delete operations

### Security Tests
- Test authentication with invalid tokens
- Test authorization with different roles
- Test SQL injection attempts
- Test password strength enforcement

### Edge Cases
- Test with empty/null values
- Test with extremely long inputs
- Test with special characters
- Test concurrent operations (race conditions)

---

## Future Enhancements

### Potential Improvements
1. **Token Blacklist**: Implement database-backed token blacklist for logout
2. **Password Reset**: Add password reset functionality
3. **Email Verification**: Add email verification on registration
4. **Two-Factor Authentication**: Add 2FA support
5. **Rate Limiting**: Add rate limiting to prevent brute force attacks
6. **Pagination**: Add pagination to view_all_users endpoint
7. **Soft Delete**: Implement soft delete instead of permanent deletion
8. **Password History**: Prevent password reuse
9. **Account Lockout**: Lock account after failed login attempts
10. **Audit Log Enhancement**: More detailed audit logging

---

## Notes

- All Entity methods use `@staticmethod` (no instance required)
- Password hashing uses pbkdf2:sha256 (no cryptography library needed)
- Token invalidation is stateless (JWT-based, no blacklist in MVP)
- Activity logging is best-effort (failures silently ignored)
- Email uniqueness check allows same user to keep their email on update
- Search uses server-side filtering for username, client-side for email/full_name
- All timestamps stored as ISO 8601 strings
- Database connections use retry logic for resilience

---

## Quick Reference

### Create User Request
```json
POST /api/userAccount
{
  "username": "john_doe",
  "password": "SecurePass123",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role_id": 1
}
```

### Update User Request
```json
PUT /api/userAccount/42
{
  "email": "newemail@example.com",
  "full_name": "John Smith"
}
```

### Search Users Request
```json
POST /api/userAccount/search
{
  "username": "john",
  "email": "",
  "full_name": ""
}
```

### Success Response Format
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_CODE",
  "details": { ... }
}
```

---

## Contact & Support

For questions or issues related to the User Account Management module:
- Review the BCE Class Diagrams document for architecture details
- Review the Sequence Diagrams document for flow details
- Check the code comments in the source files
- Refer to the validation rules section for input requirements

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-08  
**Module**: User Account Management  
**Architecture**: BCE (Boundary-Control-Entity)  
**Total Documentation Pages**: 3 (BCE Diagrams, Sequence Diagrams, Summary)


