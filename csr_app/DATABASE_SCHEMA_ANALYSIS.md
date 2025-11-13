# Database Schema Analysis: Supabase vs Entity Models

## Overview
This document provides a comprehensive analysis of the database schema used in the CSR Application, comparing the Supabase PostgreSQL database structure with the Python Entity models.

---

## 📊 Database Tables Summary

### 1. **`users` Table**

#### Supabase Schema (Inferred from Entity):
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,  -- Hashed using pbkdf2:sha256
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

#### Entity Model Fields (`user.py`):
- `id` (int) - Primary key
- `username` (str) - Unique identifier for login
- `password` (str) - Hashed password (pbkdf2:sha256 or scrypt)
- `email` (str) - User email address
- `full_name` (str) - Full display name
- `role_id` (int) - Foreign key to `roles` table
- `is_active` (bool) - Account status flag
- `created_at` (str) - Account creation timestamp
- `last_login` (str) - Last successful login timestamp
- `roles` (dict) - **Joined data** from `roles` table (not in DB, populated via query)

#### Key Methods:
- **Authentication**: `authenticate()`, `verify_password()`, `generate_session_token()`
- **Factory Methods**: `find()`, `find_by_username()`, `find_by_email()`, `all()`
- **Instance Methods**: `save()`, `update()`, `delete()`, `update_last_login()`

---

### 2. **`roles` Table**

#### Supabase Schema:
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR UNIQUE NOT NULL,  -- e.g., 'User Admin', 'PIN', 'CSR Rep'
    role_code VARCHAR UNIQUE NOT NULL,  -- e.g., 'USER_ADMIN', 'PIN', 'CSR_REP'
    description TEXT,
    dashboard_route VARCHAR NOT NULL,   -- e.g., '/admin/dashboard', '/pin/dashboard'
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Entity Model Fields (`role.py`):
- `id` (int) - Primary key
- `role_name` (str) - Human-readable role name
- `role_code` (str) - Code identifier for role
- `description` (str) - Role description
- `dashboard_route` (str) - Default dashboard path for this role
- `created_at` (str) - Creation timestamp

#### Predefined Roles (Constants in Entity):
- `USER_ADMIN` - "User Admin" → `/admin/dashboard`
- `PIN` - "PIN" → `/pin/dashboard`
- `CSR_REP` - "CSR Rep" → `/csr/dashboard`
- `PLATFORM_MANAGEMENT` - "Platform Management" → `/platform/dashboard`

#### Key Methods:
- **Factory Methods**: `find()`, `find_by_name()`, `find_by_code()`, `all()`, `public_roles()`
- **Instance Methods**: `save()`, `update()`, `delete()`, `get_dashboard_route()`

---

### 3. **`requests` Table** (PIN Service Requests)

#### Supabase Schema:
```sql
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    pin_user_id INTEGER REFERENCES users(id) NOT NULL,  -- PIN user who created request
    title VARCHAR NOT NULL,
    description TEXT,
    service_type VARCHAR NOT NULL,   -- e.g., 'Grocery Shopping', 'Medical Escort'
    region VARCHAR NOT NULL,          -- e.g., 'Hougang', 'Clementi'
    requested_by_date DATE,           -- Deadline for request
    image_url VARCHAR,                -- Path to uploaded image
    status VARCHAR DEFAULT 'ACTIVE',  -- 'ACTIVE', 'SUSPENDED', 'FULFILLED', 'CANCELLED'
    is_archived BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,     -- Number of times viewed by CSRs
    shortlist_count INTEGER DEFAULT 0, -- Number of CSRs who shortlisted
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    fulfilled_at TIMESTAMP,
    suspended_at TIMESTAMP
);
```

#### Entity Model Fields (`request.py`):
- `id` (int) - Primary key
- `pin_user_id` (int) - Foreign key to `users` table (PIN user)
- `title` (str) - Request title
- `description` (str) - Detailed description
- `service_type` (str) - Type of service needed
- `region` (str) - Geographic location
- `requested_by_date` (str) - Deadline date
- `image_url` (str) - Image path
- `status` (str) - Current status (default: `'ACTIVE'`)
- `is_archived` (bool) - Archive flag
- `view_count` (int) - View counter
- `shortlist_count` (int) - Shortlist counter
- `created_at` (str) - Creation timestamp
- `updated_at` (str) - Last update timestamp
- `fulfilled_at` (str) - Fulfillment timestamp
- `suspended_at` (str) - Suspension timestamp

#### Valid Statuses (Constants):
- `STATUS_ACTIVE` = `'ACTIVE'` - Open for volunteers
- `STATUS_SUSPENDED` = `'SUSPENDED'` - Temporarily paused
- `STATUS_FULFILLED` = `'FULFILLED'` - Completed
- `STATUS_CANCELLED` = `'CANCELLED'` - Cancelled by PIN user

#### Key Methods:
- **State Management**: `suspend()`, `fulfill()`, `archive()`
- **Counters**: `increment_view_count()`, `increment_shortlist_count()`, `decrement_shortlist_count()`
- **Factory Methods**: `find()`, `all()`, `by_pin_user()`, `by_status()`, `active()`, `search()`
- **Instance Methods**: `save()`, `update()`, `delete()`

---

### 4. **`shortlist` Table** (CSR Shortlist/Assignments)

#### Supabase Schema:
```sql
CREATE TABLE shortlist (
    id SERIAL PRIMARY KEY,
    csr_user_id INTEGER REFERENCES users(id) NOT NULL,  -- CSR user
    request_id INTEGER REFERENCES requests(id) NOT NULL,
    status VARCHAR DEFAULT 'SHORTLISTED',  -- 'SHORTLISTED', 'IN_PROGRESS', 'COMPLETED', 'DECLINED'
    notes TEXT,                             -- CSR notes about the opportunity
    volunteered_hours DECIMAL(5,2),         -- Volunteer rating from PIN user (1-5 scale)
    completion_date TIMESTAMP,              -- When marked as completed
    feedback_from_pin TEXT,                 -- Feedback from PIN user
    shortlisted_at TIMESTAMP DEFAULT NOW(), -- When added to shortlist
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(csr_user_id, request_id)  -- One CSR can only shortlist a request once
);
```

#### Entity Model Fields (`shortlist.py`):
- `id` (int) - Primary key
- `csr_user_id` (int) - Foreign key to `users` table (CSR Rep)
- `request_id` (int) - Foreign key to `requests` table
- `status` (str) - Current status (default: `'SHORTLISTED'`)
- `notes` (str) - CSR's notes
- `volunteered_hours` (float) - Volunteer rating given by PIN user (1-5 scale)
- `completion_date` (str) - Completion timestamp
- `feedback_from_pin` (str) - PIN user's feedback
- `shortlisted_at` (str) - When shortlisted
- `updated_at` (str) - Last update
- `requests` (dict) - **Joined data** from `requests` table (not in DB, populated via query)

#### Valid Statuses (Constants):
- `STATUS_SHORTLISTED` = `'SHORTLISTED'` - Saved for later
- `STATUS_IN_PROGRESS` = `'IN_PROGRESS'` - Currently volunteering
- `STATUS_COMPLETED` = `'COMPLETED'` - Finished
- `STATUS_DECLINED` = `'DECLINED'` - CSR declined

#### Key Methods:
- **State Management**: `mark_in_progress()`, `mark_completed()`, `decline()`
- **Factory Methods**: `find()`, `by_csr_user()`, `by_request()`, `search()`, `get_active_assignment()`
- **Instance Methods**: `save()`, `update()`, `delete()`

---

### 5. **`request_status_history` Table** (Audit Log)

#### Supabase Schema:
```sql
CREATE TABLE request_status_history (
    id SERIAL PRIMARY KEY,
    request_id INTEGER REFERENCES requests(id) NOT NULL,
    old_status VARCHAR,               -- Previous status
    new_status VARCHAR NOT NULL,      -- New status
    reason TEXT,                      -- Optional reason for status change
    changed_at TIMESTAMP DEFAULT NOW(),
    changed_by INTEGER REFERENCES users(id)  -- User who made the change (optional)
);
```

#### Purpose:
This is an **audit log table** that tracks all status changes for requests. It's used for:
- **Compliance & Auditing**: Track who changed what and when
- **History Tracking**: View the lifecycle of a request
- **Analytics**: Understand request flow patterns

#### Entity Model:
**No dedicated entity class** - This table is written to directly by the `Request` entity's state transition methods:
- `Request.suspend()` → Logs `ACTIVE` → `SUSPENDED` transition
- `Request.fulfill()` → Logs `old_status` → `FULFILLED` transition

#### Example Records:
```python
# When a request is suspended:
{
  'request_id': 5,
  'old_status': 'ACTIVE',
  'new_status': 'SUSPENDED',
  'reason': 'PIN user temporarily unavailable',
  'changed_at': '2025-11-10T15:30:00'
}

# When a request is fulfilled:
{
  'request_id': 5,
  'old_status': 'SUSPENDED',
  'new_status': 'FULFILLED',
  'reason': None,
  'changed_at': '2025-11-11T10:00:00'
}
```

#### Key Characteristics:
- **Write-Only**: Records are only inserted, never updated or deleted
- **No Entity Class**: Direct database inserts from `Request` entity
- **Graceful Failures**: Logging failures don't prevent the main operation (wrapped in try-except)
- **Optional Fields**: `reason` and `changed_by` can be NULL

---

## 🔗 Relationships

### Entity Relationship Diagram (ERD):

```
┌─────────────┐
│   roles     │
│─────────────│
│ id (PK)     │
│ role_name   │
│ role_code   │
└─────────────┘
       │
       │ 1:N
       ▼
┌─────────────┐
│   users     │
│─────────────│
│ id (PK)     │
│ username    │
│ role_id (FK)│
└─────────────┘
       │
       ├──────────────┐
       │ 1:N          │ 1:N
       ▼              ▼
┌─────────────┐  ┌──────────────┐
│  requests   │  │  shortlist   │
│─────────────│  │──────────────│
│ id (PK)     │  │ id (PK)      │
│ pin_user_id │  │ csr_user_id  │
│   (FK)      │  │   (FK)       │
│ title       │  │ request_id   │
│ status      │  │   (FK)       │
└─────────────┘  └──────────────┘
       │                │
       │                └────────────────┘
       │                     N:M
       │
       │ 1:N
       ▼
┌──────────────────────────┐
│ request_status_history   │
│──────────────────────────│
│ id (PK)                  │
│ request_id (FK)          │
│ old_status               │
│ new_status               │
│ reason                   │
│ changed_at               │
└──────────────────────────┘
```

### Relationships Explained:

1. **`users` ↔ `roles`**: Many-to-One
   - Each user belongs to one role
   - One role can have many users
   - FK: `users.role_id` → `roles.id`

2. **`users` (PIN) ↔ `requests`**: One-to-Many
   - A PIN user can create many requests
   - Each request belongs to one PIN user
   - FK: `requests.pin_user_id` → `users.id`

3. **`users` (CSR) ↔ `shortlist`**: One-to-Many
   - A CSR user can shortlist many requests
   - Each shortlist entry belongs to one CSR user
   - FK: `shortlist.csr_user_id` → `users.id`

4. **`requests` ↔ `shortlist`**: One-to-Many
   - A request can be shortlisted by many CSR users
   - Each shortlist entry references one request
   - FK: `shortlist.request_id` → `requests.id`

5. **`users` (CSR) ↔ `requests`**: Many-to-Many (via `shortlist`)
   - CSR users and requests have a many-to-many relationship
   - Implemented through the `shortlist` junction table
   - UNIQUE constraint: `(csr_user_id, request_id)` prevents duplicates

6. **`requests` ↔ `request_status_history`**: One-to-Many
   - A request can have many status change records
   - Each history entry belongs to one request
   - FK: `request_status_history.request_id` → `requests.id`
   - **Audit log only**: No bidirectional navigation (history is write-only)

---

## 🔍 Key Differences: Supabase vs Entity

### 1. **Joined Data (Not in DB)**
The entity models include **virtual fields** that don't exist in the database tables but are populated through SQL JOINs:

- `User.roles` → Joined from `roles` table
- `Shortlist.requests` → Joined from `requests` table

**Example Query:**
```python
# Entity loads with JOIN
result = supabase.table('users').select('*, roles(*)').eq('id', user_id).execute()
# Result includes:
# {
#   'id': 1,
#   'username': 'john',
#   'roles': {'role_name': 'CSR Rep', 'role_code': 'CSR_REP', ...}
# }
```

### 2. **OOP Abstraction**
Entities provide object-oriented abstraction over raw database operations:

**Database (Raw Supabase):**
```python
supabase.table('users').update({'full_name': 'New Name'}).eq('id', 42).execute()
```

**Entity (OOP):**
```python
user = User.find(42)
user.full_name = 'New Name'
user.save()  # Handles validation, uniqueness checks, etc.
```

### 3. **Business Logic Encapsulation**
Entities encapsulate business logic that doesn't exist in the database:

- **Validation**: `validate()` methods check data integrity before DB operations
- **Password Hashing**: `User` entity handles password hashing/verification
- **Token Generation**: `User.generate_session_token()` creates JWTs
- **State Transitions**: `Request.suspend()`, `Request.fulfill()`, `Shortlist.mark_completed()`
- **Counter Management**: `Request.increment_view_count()` updates analytics

### 4. **Data Type Mapping**

| Database Type | Python Entity Type |
|--------------|-------------------|
| SERIAL (int) | `int` |
| VARCHAR/TEXT | `str` |
| BOOLEAN | `bool` |
| TIMESTAMP | `str` (ISO format) |
| DECIMAL | `float` |

**Note:** Timestamps are stored in the database as PostgreSQL `TIMESTAMP` but represented as ISO format strings in Python entities (e.g., `'2025-11-10T23:22:07.565286+00:00'`).

---

## 📝 Special Fields & Their Purpose

### 1. **`volunteered_hours` in `shortlist` table**
**Actual Usage:** Stores volunteer **rating** (1-5 scale), not actual hours
- Despite the misleading name, this field stores the rating given by PIN users to CSR volunteers
- Used for: Volunteer performance tracking and statistics

### 2. **`view_count` in `requests` table**
**Purpose:** Analytics tracking
- Incremented each time a CSR views the request details
- Used for: PIN user analytics (US-27 & US-28)

### 3. **`shortlist_count` in `requests` table**
**Purpose:** Popularity indicator
- Incremented when a CSR adds to shortlist
- Decremented when removed from shortlist
- Used for: PIN user analytics and trending requests

### 4. **Timestamp Fields**
Multiple timestamp fields track state history:
- `created_at` - Initial creation
- `updated_at` - Last modification
- `fulfilled_at` - When marked as fulfilled
- `suspended_at` - When suspended
- `completion_date` - When CSR completed work

---

## 🔐 Security & Data Integrity

### 1. **Password Storage**
- Passwords are **never stored in plaintext**
- Hashed using `pbkdf2:sha256` (or `scrypt` if available)
- Entity handles hashing automatically in `User.save()`

### 2. **Unique Constraints**
- `users.username` - UNIQUE
- `users.email` - UNIQUE
- `roles.role_name` - UNIQUE
- `roles.role_code` - UNIQUE
- `shortlist.(csr_user_id, request_id)` - UNIQUE (composite)

### 3. **Foreign Key Relationships**
All FK relationships are enforced at the database level to maintain referential integrity.

### 4. **Validation**
All entities implement `validate()` methods that check:
- Required fields are present
- Field formats are valid (email, dates, etc.)
- Business rules are satisfied (e.g., status must be in `VALID_STATUSES`)

---

## 🚀 Query Patterns

### Factory Methods (Class Methods)
Used to **retrieve** data from the database and return entity instances:

```python
# Single record
user = User.find(42)
role = Role.find_by_code('CSR_REP')

# Multiple records
all_users = User.all()
active_requests = Request.active()
shortlist_items = Shortlist.by_csr_user(user_id=43)

# Search with filters
requests = Request.search(
    status='ACTIVE',
    service_type='Grocery Shopping',
    region='Hougang'
)
```

### Instance Methods
Used to **manipulate** data on loaded entities:

```python
# Create new
user = User()
user.username = 'john_doe'
user.save()  # INSERT

# Update existing
user = User.find(42)
user.full_name = 'John Smith'
user.save()  # UPDATE

# State transitions
request = Request.find(1)
request.fulfill()  # Changes status + sets fulfilled_at

# Delete
request.delete()  # DELETE FROM requests
```

---

## 📊 Summary Table

| **Aspect** | **Supabase (Database)** | **Entity Models (Python)** |
|-----------|------------------------|---------------------------|
| **Tables Count** | 5 tables (`users`, `roles`, `requests`, `shortlist`, `request_status_history`) | 4 entity classes (`User`, `Role`, `Request`, `Shortlist`) |
| **Data Storage** | PostgreSQL tables with columns | Python objects with attributes |
| **Relationships** | Foreign keys | Joined data in dictionaries |
| **Business Logic** | None (pure data) | Validation, state management, authentication |
| **Access Pattern** | SQL queries via Supabase client | OOP methods (`.save()`, `.find()`, etc.) |
| **Type System** | SQL types (INTEGER, VARCHAR, etc.) | Python types (int, str, bool) |
| **Constraints** | UNIQUE, NOT NULL, FK at DB level | `validate()` and `check_uniqueness()` in code |
| **State Management** | Manual UPDATE queries | Instance methods (`suspend()`, `fulfill()`) |
| **Audit Logging** | `request_status_history` table | Automatic inserts from `Request` entity |
| **Abstraction Level** | Low (raw data) | High (business objects) |

---

## 🎯 Conclusion

Your database architecture follows a **clean separation of concerns**:

1. **Supabase (PostgreSQL)**: Handles persistent storage, relationships, and data integrity
2. **Entity Models (Python OOP)**: Provide business logic, validation, and abstraction

This design pattern (similar to **Active Record** or **Data Mapper** patterns) makes your code:
- ✅ More maintainable (business logic in one place)
- ✅ Easier to test (entities can be instantiated without DB)
- ✅ Type-safe (Python type hints)
- ✅ Database-agnostic (could swap Supabase for another DB with minimal changes)

The only minor issue is the **misleading `volunteered_hours` field name** (which actually stores ratings). Consider renaming it to `volunteer_rating` in a future migration for clarity.

