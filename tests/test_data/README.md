# Test Data for CSR Application

This directory contains JSON test data files used for automated testing with pytest.

## File Structure

```
test_data/
├── README.md                 # This file
├── roles.json               # Role definitions (4 roles)
├── user_accounts.json       # User account test data (100 users)
└── login_test_cases.json    # Existing login test scenarios
```

## 📋 roles.json

Contains the 4 role types used in the CSR application:

| Role Name | Role Code | Dashboard Route | Description |
|-----------|-----------|----------------|-------------|
| User Admin | ADMIN | /admin | Administrator with full system access |
| PIN | PIN | /pin | Person-In-Need who creates requests |
| CSR Rep | CSR | /csr | CSR Representative who fulfills requests |
| Platform Management | PLATFORM | /platform | Platform manager with oversight |

### Fields:
- `role_name` (string): Display name of the role
- `role_code` (string): Short code identifier
- `description` (string): Role description
- `dashboard_route` (string): Default dashboard path

---

## 👥 user_accounts.json

Contains 100 test user accounts with the following distribution:
- **PIN users**: ~40 accounts
- **CSR Rep users**: ~40 accounts
- **User Admin**: ~10 accounts
- **Platform Management**: ~10 accounts

### Fields:
- `email` (string): User email address (format: name@example.com)
- `password` (string): Plain text password for testing (secure passwords with special characters)
- `username` (string): Unique username (lowercase_underscore format)
- `full_name` (string): Full display name (Singapore-style names)
- `role_name` (string): Role assigned to user (matches roles.json)

### Example Record:
```json
{
  "email": "alice.tan@example.com",
  "password": "P@ssw0rd123!",
  "username": "alice_tan",
  "full_name": "Alice Tan Wei Ling",
  "role_name": "PIN"
}
```

### Password Format:
All passwords follow a secure pattern:
- At least 10 characters
- Contains uppercase letters
- Contains lowercase letters
- Contains numbers
- Contains special characters (!@#$)

---

## 🧪 login_test_cases.json

Contains specific test scenarios for login functionality:
- **valid_logins**: Successful login scenarios for each role
- **invalid_logins**: Failed login scenarios (wrong password, wrong username, etc.)
- **edge_cases**: Special cases (empty fields, SQL injection attempts, etc.)

---

## Usage in Tests

### Loading Role Data
```python
import json
import os

def load_roles():
    json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'roles.json')
    with open(json_path, 'r') as f:
        return json.load(f)
```

### Loading User Accounts
```python
def load_user_accounts():
    json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'user_accounts.json')
    with open(json_path, 'r') as f:
        return json.load(f)
```

### Example Test with User Accounts
```python
@pytest.fixture
def user_test_data():
    """Load user account test data"""
    json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'user_accounts.json')
    with open(json_path, 'r') as f:
        return json.load(f)

def test_bulk_user_login(client, user_test_data):
    """Test login with all 100 test users"""
    for user in user_test_data:
        response = client.post(
            '/api/auth/login',
            json={
                'username': user['username'],
                'password': user['password'],
                'role_name': user['role_name']
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
```

---

## Notes

1. **Database Setup**: These test users should be seeded into your test database before running tests
2. **Password Hashing**: When inserting into the database, passwords must be hashed using your application's password hashing method
3. **Cleanup**: Consider implementing teardown fixtures to clean up test data after tests run
4. **Isolation**: Each test should be independent and not rely on the state from previous tests

---

## Database Seeding Script

A seeding script is provided at `tests/seed_test_data.py` to easily insert or remove test data.

### Quick Start

```bash
# Activate virtual environment
cd csr_app
venv\Scripts\activate

# Run seeding script
python tests/seed_test_data.py
```

### Seeding Options

The script provides an interactive menu:

1. **Seed all (roles + users)** - Insert all 4 roles and 100 user accounts
2. **Seed roles only** - Insert only the 4 roles
3. **Seed users only** - Insert only the 100 user accounts
4. **Delete all test users** - Remove all 100 test user accounts
5. **Delete test roles** - Remove test roles (⚠️ Use with caution!)
6. **Exit**

### Usage Example

```bash
$ python tests/seed_test_data.py

============================================================
🌱 CSR TEST DATA SEEDING UTILITY
============================================================

Options:
  1. Seed all (roles + users)
  2. Seed roles only
  3. Seed users only
  4. Delete all test users
  5. Delete test roles (dangerous!)
  6. Exit

Enter your choice (1-6): 1

============================================================
🎭 SEEDING ROLES
============================================================
   ✅ User Admin (ADMIN)
   ✅ PIN (PIN)
   ✅ CSR Rep (CSR)
   ✅ Platform Management (PLATFORM)

📊 Summary:
   ✅ Created: 4
   ⚠️  Skipped: 0
   📋 Total: 4

============================================================
👥 SEEDING USER ACCOUNTS
============================================================
   [  1/100] ✅ alice_tan (PIN)
   [  2/100] ✅ bob_lim (CSR Rep)
   ...
```

### Programmatic Usage

You can also import and use the functions directly:

```python
from tests.seed_test_data import seed_all, seed_roles, seed_users

# Seed everything
seed_all()

# Or seed individually
seed_roles()
seed_users()
```

---

**Created**: November 13, 2025  
**Author**: CSR ScrumMasters Team

