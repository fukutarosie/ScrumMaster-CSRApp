# Complete BCE Class Diagrams

## System: Corporate Social Responsibility (CSR) Platform

---

## Table of Contents
1. [BCE Pattern Overview](#bce-pattern-overview)
2. [Authentication Module](#authentication-module)
3. [User Account Module](#user-account-module)
4. [User Profile Module](#user-profile-module)
5. [Role Management Module](#role-management-module)
6. [Request Management Module](#request-management-module)
7. [Shortlist Management Module](#shortlist-management-module)
8. [Entity Classes](#entity-classes)
9. [Utility Classes](#utility-classes)

---

## BCE Pattern Overview

The system follows the **Boundary-Control-Entity (BCE)** architectural pattern:

- **Boundary**: HTTP endpoints (Flask blueprints) that handle incoming requests
- **Control**: Controllers that orchestrate business logic and validation
- **Entity**: Domain objects that encapsulate data and database operations

### Key Principles
1. **Boundaries** receive HTTP requests and delegate to **Controllers**
2. **Controllers** hold request data in memory and orchestrate operations
3. **Entities** encapsulate data and perform database operations
4. True OOP: Objects hold state and instance methods do the work

---

## Authentication Module

### Boundary Class: `login_boundary`

```
┌────────────────────────────────────────┐
│        LoginBoundary (Flask)           │
├────────────────────────────────────────┤
│ - Blueprint: login_boundary            │
│ - URL Prefix: /api/auth                │
├────────────────────────────────────────┤
│ + login() : Response                   │
│   POST /api/auth/login                 │
│   - Receives: {username, password,     │
│     role_name}                          │
│   - Returns: {success, token, user}    │
│                                         │
│ + logout() : Response                  │
│   POST /api/auth/logout                │
│   - Headers: Authorization: Bearer     │
│   - Returns: {success, message}        │
│                                         │
│ + verify() : Response                  │
│   GET /api/auth/verify                 │
│   - Headers: Authorization: Bearer     │
│   - Returns: {success, user}           │
└────────────────────────────────────────┘
```

### Control Class: `LoginController`

```
┌──────────────────────────────────────────────┐
│          LoginController                     │
├──────────────────────────────────────────────┤
│ - request_data: Dict                         │
│ - user: User                                 │
│ - errors: List[str]                          │
│ - sanitized_data: Dict                       │
├──────────────────────────────────────────────┤
│ + __init__(request_data: Dict)               │
│ + validate_request_data() : bool             │
│ + authenticate_user() : bool                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Private/Helper Methods:                      │
│ - Validates username, password, role         │
│ - Sanitizes input using Sanitizers           │
│ - Delegates authentication to User.          │
│   authenticate()                              │
│ - Generates JWT token via User.              │
│   generate_session_token()                    │
└──────────────────────────────────────────────┘
```

### Control Class: `LogoutController`

```
┌──────────────────────────────────────────────┐
│          LogoutController                    │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - user: User                                 │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str)                  │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Private/Helper Methods:                      │
│ - Verifies token via User.verify_token()     │
│ - Returns success response                   │
└──────────────────────────────────────────────┘
```

### Control Class: `VerifyTokenController`

```
┌──────────────────────────────────────────────┐
│        VerifyTokenController                 │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - user: User                                 │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str)                  │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Private/Helper Methods:                      │
│ - Verifies token via User.verify_token()     │
│ - Returns user data if valid                 │
└──────────────────────────────────────────────┘
```

### Entity Class Used: `User`
(See [Entity Classes](#entity-classes) section)

---

## User Account Module

### Boundary Class: `user_account_boundary`

```
┌─────────────────────────────────────────────┐
│       UserAccountBoundary (Flask)           │
├─────────────────────────────────────────────┤
│ - Blueprint: user_account_boundary          │
│ - URL Prefix: /api/user-accounts            │
├─────────────────────────────────────────────┤
│ + create_user_account() : Response          │
│   POST /api/user-accounts                   │
│                                              │
│ + view_user_account(user_id) : Response     │
│   GET /api/user-accounts/{user_id}          │
│                                              │
│ + update_user_account(user_id) : Response   │
│   PUT /api/user-accounts/{user_id}          │
│                                              │
│ + suspend_user_account(user_id) : Response  │
│   POST /api/user-accounts/{user_id}/suspend │
│                                              │
│ + search_user_accounts() : Response         │
│   GET /api/user-accounts/search             │
└─────────────────────────────────────────────┘
```

### Control Class: `CreateUserAccountController`

```
┌──────────────────────────────────────────────┐
│      CreateUserAccountController             │
├──────────────────────────────────────────────┤
│ - request_data: Dict                         │
│ - user: User                                 │
│ - errors: List[str]                          │
│ - sanitized_data: Dict                       │
├──────────────────────────────────────────────┤
│ + __init__(request_data: Dict)               │
│ + validate_request_data() : bool             │
│ + sanitize_data() : void                     │
│ + create_user_object() : void                │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Validation Rules:                            │
│ - Username: 3-50 chars, alphanumeric + _     │
│ - Password: min 8 chars                      │
│ - Email: valid format                        │
│ - Full name: 2-100 chars                     │
│ - Role ID: must exist                        │
│                                               │
│ Flow:                                        │
│ 1. Validate input                            │
│ 2. Sanitize data                             │
│ 3. Create User entity                        │
│ 4. Call user.save()                          │
│ 5. Log activity                              │
└──────────────────────────────────────────────┘
```

### Control Class: `ViewUserAccountController`

```
┌──────────────────────────────────────────────┐
│       ViewUserAccountController              │
├──────────────────────────────────────────────┤
│ - user_id: int                               │
│ - user: User                                 │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(user_id: int)                     │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load user via User.find(user_id)          │
│ 2. Return user data                          │
└──────────────────────────────────────────────┘
```

### Control Class: `UpdateUserAccountController`

```
┌──────────────────────────────────────────────┐
│      UpdateUserAccountController             │
├──────────────────────────────────────────────┤
│ - user_id: int                               │
│ - request_data: Dict                         │
│ - user: User                                 │
│ - errors: List[str]                          │
│ - sanitized_data: Dict                       │
├──────────────────────────────────────────────┤
│ + __init__(user_id: int, request_data: Dict) │
│ + validate_request_data() : bool             │
│ + sanitize_data() : void                     │
│ + update_user_object() : void                │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load existing user                        │
│ 2. Validate input                            │
│ 3. Sanitize data                             │
│ 4. Update user attributes                    │
│ 5. Call user.save()                          │
└──────────────────────────────────────────────┘
```

### Control Class: `SuspendUserAccountController`

```
┌──────────────────────────────────────────────┐
│      SuspendUserAccountController            │
├──────────────────────────────────────────────┤
│ - user_id: int                               │
│ - user: User                                 │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(user_id: int)                     │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load user via User.find(user_id)          │
│ 2. Call user.deactivate()                    │
│ 3. Return success                            │
└──────────────────────────────────────────────┘
```

### Control Class: `SearchUserAccountController`

```
┌──────────────────────────────────────────────┐
│      SearchUserAccountController             │
├──────────────────────────────────────────────┤
│ - search_criteria: Dict                      │
│ - users: List[User]                          │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(search_criteria: Dict)            │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Extract search criteria (username,        │
│    email, full_name)                         │
│ 2. Call User.search(**criteria)              │
│ 3. Return list of users                      │
└──────────────────────────────────────────────┘
```

### Entity Class Used: `User`
(See [Entity Classes](#entity-classes) section)

---

## User Profile Module

### Boundary Class: `user_profile_boundary`

```
┌─────────────────────────────────────────────┐
│       UserProfileBoundary (Flask)           │
├─────────────────────────────────────────────┤
│ - Blueprint: user_profile_boundary          │
│ - URL Prefix: /api/user-profiles            │
├─────────────────────────────────────────────┤
│ + create_user_profile() : Response          │
│   POST /api/user-profiles                   │
│                                              │
│ + view_user_profile(profile_id) : Response  │
│   GET /api/user-profiles/{profile_id}       │
│                                              │
│ + update_user_profile(profile_id) : Response│
│   PUT /api/user-profiles/{profile_id}       │
│                                              │
│ + suspend_user_profile(profile_id):Response │
│   POST /api/user-profiles/{profile_id}/     │
│   suspend                                    │
│                                              │
│ + search_user_profiles() : Response         │
│   GET /api/user-profiles/search             │
└─────────────────────────────────────────────┘
```

### Control Class: `CreateUserProfileController`

```
┌──────────────────────────────────────────────┐
│      CreateUserProfileController             │
├──────────────────────────────────────────────┤
│ - request_data: Dict                         │
│ - profile: Profile                           │
│ - errors: List[str]                          │
│ - sanitized_data: Dict                       │
├──────────────────────────────────────────────┤
│ + __init__(request_data: Dict)               │
│ + validate_request_data() : bool             │
│ + sanitize_data() : void                     │
│ + create_profile_object() : void             │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Validation Rules:                            │
│ - Profile name: min 2 chars, unique          │
│ - Description: optional                      │
│                                               │
│ Flow:                                        │
│ 1. Validate input                            │
│ 2. Sanitize data                             │
│ 3. Create Profile entity                     │
│ 4. Call profile.save()                       │
└──────────────────────────────────────────────┘
```

### Control Classes: Similar structure for
- `ViewUserProfileController`
- `UpdateUserProfileController`
- `SuspendUserProfileController`
- `SearchUserProfileController`

### Entity Class Used: `Profile`
(See [Entity Classes](#entity-classes) section)

---

## Role Management Module

### Boundary Class: `role_boundary`

```
┌─────────────────────────────────────────────┐
│           RoleBoundary (Flask)              │
├─────────────────────────────────────────────┤
│ - Blueprint: role_boundary                  │
│ - URL Prefix: /api/roles                    │
├─────────────────────────────────────────────┤
│ + create_role() : Response                  │
│   POST /api/roles                           │
│                                              │
│ + get_role(role_id) : Response              │
│   GET /api/roles/{role_id}                  │
│                                              │
│ + get_all_roles() : Response                │
│   GET /api/roles                            │
│                                              │
│ + get_public_roles() : Response             │
│   GET /api/roles/public                     │
│                                              │
│ + update_role(role_id) : Response           │
│   PUT /api/roles/{role_id}                  │
│                                              │
│ + delete_role(role_id) : Response           │
│   DELETE /api/roles/{role_id}               │
└─────────────────────────────────────────────┘
```

### Control Class: `CreateRoleController`

```
┌──────────────────────────────────────────────┐
│           CreateRoleController               │
├──────────────────────────────────────────────┤
│ - request_data: Dict                         │
│ - role: Role                                 │
│ - errors: List[str]                          │
│ - sanitized_data: Dict                       │
├──────────────────────────────────────────────┤
│ + __init__(request_data: Dict)               │
│ + validate_request_data() : bool             │
│ + sanitize_data() : void                     │
│ + create_role_object() : void                │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Validation Rules:                            │
│ - Role name: min 2 chars, unique             │
│ - Role code: min 2 chars, unique             │
│ - Dashboard route: required, valid path      │
│ - Description: optional                      │
│                                               │
│ Flow:                                        │
│ 1. Validate input                            │
│ 2. Sanitize data                             │
│ 3. Create Role entity                        │
│ 4. Call role.save()                          │
└──────────────────────────────────────────────┘
```

### Control Class: `GetRoleController`

```
┌──────────────────────────────────────────────┐
│           GetRoleController                  │
├──────────────────────────────────────────────┤
│ - role_id: int                               │
│ - role: Role                                 │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(role_id: int)                     │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load role via Role.find(role_id)          │
│ 2. Return role data                          │
└──────────────────────────────────────────────┘
```

### Control Class: `GetAllRolesController`

```
┌──────────────────────────────────────────────┐
│        GetAllRolesController                 │
├──────────────────────────────────────────────┤
│ - roles: List[Role]                          │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__()                                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load all roles via Role.all()             │
│ 2. Return list of roles                      │
└──────────────────────────────────────────────┘
```

### Control Class: `GetPublicRolesController`

```
┌──────────────────────────────────────────────┐
│       GetPublicRolesController               │
├──────────────────────────────────────────────┤
│ - roles: List[Role]                          │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__()                                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load roles via Role.public_roles()        │
│ 2. Return non-admin roles                    │
└──────────────────────────────────────────────┘
```

### Control Class: `UpdateRoleController`

```
┌──────────────────────────────────────────────┐
│          UpdateRoleController                │
├──────────────────────────────────────────────┤
│ - role_id: int                               │
│ - request_data: Dict                         │
│ - role: Role                                 │
│ - errors: List[str]                          │
│ - sanitized_data: Dict                       │
├──────────────────────────────────────────────┤
│ + __init__(role_id: int, request_data: Dict) │
│ + validate_request_data() : bool             │
│ + sanitize_data() : void                     │
│ + update_role_object() : void                │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load existing role                        │
│ 2. Validate input                            │
│ 3. Sanitize data                             │
│ 4. Update role attributes                    │
│ 5. Call role.save()                          │
└──────────────────────────────────────────────┘
```

### Control Class: `DeleteRoleController`

```
┌──────────────────────────────────────────────┐
│          DeleteRoleController                │
├──────────────────────────────────────────────┤
│ - role_id: int                               │
│ - role: Role                                 │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(role_id: int)                     │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load role via Role.find(role_id)          │
│ 2. Check if role assigned to users           │
│ 3. Call role.delete()                        │
│ 4. Return success                            │
└──────────────────────────────────────────────┘
```

### Entity Class Used: `Role`
(See [Entity Classes](#entity-classes) section)

---

## Request Management Module

### Boundary Class: `request_boundary`

```
┌──────────────────────────────────────────────┐
│         RequestBoundary (Flask)              │
├──────────────────────────────────────────────┤
│ - Blueprint: request_boundary                │
│ - URL Prefix: /api/requests                  │
├──────────────────────────────────────────────┤
│ + create_new_pin_request() : Response        │
│   POST /api/requests                         │
│                                               │
│ + get_pin_requests() : Response              │
│   GET /api/requests/pin                      │
│                                               │
│ + view_pin_request(request_id) : Response    │
│   GET /api/requests/{request_id}             │
│                                               │
│ + update_pin_request(request_id) : Response  │
│   PUT /api/requests/{request_id}             │
│                                               │
│ + suspend_pin_request(request_id) : Response │
│   POST /api/requests/{request_id}/suspend    │
│                                               │
│ + search_pin_request() : Response            │
│   GET /api/requests/search                   │
│                                               │
│ + increment_view_count(request_id): Response │
│   POST /api/requests/{request_id}/view       │
│                                               │
│ + get_request_analytics() : Response         │
│   GET /api/requests/analytics                │
│                                               │
│ + get_completed_matches() : Response         │
│   GET /api/requests/completed-matches        │
│                                               │
│ + get_request_lookups() : Response           │
│   GET /api/requests/lookups                  │
└──────────────────────────────────────────────┘
```

### Control Class: `CreateNewPINRequestController`

```
┌──────────────────────────────────────────────┐
│     CreateNewPINRequestController            │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - request_data: Dict                         │
│ - user: User                                 │
│ - request: Request                           │
│ - errors: List[str]                          │
│ - image_url: str                             │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str,                  │
│            request_data: Dict)                │
│ + authenticate_user() : bool                 │
│ + validate_request_data() : bool             │
│ + process_image_upload() : bool              │
│ + create_request_object() : void             │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Validation Rules:                            │
│ - Title: min 5 chars                         │
│ - Description: min 10 chars                  │
│ - Service type: must exist in lookup table   │
│ - Region: required                           │
│ - Requested by date: required                │
│ - Image: required, base64 format             │
│                                               │
│ Flow:                                        │
│ 1. Authenticate PIN user                     │
│ 2. Validate input                            │
│ 3. Process image upload                      │
│ 4. Create Request entity                     │
│ 5. Call request.save()                       │
└──────────────────────────────────────────────┘
```

### Control Class: `GetPINRequestsController`

```
┌──────────────────────────────────────────────┐
│        GetPINRequestsController              │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - user: User                                 │
│ - requests: List[Request]                    │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str)                  │
│ + authenticate_user() : bool                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Authenticate user                         │
│ 2. Get requests via Request.by_pin_user()    │
│ 3. Return list of requests                   │
└──────────────────────────────────────────────┘
```

### Control Class: `ViewPINRequestController`

```
┌──────────────────────────────────────────────┐
│        ViewPINRequestController              │
├──────────────────────────────────────────────┤
│ - request_id: int                            │
│ - request: Request                           │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(request_id: int)                  │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load request via Request.find(request_id) │
│ 2. Return request data                       │
└──────────────────────────────────────────────┘
```

### Control Class: `UpdatePINRequestController`

```
┌──────────────────────────────────────────────┐
│       UpdatePINRequestController             │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - request_id: int                            │
│ - request_data: Dict                         │
│ - user: User                                 │
│ - request: Request                           │
│ - errors: List[str]                          │
│ - image_url: str                             │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str, request_id: int, │
│            request_data: Dict)                │
│ + authenticate_user() : bool                 │
│ + validate_request_data() : bool             │
│ + process_image_upload() : bool              │
│ + update_request_object() : void             │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Authenticate user                         │
│ 2. Load existing request                     │
│ 3. Verify ownership                          │
│ 4. Validate input                            │
│ 5. Process image if provided                 │
│ 6. Update request attributes                 │
│ 7. Call request.save()                       │
└──────────────────────────────────────────────┘
```

### Control Class: `SuspendPINRequestController`

```
┌──────────────────────────────────────────────┐
│      SuspendPINRequestController             │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - request_id: int                            │
│ - user: User                                 │
│ - request: Request                           │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str, request_id: int) │
│ + authenticate_user() : bool                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Authenticate user                         │
│ 2. Load request                              │
│ 3. Verify ownership                          │
│ 4. Call request.suspend()                    │
│ 5. Return success                            │
└──────────────────────────────────────────────┘
```

### Control Class: `SearchPINRequestController`

```
┌──────────────────────────────────────────────┐
│       SearchPINRequestController             │
├──────────────────────────────────────────────┤
│ - search_criteria: Dict                      │
│ - requests: List[Request]                    │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(search_criteria: Dict)            │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Extract criteria (service_type, region,   │
│    status, pin_user_id)                      │
│ 2. Call Request.search(**criteria)           │
│ 3. Return matching requests                  │
└──────────────────────────────────────────────┘
```

### Control Class: `IncrementViewCountController`

```
┌──────────────────────────────────────────────┐
│      IncrementViewCountController            │
├──────────────────────────────────────────────┤
│ - request_id: int                            │
│ - request: Request                           │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(request_id: int)                  │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Load request                              │
│ 2. Call request.increment_view_count()       │
│ 3. Return success                            │
└──────────────────────────────────────────────┘
```

### Control Class: `GetRequestAnalyticsController`

```
┌──────────────────────────────────────────────┐
│      GetRequestAnalyticsController           │
├──────────────────────────────────────────────┤
│ - analytics: Dict                            │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__()                                 │
│ + calculate_analytics() : Dict               │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Analytics Calculated:                        │
│ - Total requests by status                   │
│ - Requests by service type                   │
│ - Requests by region                         │
│ - Average view count                         │
│ - Average shortlist count                    │
│ - Fulfillment rate                           │
│                                               │
│ Flow:                                        │
│ 1. Query database for aggregated stats       │
│ 2. Calculate metrics                         │
│ 3. Return analytics                          │
└──────────────────────────────────────────────┘
```

### Control Class: `GetCompletedMatchesController`

```
┌──────────────────────────────────────────────┐
│      GetCompletedMatchesController           │
├──────────────────────────────────────────────┤
│ - matches: List[Dict]                        │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__()                                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Query shortlist with status=COMPLETED     │
│ 2. Join with request and user data           │
│ 3. Return completed matches                  │
└──────────────────────────────────────────────┘
```

### Control Class: `GetRequestLookupsController`

```
┌──────────────────────────────────────────────┐
│       GetRequestLookupsController            │
├──────────────────────────────────────────────┤
│ - lookups: Dict                              │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__()                                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Lookups Returned:                            │
│ - Service types                              │
│ - Regions (unique from requests)             │
│ - Request statuses                           │
│                                               │
│ Flow:                                        │
│ 1. Get service types via Request.            │
│    get_service_types()                       │
│ 2. Get unique regions from database          │
│ 3. Get status constants                      │
│ 4. Return lookups                            │
└──────────────────────────────────────────────┘
```

### Entity Class Used: `Request`
(See [Entity Classes](#entity-classes) section)

---

## Shortlist Management Module

### Boundary Class: `shortlist_boundary`

```
┌──────────────────────────────────────────────┐
│        ShortlistBoundary (Flask)             │
├──────────────────────────────────────────────┤
│ - Blueprint: shortlist_boundary              │
│ - URL Prefix: /api/shortlist                 │
├──────────────────────────────────────────────┤
│ + add_to_shortlist() : Response              │
│   POST /api/shortlist                        │
│                                               │
│ + get_shortlist() : Response                 │
│   GET /api/shortlist                         │
│                                               │
│ + get_shortlist_stats() : Response           │
│   GET /api/shortlist/stats                   │
│                                               │
│ + remove_from_shortlist(shortlist_id):       │
│   Response                                    │
│   DELETE /api/shortlist/{shortlist_id}       │
│                                               │
│ + update_shortlist_status(shortlist_id):     │
│   Response                                    │
│   PUT /api/shortlist/{shortlist_id}/status   │
└──────────────────────────────────────────────┘
```

### Control Class: `AddToShortlistController`

```
┌──────────────────────────────────────────────┐
│        AddToShortlistController              │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - request_data: Dict                         │
│ - user: User                                 │
│ - shortlist: Shortlist                       │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str,                  │
│            request_data: Dict)                │
│ + authenticate_user() : bool                 │
│ + validate_request_data() : bool             │
│ + create_shortlist_object() : void           │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Validation:                                  │
│ - Request ID required                        │
│ - Request must be ACTIVE                     │
│ - No duplicate shortlist                     │
│                                               │
│ Flow:                                        │
│ 1. Authenticate CSR user                     │
│ 2. Validate request_id                       │
│ 3. Create Shortlist entity                   │
│ 4. Set status to SHORTLISTED                 │
│ 5. Call shortlist.save()                     │
│ 6. Increment request.shortlist_count         │
└──────────────────────────────────────────────┘
```

### Control Class: `GetShortlistController`

```
┌──────────────────────────────────────────────┐
│         GetShortlistController               │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - user: User                                 │
│ - shortlist_items: List[Shortlist]           │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str)                  │
│ + authenticate_user() : bool                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Authenticate user                         │
│ 2. Get shortlist via Shortlist.by_csr_user() │
│ 3. Return list with joined request data      │
└──────────────────────────────────────────────┘
```

### Control Class: `GetShortlistStatsController`

```
┌──────────────────────────────────────────────┐
│       GetShortlistStatsController            │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - user: User                                 │
│ - stats: Dict                                │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str)                  │
│ + authenticate_user() : bool                 │
│ + calculate_stats() : Dict                   │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Stats Calculated:                            │
│ - Total shortlisted                          │
│ - In progress count                          │
│ - Completed count                            │
│ - Declined count                             │
│ - Total volunteered hours                    │
│                                               │
│ Flow:                                        │
│ 1. Authenticate user                         │
│ 2. Get all shortlist entries                 │
│ 3. Calculate statistics                      │
│ 4. Return stats                              │
└──────────────────────────────────────────────┘
```

### Control Class: `RemoveFromShortlistController`

```
┌──────────────────────────────────────────────┐
│      RemoveFromShortlistController           │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - shortlist_id: int                          │
│ - user: User                                 │
│ - shortlist: Shortlist                       │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str,                  │
│            shortlist_id: int)                 │
│ + authenticate_user() : bool                 │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Authenticate user                         │
│ 2. Load shortlist entry                      │
│ 3. Verify ownership                          │
│ 4. Verify status is SHORTLISTED              │
│ 5. Call shortlist.delete()                   │
│ 6. Decrement request.shortlist_count         │
│ 7. Return success                            │
└──────────────────────────────────────────────┘
```

### Control Class: `UpdateShortlistStatusController`

```
┌──────────────────────────────────────────────┐
│     UpdateShortlistStatusController          │
├──────────────────────────────────────────────┤
│ - auth_token: str                            │
│ - shortlist_id: int                          │
│ - request_data: Dict                         │
│ - user: User                                 │
│ - shortlist: Shortlist                       │
│ - errors: List[str]                          │
├──────────────────────────────────────────────┤
│ + __init__(auth_token: str, shortlist_id:    │
│            int, request_data: Dict)           │
│ + authenticate_user() : bool                 │
│ + validate_request_data() : bool             │
│ + update_shortlist_object() : void           │
│ + execute() : Tuple[Dict, int]               │
│                                               │
│ Flow:                                        │
│ 1. Authenticate user                         │
│ 2. Load shortlist entry                      │
│ 3. Verify ownership                          │
│ 4. Validate new status                       │
│ 5. Update shortlist attributes (status,      │
│    notes, hours, completion_date)            │
│ 6. Call shortlist.save()                     │
│ 7. Return success                            │
└──────────────────────────────────────────────┘
```

### Entity Class Used: `Shortlist`
(See [Entity Classes](#entity-classes) section)

---

## Entity Classes

### Entity Class: `User`

```
┌──────────────────────────────────────────────────────┐
│                      User                            │
├──────────────────────────────────────────────────────┤
│ Instance Variables (Data in Memory):                 │
│ - id: int                                            │
│ - username: str                                      │
│ - password: str (hashed)                             │
│ - email: str                                         │
│ - full_name: str                                     │
│ - role_id: int                                       │
│ - is_active: bool                                    │
│ - created_at: str                                    │
│ - last_login: str                                    │
│ - roles: Dict (joined role data)                     │
├──────────────────────────────────────────────────────┤
│ Constructor:                                         │
│ + __init__(user_id: int = None,                      │
│            user_data: Dict = None)                    │
├──────────────────────────────────────────────────────┤
│ Validation Methods:                                  │
│ + validate() : Tuple[bool, List[str]]                │
│ + check_uniqueness() : Tuple[bool, str]              │
├──────────────────────────────────────────────────────┤
│ CRUD Methods (Instance Methods):                     │
│ + save() : bool                                      │
│   - Creates or updates user in database              │
│   - Hashes password for new users                    │
│   - Validates and checks uniqueness                  │
│                                                       │
│ + delete() : bool                                    │
│   - Deletes user from database                       │
│                                                       │
│ + deactivate() : bool                                │
│   - Sets is_active = False                           │
│                                                       │
│ + activate() : bool                                  │
│   - Sets is_active = True                            │
│                                                       │
│ + update_last_login() : bool                         │
│   - Updates last_login timestamp                     │
├──────────────────────────────────────────────────────┤
│ Password Methods:                                    │
│ + verify_password(password: str) : bool              │
│ + set_password(new_password: str) : void             │
├──────────────────────────────────────────────────────┤
│ Authentication Methods:                              │
│ + generate_session_token() : str                     │
│   - Generates JWT with 24h expiration                │
├──────────────────────────────────────────────────────┤
│ Utility Methods:                                     │
│ + to_dict(include_password: bool = False) : Dict     │
│ + log_activity(activity_type: str,                   │
│                activity_details: str) : bool          │
├──────────────────────────────────────────────────────┤
│ Magic Methods:                                       │
│ + __str__() : str                                    │
│ + __repr__() : str                                   │
│ + __eq__(other) : bool                               │
│ + __hash__() : int                                   │
├──────────────────────────────────────────────────────┤
│ Factory Methods (Class Methods):                     │
│ + find(user_id: int) : User                          │
│ + find_by_username(username: str) : User             │
│ + find_by_email(email: str) : User                   │
│ + all(include_inactive: bool = False) : List[User]   │
│ + by_role(role_id: int) : List[User]                 │
│ + by_role_name(role_name: str) : List[User]          │
│ + authenticate(username: str, password: str,         │
│                role_name: str = None) : User          │
│ + verify_token(token: str) : User                    │
│ + search(username: str = '', email: str = '',        │
│          full_name: str = '') : List[User]            │
│ + count_all() : int                                  │
│ + count_active() : int                               │
└──────────────────────────────────────────────────────┘
```

### Entity Class: `Role`

```
┌──────────────────────────────────────────────────────┐
│                      Role                            │
├──────────────────────────────────────────────────────┤
│ Class Constants:                                     │
│ - USER_ADMIN = "User Admin"                          │
│ - PIN = "PIN"                                        │
│ - CSR_REP = "CSR Rep"                                │
│ - PLATFORM_MANAGEMENT = "Platform Management"        │
│ - ROLE_ROUTES: Dict[str, str]                        │
├──────────────────────────────────────────────────────┤
│ Instance Variables:                                  │
│ - id: int                                            │
│ - role_name: str                                     │
│ - role_code: str                                     │
│ - description: str                                   │
│ - dashboard_route: str                               │
│ - created_at: str                                    │
├──────────────────────────────────────────────────────┤
│ Constructor:                                         │
│ + __init__(role_id: int = None,                      │
│            role_data: Dict = None)                    │
├──────────────────────────────────────────────────────┤
│ Validation Methods:                                  │
│ + validate() : Tuple[bool, List[str]]                │
│ + check_uniqueness() : Tuple[bool, str]              │
├──────────────────────────────────────────────────────┤
│ CRUD Methods:                                        │
│ + save() : bool                                      │
│ + delete() : bool                                    │
│ + update(updates: Dict = None) : bool                │
├──────────────────────────────────────────────────────┤
│ Utility Methods:                                     │
│ + to_dict() : Dict                                   │
│ + get_dashboard_route() : str                        │
├──────────────────────────────────────────────────────┤
│ Magic Methods:                                       │
│ + __str__() : str                                    │
│ + __repr__() : str                                   │
│ + __eq__(other) : bool                               │
│ + __hash__() : int                                   │
├──────────────────────────────────────────────────────┤
│ Factory Methods:                                     │
│ + find(role_id: int) : Role                          │
│ + find_by_name(role_name: str) : Role                │
│ + find_by_code(role_code: str) : Role                │
│ + all() : List[Role]                                 │
│ + public_roles() : List[Role]                        │
└──────────────────────────────────────────────────────┘
```

### Entity Class: `Profile`

```
┌──────────────────────────────────────────────────────┐
│                    Profile                           │
├──────────────────────────────────────────────────────┤
│ Instance Variables:                                  │
│ - id: int                                            │
│ - profile_name: str                                  │
│ - description: str                                   │
│ - created_at: str                                    │
│ - updated_at: str                                    │
├──────────────────────────────────────────────────────┤
│ Constructor:                                         │
│ + __init__(profile_id: int = None,                   │
│            profile_data: Dict = None)                 │
├──────────────────────────────────────────────────────┤
│ Validation Methods:                                  │
│ + validate() : Tuple[bool, List[str]]                │
│ + check_uniqueness() : Tuple[bool, str]              │
├──────────────────────────────────────────────────────┤
│ CRUD Methods:                                        │
│ + save() : bool                                      │
│ + delete() : bool                                    │
├──────────────────────────────────────────────────────┤
│ Utility Methods:                                     │
│ + to_dict() : Dict                                   │
├──────────────────────────────────────────────────────┤
│ Magic Methods:                                       │
│ + __str__() : str                                    │
│ + __repr__() : str                                   │
│ + __eq__(other) : bool                               │
│ + __hash__() : int                                   │
├──────────────────────────────────────────────────────┤
│ Factory Methods:                                     │
│ + find(profile_id: int) : Profile                    │
│ + find_by_name(profile_name: str) : Profile          │
│ + all() : List[Profile]                              │
│ + search(profile_name: str = '',                     │
│          description: str = '') : List[Profile]       │
└──────────────────────────────────────────────────────┘
```

### Entity Class: `Request`

```
┌──────────────────────────────────────────────────────┐
│                    Request                           │
├──────────────────────────────────────────────────────┤
│ Class Constants:                                     │
│ - STATUS_ACTIVE = 'ACTIVE'                           │
│ - STATUS_SUSPENDED = 'SUSPENDED'                     │
│ - STATUS_FULFILLED = 'FULFILLED'                     │
│ - STATUS_CANCELLED = 'CANCELLED'                     │
│ - VALID_STATUSES: List[str]                          │
├──────────────────────────────────────────────────────┤
│ Instance Variables:                                  │
│ - id: int                                            │
│ - pin_user_id: int                                   │
│ - title: str                                         │
│ - description: str                                   │
│ - service_type: str                                  │
│ - region: str                                        │
│ - requested_by_date: str                             │
│ - image_url: str                                     │
│ - status: str (default: ACTIVE)                      │
│ - is_archived: bool                                  │
│ - view_count: int                                    │
│ - shortlist_count: int                               │
│ - created_at: str                                    │
│ - updated_at: str                                    │
│ - fulfilled_at: str                                  │
│ - suspended_at: str                                  │
├──────────────────────────────────────────────────────┤
│ Constructor:                                         │
│ + __init__(request_id: int = None,                   │
│            request_data: Dict = None)                 │
├──────────────────────────────────────────────────────┤
│ Validation Methods:                                  │
│ + validate() : Tuple[bool, List[str]]                │
│ + validate_pin_user() : Tuple[bool, str]             │
│ + validate_service_type() : Tuple[bool, str]         │
├──────────────────────────────────────────────────────┤
│ CRUD Methods:                                        │
│ + save() : bool                                      │
│ + delete() : bool                                    │
├──────────────────────────────────────────────────────┤
│ Status Methods:                                      │
│ + suspend(reason: str = None) : bool                 │
│ + fulfill() : bool                                   │
│ + archive() : bool                                   │
├──────────────────────────────────────────────────────┤
│ Counter Methods:                                     │
│ + increment_view_count() : bool                      │
│ + increment_shortlist_count() : bool                 │
│ + decrement_shortlist_count() : bool                 │
├──────────────────────────────────────────────────────┤
│ Utility Methods:                                     │
│ + to_dict() : Dict                                   │
├──────────────────────────────────────────────────────┤
│ Magic Methods:                                       │
│ + __str__() : str                                    │
│ + __repr__() : str                                   │
│ + __eq__(other) : bool                               │
│ + __hash__() : int                                   │
├──────────────────────────────────────────────────────┤
│ Factory Methods:                                     │
│ + find(request_id: int) : Request                    │
│ + all(include_archived: bool = False) :              │
│       List[Request]                                   │
│ + by_pin_user(pin_user_id: int) : List[Request]      │
│ + by_status(status: str) : List[Request]             │
│ + search(service_type: str = None,                   │
│          region: str = None, status: str = None,     │
│          pin_user_id: int = None) : List[Request]     │
├──────────────────────────────────────────────────────┤
│ Static Methods:                                      │
│ + get_service_types() : List[Dict]                   │
│ + get_categories() : List[str]                       │
└──────────────────────────────────────────────────────┘
```

### Entity Class: `Shortlist`

```
┌──────────────────────────────────────────────────────┐
│                   Shortlist                          │
├──────────────────────────────────────────────────────┤
│ Class Constants:                                     │
│ - STATUS_SHORTLISTED = 'SHORTLISTED'                 │
│ - STATUS_IN_PROGRESS = 'IN_PROGRESS'                 │
│ - STATUS_COMPLETED = 'COMPLETED'                     │
│ - STATUS_DECLINED = 'DECLINED'                       │
│ - VALID_STATUSES: List[str]                          │
├──────────────────────────────────────────────────────┤
│ Instance Variables:                                  │
│ - id: int                                            │
│ - csr_user_id: int                                   │
│ - request_id: int                                    │
│ - status: str (default: SHORTLISTED)                 │
│ - notes: str                                         │
│ - volunteered_hours: float                           │
│ - completion_date: str                               │
│ - feedback_from_pin: str                             │
│ - shortlisted_at: str                                │
│ - updated_at: str                                    │
│ - requests: Dict (joined request data)               │
├──────────────────────────────────────────────────────┤
│ Constructor:                                         │
│ + __init__(shortlist_id: int = None,                 │
│            shortlist_data: Dict = None)               │
├──────────────────────────────────────────────────────┤
│ Validation Methods:                                  │
│ + validate() : Tuple[bool, List[str]]                │
│ + check_duplicate() : Tuple[bool, str]               │
│ + validate_request_active() : Tuple[bool, str]       │
├──────────────────────────────────────────────────────┤
│ CRUD Methods:                                        │
│ + save() : bool                                      │
│   - Checks duplicate                                 │
│   - Validates request is active                      │
│   - Increments request.shortlist_count               │
│                                                       │
│ + delete() : bool                                    │
│   - Decrements request.shortlist_count               │
├──────────────────────────────────────────────────────┤
│ Status Methods:                                      │
│ + mark_in_progress() : bool                          │
│ + mark_completed(volunteered_hours: float = None,    │
│                  feedback: str = None) : bool         │
├──────────────────────────────────────────────────────┤
│ Utility Methods:                                     │
│ + to_dict() : Dict                                   │
│ + get_csr_user() : User                              │
│ + to_assignment_dict() : Dict                        │
├──────────────────────────────────────────────────────┤
│ Magic Methods:                                       │
│ + __str__() : str                                    │
│ + __repr__() : str                                   │
│ + __eq__(other) : bool                               │
│ + __hash__() : int                                   │
├──────────────────────────────────────────────────────┤
│ Factory Methods:                                     │
│ + find(shortlist_id: int) : Shortlist                │
│ + all() : List[Shortlist]                            │
│ + by_csr_user(csr_user_id: int,                      │
│               status: str = None) : List[Shortlist]   │
│ + by_request(request_id: int) : List[Shortlist]      │
│ + active_assignment_for_request(request_id: int):    │
│       Shortlist                                       │
│ + search(csr_user_id: int = None,                    │
│          request_id: int = None,                     │
│          status: str = None) : List[Shortlist]        │
│ + find_by_csr_and_request(csr_user_id: int,          │
│          request_id: int) : Shortlist                 │
└──────────────────────────────────────────────────────┘
```

---

## Utility Classes

### Class: `Validators`

```
┌──────────────────────────────────────────────────────┐
│                 Validators                           │
├──────────────────────────────────────────────────────┤
│ Static Methods:                                      │
│ + validate_username(username: str) :                 │
│       Tuple[bool, str]                                │
│   - 3-50 characters                                  │
│   - Alphanumeric and underscore only                 │
│                                                       │
│ + validate_password(password: str) :                 │
│       Tuple[bool, str]                                │
│   - Minimum 8 characters                             │
│                                                       │
│ + validate_email(email: str) : Tuple[bool, str]      │
│   - Must contain @                                   │
│   - Basic email format                               │
│                                                       │
│ + validate_full_name(name: str) :                    │
│       Tuple[bool, str]                                │
│   - 2-100 characters                                 │
│                                                       │
│ + validate_role_id(role_id) : Tuple[bool, str]       │
│   - Must be integer                                  │
│   - Must be positive                                 │
└──────────────────────────────────────────────────────┘
```

### Class: `Sanitizers`

```
┌──────────────────────────────────────────────────────┐
│                 Sanitizers                           │
├──────────────────────────────────────────────────────┤
│ Static Methods:                                      │
│ + sanitize_string(value: str) : str                  │
│   - Strips whitespace                                │
│   - Removes dangerous characters                     │
│                                                       │
│ + sanitize_username(username: str) : str             │
│   - Strips whitespace                                │
│   - Converts to lowercase                            │
│   - Removes non-alphanumeric except underscore       │
│                                                       │
│ + sanitize_email(email: str) : str                   │
│   - Strips whitespace                                │
│   - Converts to lowercase                            │
│                                                       │
│ + sanitize_user_data(data: Dict) : Dict              │
│   - Sanitizes all user fields                        │
│   - Returns cleaned dictionary                       │
└──────────────────────────────────────────────────────┘
```

### Class: `TokenHelpers`

```
┌──────────────────────────────────────────────────────┐
│                TokenHelpers                          │
├──────────────────────────────────────────────────────┤
│ Static Methods:                                      │
│ + extract_token_from_header(header: str) : str       │
│   - Extracts Bearer token from Authorization header  │
│                                                       │
│ + decode_token(token: str) : Dict                    │
│   - Decodes JWT token                                │
│   - Returns payload                                  │
└──────────────────────────────────────────────────────┘
```

### Class: `RequestHelpers`

```
┌──────────────────────────────────────────────────────┐
│                RequestHelpers                        │
├──────────────────────────────────────────────────────┤
│ Static Methods:                                      │
│ + validate_required_fields(data: Dict,               │
│       required: List[str]) : Tuple[bool, str, List]   │
│   - Checks all required fields present               │
│   - Returns validation result and missing fields     │
│                                                       │
│ + extract_pagination_params(request) :               │
│       Tuple[int, int]                                 │
│   - Gets page and limit from query params            │
└──────────────────────────────────────────────────────┘
```

### Class: `ResponseHelpers`

```
┌──────────────────────────────────────────────────────┐
│                ResponseHelpers                       │
├──────────────────────────────────────────────────────┤
│ Static Methods:                                      │
│ + success_response(data=None, message='Success',     │
│       status_code=200) : Tuple[Dict, int]             │
│   - Formats success response                         │
│   - Returns {success: true, data, message}           │
│                                                       │
│ + error_response(message='Error',                    │
│       error_code='ERROR',                             │
│       status_code=400, details=None) :                │
│       Tuple[Dict, int]                                 │
│   - Formats error response                           │
│   - Returns {success: false, error_code, message}    │
└──────────────────────────────────────────────────────┘
```

### Class: `DataHelpers`

```
┌──────────────────────────────────────────────────────┐
│                 DataHelpers                          │
├──────────────────────────────────────────────────────┤
│ Static Methods:                                      │
│ + format_user_response(user_dict: Dict) : Dict       │
│   - Removes sensitive data (password)                │
│   - Formats timestamps                               │
│                                                       │
│ + format_request_response(request_dict: Dict) : Dict │
│   - Formats request data for API response            │
│                                                       │
│ + format_shortlist_response(shortlist_dict: Dict):   │
│       Dict                                            │
│   - Formats shortlist with joined request data       │
└──────────────────────────────────────────────────────┘
```

### Class: `ImageUpload`

```
┌──────────────────────────────────────────────────────┐
│                 ImageUpload                          │
├──────────────────────────────────────────────────────┤
│ Functions:                                           │
│ + save_base64_image(base64_data: str,                │
│       filename_prefix: str) :                         │
│       Tuple[bool, str, str]                           │
│   - Decodes base64 image                             │
│   - Generates unique filename                        │
│   - Saves to file system                             │
│   - Returns (success, image_url, error_msg)          │
│                                                       │
│ + delete_image(image_url: str) : bool                │
│   - Deletes image file from file system              │
└──────────────────────────────────────────────────────┘
```

---

## Class Relationships

### Authentication Flow
```
LoginBoundary → LoginController → User (Entity)
                                ↓
                          Token Generation
```

### User Account Management Flow
```
UserAccountBoundary → CreateUserAccountController → User (Entity)
                    → ViewUserAccountController   → User (Entity)
                    → UpdateUserAccountController → User (Entity)
                    → SuspendUserAccountController → User (Entity)
                    → SearchUserAccountController → User (Entity)
```

### Request Management Flow
```
RequestBoundary → CreateNewPINRequestController → Request (Entity)
                                                → ImageUpload (Utility)
                → GetPINRequestsController      → Request (Entity)
                → ViewPINRequestController      → Request (Entity)
                → UpdatePINRequestController    → Request (Entity)
                → SearchPINRequestController    → Request (Entity)
```

### Shortlist Management Flow
```
ShortlistBoundary → AddToShortlistController → Shortlist (Entity)
                                             → Request (Entity)
                  → GetShortlistController   → Shortlist (Entity)
                  → RemoveFromShortlistController → Shortlist (Entity)
                  → UpdateShortlistStatusController → Shortlist (Entity)
```

### Entity Relationships
```
User (1) ←→ (N) Request
User (1) ←→ (N) Shortlist
Role (1) ←→ (N) User
Request (1) ←→ (N) Shortlist
Profile (1) ←→ (N) User (potential)
```

---

## Design Patterns Used

### 1. Boundary-Control-Entity (BCE)
- **Boundary**: HTTP endpoints (Flask blueprints)
- **Control**: Controllers with business logic
- **Entity**: Domain objects with data and operations

### 2. Factory Pattern
- Entity classes use factory methods (class methods) for object creation
- Examples: `User.find()`, `Request.by_pin_user()`, `Role.all()`

### 3. Active Record Pattern
- Entities encapsulate both data and database operations
- Instance methods perform CRUD operations
- Examples: `user.save()`, `request.delete()`, `shortlist.mark_completed()`

### 4. Singleton Pattern
- Supabase client configuration
- Single instance shared across application

### 5. Strategy Pattern
- Validators for different field types
- Sanitizers for different data types

---

## End of BCE Class Diagrams


