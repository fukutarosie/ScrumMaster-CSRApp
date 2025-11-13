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

## Database Seeding Script Example

```python
from src.entity.user import User
from src.entity.role import Role
import json

def seed_test_users():
    """Seed test users into database"""
    # Load user data
    with open('tests/test_data/user_accounts.json', 'r') as f:
        users = json.load(f)
    
    for user_data in users:
        # Find role
        role = Role.find_by_name(user_data['role_name'])
        if not role:
            continue
        
        # Create user
        user = User()
        user.username = user_data['username']
        user.email = user_data['email']
        user.full_name = user_data['full_name']
        user.role_id = role.id
        user.set_password(user_data['password'])  # Hash password
        user.save()
```

---

**Created**: November 13, 2025  
**Author**: CSR ScrumMasters Team

