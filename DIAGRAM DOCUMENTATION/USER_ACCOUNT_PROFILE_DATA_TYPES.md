# User Account & User Profile - Data Types Reference

## Overview
This document provides a comprehensive reference of all data types used in the User Account and User Profile entities for CRUD operations.

---

## Table of Contents
1. [User Entity - Data Types](#user-entity---data-types)
2. [Profile Entity - Data Types](#profile-entity---data-types)
3. [Type Hints Reference](#type-hints-reference)
4. [Database Column Types](#database-column-types)

---

## User Entity - Data Types

### Imports
```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
```

---

### CRUD Methods with Data Types

#### 1. CREATE - `create_user()`

```python
@staticmethod
def create_user(
    username: str, 
    password: str, 
    email: str, 
    full_name: str, 
    role_id: int
) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `username` | `str` | User's username | `"john_doe"` |
| `password` | `str` | Plain text password (will be hashed) | `"SecurePass123"` |
| `email` | `str` | User's email address | `"john@example.com"` |
| `full_name` | `str` | User's full name | `"John Doe"` |
| `role_id` | `int` | Foreign key to roles table | `1` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Success**: `{'data': user_dict}` where `user_dict` is `Dict`
- **Error**: `{'error': str, 'message': str}` where both are `str`
- **None**: Not returned (always returns `Dict`)

**Example Return (Success):**
```python
{
    'data': {
        'id': 42,                    # int
        'username': 'john_doe',      # str
        'password': 'pbkdf2:...',    # str (hashed)
        'email': 'john@example.com', # str
        'full_name': 'John Doe',     # str
        'role_id': 1,                # int
        'is_active': True,           # bool
        'created_at': '2025-11-08T...' # str (ISO datetime)
    }
}
```

**Example Return (Error):**
```python
{
    'error': 'USERNAME_EXISTS',              # str
    'message': 'Username already exists'     # str
}
```

---

#### 2. READ - `get_user_by_id()`

```python
@staticmethod
def get_user_by_id(user_id: int) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Found**: `Dict` containing user data
- **Not Found**: `None`

**Example Return:**
```python
{
    'id': 42,                           # int
    'username': 'john_doe',             # str
    'password': 'pbkdf2:sha256:...',    # str
    'email': 'john@example.com',        # str
    'full_name': 'John Doe',            # str
    'role_id': 1,                       # int
    'is_active': True,                  # bool
    'last_login': '2025-11-08T...',     # str or None
    'created_at': '2025-10-27T...',     # str
    'roles': {                          # Dict (nested)
        'id': 1,                        # int
        'role_name': 'User Admin',      # str
        'role_code': 'USER_ADMIN'       # str
    }
}
```

---

#### 3. READ - `get_user_by_username()`

```python
@staticmethod
def get_user_by_username(username: str) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `username` | `str` | User's username | `"john_doe"` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Found**: `Dict` containing user data
- **Not Found**: `None`

---

#### 4. READ - `get_user_by_email()`

```python
@staticmethod
def get_user_by_email(email: str) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `email` | `str` | User's email | `"john@example.com"` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Found**: `Dict` containing user data
- **Not Found**: `None`

---

#### 5. READ - `get_all_users()`

```python
@staticmethod
def get_all_users() -> List[Dict]:
```

**Parameters:** None

**Return Type:** `List[Dict]`

**Return Values:**
- **Success**: `List` of `Dict` objects (can be empty list `[]`)
- **Error**: Empty list `[]`

**Example Return:**
```python
[
    {
        'id': 42,                    # int
        'username': 'john_doe',      # str
        'email': 'john@example.com', # str
        'full_name': 'John Doe',     # str
        'role_id': 1,                # int
        'is_active': True,           # bool
        'roles': { ... }             # Dict
    },
    {
        'id': 43,                    # int
        'username': 'jane_smith',    # str
        # ... more fields
    }
]
```

---

#### 6. UPDATE - `update_user()`

```python
@staticmethod
def update_user(user_id: int, updates: Dict) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |
| `updates` | `Dict` | Dictionary of fields to update | `{'email': 'new@example.com', 'full_name': 'John Smith'}` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Success**: `Dict` containing updated user data
- **Failure**: `None`

**Allowed Update Fields:**
```python
{
    'email': str,           # Optional
    'full_name': str,       # Optional
    'role_id': int,         # Optional
    'password': str,        # Optional (will be hashed)
    'is_active': bool       # Optional
}
```

**Example Return:**
```python
{
    'id': 42,                        # int
    'username': 'john_doe',          # str (unchanged)
    'email': 'new@example.com',      # str (updated)
    'full_name': 'John Smith',       # str (updated)
    'role_id': 1,                    # int
    'is_active': True,               # bool
    # ... other fields
}
```

---

#### 7. DELETE - `delete_user()`

```python
@staticmethod
def delete_user(user_id: int) -> bool:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |

**Return Type:** `bool`

**Return Values:**
- **Success**: `True`
- **Failure**: `False`

---

#### 8. SEARCH - `search_users()`

```python
@staticmethod
def search_users(
    username: str = '', 
    email: str = '', 
    full_name: str = ''
) -> List[Dict]:
```

**Parameters:**
| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `username` | `str` | `''` | Username to search | `"john"` |
| `email` | `str` | `''` | Email to search | `"@example.com"` |
| `full_name` | `str` | `''` | Full name to search | `"John"` |

**Return Type:** `List[Dict]`

**Return Values:**
- **Success**: `List` of matching `Dict` objects (can be empty)
- **Error**: Empty list `[]`

---

### Validation & Check Methods

#### 9. `username_exists()`

```python
@staticmethod
def username_exists(username: str) -> bool:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `username` | `str` | Username to check | `"john_doe"` |

**Return Type:** `bool`

**Return Values:**
- **Exists**: `True`
- **Not Exists**: `False`

---

#### 10. `email_exists()`

```python
@staticmethod
def email_exists(email: str) -> bool:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `email` | `str` | Email to check | `"john@example.com"` |

**Return Type:** `bool`

**Return Values:**
- **Exists**: `True`
- **Not Exists**: `False`

---

### Authentication Methods

#### 11. `authenticate_user()`

```python
@staticmethod
def authenticate_user(
    username: str, 
    password: str, 
    role_name: str = None
) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `username` | `str` | - | User's username | `"john_doe"` |
| `password` | `str` | - | Plain text password | `"SecurePass123"` |
| `role_name` | `str` | `None` | Optional role to verify | `"User Admin"` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Success**: `Dict` with user info and token
- **Failure**: `None`

**Example Return:**
```python
{
    'id': 42,                        # int
    'username': 'john_doe',          # str
    'email': 'john@example.com',     # str
    'full_name': 'John Doe',         # str
    'role_id': 1,                    # int
    'is_active': True,               # bool
    'token': 'eyJhbGciOi...',        # str (JWT)
    'role': {                        # Dict
        'id': 1,                     # int
        'name': 'User Admin',        # str
        'code': 'USER_ADMIN',        # str
        'dashboard_route': '/admin'  # str
    }
}
```

---

#### 12. `check_login()`

```python
@staticmethod
def check_login(username: str, password: str) -> Tuple[bool, Optional[Dict]]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `username` | `str` | User's username | `"john_doe"` |
| `password` | `str` | Plain text password | `"SecurePass123"` |

**Return Type:** `Tuple[bool, Optional[Dict]]`

**Return Values:**
- **Success**: `(True, user_dict)` where `user_dict` is `Dict`
- **Failure**: `(False, None)`

---

#### 13. `create_session_token()`

```python
@staticmethod
def create_session_token(user_id: int) -> str:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |

**Return Type:** `str`

**Return Values:**
- **Always**: JWT token string

**Example Return:**
```python
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MiwiZXhwIjoxNzMxMTU..."
```

---

#### 14. `verify_session_token()`

```python
@staticmethod
def verify_session_token(token: str) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `token` | `str` | JWT token | `"eyJhbGciOi..."` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Valid**: `Dict` with user data
- **Invalid/Expired**: `None`

---

#### 15. `invalidate_session_token()`

```python
@staticmethod
def invalidate_session_token(token: str) -> bool:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `token` | `str` | JWT token to invalidate | `"eyJhbGciOi..."` |

**Return Type:** `bool`

**Return Values:**
- **Valid token**: `True`
- **Invalid token**: `False`

---

### Utility Methods

#### 16. `activate_user()`

```python
@staticmethod
def activate_user(user_id: int) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Success**: `Dict` with updated user data
- **Failure**: `None`

---

#### 17. `deactivate_user()`

```python
@staticmethod
def deactivate_user(user_id: int) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Success**: `Dict` with updated user data
- **Failure**: `None`

---

#### 18. `log_user_activity()`

```python
@staticmethod
def log_user_activity(
    user_id: int, 
    activity_type: str, 
    activity_details: str
) -> None:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |
| `activity_type` | `str` | Type of activity | `"user_created"` |
| `activity_details` | `str` | Activity description | `"User account created with username: john_doe"` |

**Return Type:** `None`

**Return Values:** None (void function, best-effort logging)

---

#### 19. `get_user_complete_details()`

```python
@staticmethod
def get_user_complete_details(user_id: int) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `user_id` | `int` | User's ID | `42` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Success**: `Dict` with user, role, and profile data
- **Failure**: `None`

**Example Return:**
```python
{
    'id': 42,                        # int
    'username': 'john_doe',          # str
    'email': 'john@example.com',     # str
    'full_name': 'John Doe',         # str
    'role_id': 1,                    # int
    'is_active': True,               # bool
    'roles': {                       # Dict
        'id': 1,                     # int
        'role_name': 'User Admin',   # str
        'role_code': 'USER_ADMIN',   # str
        'dashboard_route': '/admin'  # str
    },
    'profile': {                     # Dict (optional)
        'user_id': 42,               # int
        'bio': 'Software engineer',  # str
        'phone': '+1234567890'       # str
    }
}
```

---

### Module-Level Functions

#### 20. `hash_password()`

```python
def hash_password(password: str) -> str:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `password` | `str` | Plain text password | `"SecurePass123"` |

**Return Type:** `str`

**Return Values:**
- **Always**: Hashed password string

**Example Return:**
```python
"pbkdf2:sha256:260000$xT5vbSJXTogjOMNG$0aa1d7df334ae42434084e941478966f..."
```

---

#### 21. `verify_password()`

```python
def verify_password(stored_hash: str, password: str) -> bool:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `stored_hash` | `str` | Hashed password from database | `"pbkdf2:sha256:..."` |
| `password` | `str` | Plain text password to verify | `"SecurePass123"` |

**Return Type:** `bool`

**Return Values:**
- **Match**: `True`
- **No Match**: `False`

---

## Profile Entity - Data Types

### Imports
```python
from typing import Dict, List, Optional, Tuple
from datetime import datetime
```

---

### CRUD Methods with Data Types

#### 1. CREATE - `create_profile()`

```python
@staticmethod
def create_profile(
    profile_name: str, 
    description: str = ''
) -> Tuple[bool, int]:
```

**Parameters:**
| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `profile_name` | `str` | - | Profile name | `"Administrator"` |
| `description` | `str` | `''` | Profile description | `"Full system access"` |

**Return Type:** `Tuple[bool, int]`

**Return Values:**
- **Success**: `(True, 201)`
- **Conflict**: `(False, 409)` - Profile already exists
- **Error**: `(False, 500)`

**Example Usage:**
```python
success, status_code = Profile.create_profile("Administrator", "Full access")
# Returns: (True, 201) or (False, 409) or (False, 500)
```

---

#### 2. READ - `get_profile_by_id()`

```python
@staticmethod
def get_profile_by_id(profile_id: int) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `profile_id` | `int` | Profile ID | `1` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Found**: `Dict` containing profile data
- **Not Found**: `None`

**Example Return:**
```python
{
    'id': 1,                              # int
    'profile_name': 'Administrator',      # str
    'description': 'Full system access',  # str
    'created_at': '2025-10-27T...',       # str (ISO datetime)
    'updated_at': '2025-11-08T...'        # str (ISO datetime)
}
```

---

#### 3. READ - `get_profile_by_name()`

```python
@staticmethod
def get_profile_by_name(profile_name: str) -> Optional[Dict]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `profile_name` | `str` | Profile name | `"Administrator"` |

**Return Type:** `Optional[Dict]`

**Return Values:**
- **Found**: `Dict` containing profile data
- **Not Found**: `None`

---

#### 4. READ - `get_all_profiles()`

```python
@staticmethod
def get_all_profiles() -> List[Dict]:
```

**Parameters:** None

**Return Type:** `List[Dict]`

**Return Values:**
- **Success**: `List` of `Dict` objects (can be empty list `[]`)
- **Error**: Empty list `[]`

**Example Return:**
```python
[
    {
        'id': 1,                              # int
        'profile_name': 'Administrator',      # str
        'description': 'Full system access',  # str
        'created_at': '2025-10-27T...',       # str
        'updated_at': '2025-11-08T...'        # str
    },
    {
        'id': 2,                              # int
        'profile_name': 'Manager',            # str
        'description': 'Management access',   # str
        'created_at': '2025-10-28T...',       # str
        'updated_at': '2025-11-08T...'        # str
    }
]
```

---

#### 5. UPDATE - `update_profile()`

```python
@staticmethod
def update_profile(profile_id: int, updates: Dict) -> Tuple[bool, int]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `profile_id` | `int` | Profile ID | `1` |
| `updates` | `Dict` | Dictionary of fields to update | `{'description': 'Updated description'}` |

**Return Type:** `Tuple[bool, int]`

**Return Values:**
- **Success**: `(True, 200)`
- **Not Found**: `(False, 404)`
- **Error**: `(False, 500)`

**Allowed Update Fields:**
```python
{
    'profile_name': str,    # Optional
    'description': str      # Optional
}
```

**Note:** `updated_at` is automatically set by the method.

---

#### 6. DELETE - `delete_profile()`

```python
@staticmethod
def delete_profile(profile_id: int) -> Tuple[bool, int]:
```

**Parameters:**
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `profile_id` | `int` | Profile ID | `1` |

**Return Type:** `Tuple[bool, int]`

**Return Values:**
- **Success**: `(True, 200)`
- **Error**: `(False, 500)`

**Note:** This method performs cascade delete of associated users.

---

#### 7. SEARCH - `search_profiles()`

```python
@staticmethod
def search_profiles(query: str = '') -> List[Dict]:
```

**Parameters:**
| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `query` | `str` | `''` | Search query | `"admin"` |

**Return Type:** `List[Dict]`

**Return Values:**
- **Success**: `List` of matching `Dict` objects (can be empty)
- **Error**: Empty list `[]`

**Search Fields:** Searches in `profile_name` and `description` (case-insensitive)

---

## Type Hints Reference

### Basic Types
| Type | Description | Example |
|------|-------------|---------|
| `str` | String | `"john_doe"`, `"john@example.com"` |
| `int` | Integer | `42`, `1`, `100` |
| `bool` | Boolean | `True`, `False` |
| `float` | Floating point | `3.14`, `99.99` |

### Complex Types
| Type | Description | Example |
|------|-------------|---------|
| `Dict` | Dictionary | `{'key': 'value', 'id': 42}` |
| `List` | List | `[1, 2, 3]`, `['a', 'b']` |
| `Tuple` | Tuple | `(True, 200)`, `(False, None)` |
| `Optional[T]` | Can be `T` or `None` | `Optional[Dict]` = `Dict` or `None` |

### Specialized Types
| Type | Description | Example |
|------|-------------|---------|
| `Optional[Dict]` | Dictionary or None | `{'id': 42}` or `None` |
| `List[Dict]` | List of dictionaries | `[{'id': 1}, {'id': 2}]` |
| `Tuple[bool, int]` | Tuple with bool and int | `(True, 200)` |
| `Tuple[bool, Optional[Dict]]` | Tuple with bool and optional dict | `(True, {'id': 42})` or `(False, None)` |

### Type Aliases Used
```python
from typing import Dict, List, Optional, Tuple

# Common patterns in the codebase:
UserDict = Dict[str, Any]           # User data dictionary
ProfileDict = Dict[str, Any]        # Profile data dictionary
StatusTuple = Tuple[bool, int]      # (success, status_code)
```

---

## Database Column Types

### users Table

| Column | Python Type | Database Type | Nullable | Example |
|--------|-------------|---------------|----------|---------|
| `id` | `int` | `SERIAL` | No | `42` |
| `username` | `str` | `VARCHAR(50)` | No | `"john_doe"` |
| `password` | `str` | `VARCHAR(255)` | No | `"pbkdf2:sha256:..."` |
| `email` | `str` | `VARCHAR(255)` | No | `"john@example.com"` |
| `full_name` | `str` | `VARCHAR(100)` | No | `"John Doe"` |
| `role_id` | `int` | `INTEGER` | No | `1` |
| `is_active` | `bool` | `BOOLEAN` | No | `True` |
| `last_login` | `str` or `None` | `TIMESTAMP` | Yes | `"2025-11-08T14:30:00"` |
| `created_at` | `str` | `TIMESTAMP` | No | `"2025-10-27T00:20:40"` |

### profiles Table

| Column | Python Type | Database Type | Nullable | Example |
|--------|-------------|---------------|----------|---------|
| `id` | `int` | `SERIAL` | No | `1` |
| `profile_name` | `str` | `VARCHAR(100)` | No | `"Administrator"` |
| `description` | `str` | `TEXT` | Yes | `"Full system access"` |
| `created_at` | `str` | `TIMESTAMP` | No | `"2025-10-27T00:20:40"` |
| `updated_at` | `str` | `TIMESTAMP` | No | `"2025-11-08T14:30:00"` |

---

## Data Type Conversion

### Python → Database
```python
# String (no conversion needed)
username: str = "john_doe"  # → VARCHAR in DB

# Integer (no conversion needed)
user_id: int = 42  # → INTEGER in DB

# Boolean (no conversion needed)
is_active: bool = True  # → BOOLEAN in DB

# DateTime (converted to ISO string)
from datetime import datetime
created_at = datetime.utcnow().isoformat()  # → "2025-11-08T14:30:00" → TIMESTAMP in DB

# Password (hashed before storage)
password: str = "SecurePass123"
hashed = hash_password(password)  # → "pbkdf2:sha256:..." → VARCHAR in DB
```

### Database → Python
```python
# All database values come back as Python types via Supabase client
result = supabase.table('users').select('*').eq('id', 42).execute()
user = result.data[0]  # Dict

# Access with correct types:
user_id: int = user['id']                    # int
username: str = user['username']             # str
is_active: bool = user['is_active']          # bool
last_login: Optional[str] = user['last_login']  # str or None
```

---

## Type Safety Best Practices

### 1. Always Use Type Hints
```python
# Good ✅
def create_user(username: str, email: str) -> Optional[Dict]:
    pass

# Bad ❌
def create_user(username, email):
    pass
```

### 2. Handle Optional Types
```python
# Good ✅
user = User.get_user_by_id(42)
if user is not None:
    print(user['username'])

# Bad ❌
user = User.get_user_by_id(42)
print(user['username'])  # Can crash if user is None
```

### 3. Validate Types Before Database Operations
```python
# Good ✅
if not isinstance(role_id, int):
    return False, "role_id must be an integer"

# Bad ❌
# Assuming role_id is correct type
```

### 4. Use Type Checking Tools
```bash
# Install mypy
pip install mypy

# Run type checker
mypy src/entity/user.py
mypy src/entity/profile.py
```

---

## Summary

### User Entity - Method Count by Return Type
- **`Optional[Dict]`**: 10 methods (get, authenticate, update, etc.)
- **`List[Dict]`**: 2 methods (get_all, search)
- **`bool`**: 3 methods (delete, username_exists, email_exists)
- **`str`**: 1 method (create_session_token)
- **`Tuple[bool, Optional[Dict]]`**: 1 method (check_login)
- **`None`**: 1 method (log_user_activity)

### Profile Entity - Method Count by Return Type
- **`Tuple[bool, int]`**: 3 methods (create, update, delete)
- **`Optional[Dict]`**: 2 methods (get_by_id, get_by_name)
- **`List[Dict]`**: 2 methods (get_all, search)

### Total Methods
- **User Entity**: 21 methods + 2 module functions = **23 functions**
- **Profile Entity**: **7 methods**
- **Grand Total**: **30 functions**

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-08  
**Entities Covered**: User, Profile  
**Total Functions Documented**: 30


