"""
Quick Login Debug Script
Tests authentication with your real credentials
"""

import sys
import os
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(__file__))

from src.entity.user import User
from src.entity.role import Role

print("\n" + "="*60)
print("LOGIN DEBUG TEST")
print("="*60)

# Test credentials
test_accounts = [
    ("admin1", "password123", "User Admin"),
    ("csr_rep1", "password123", "CSR Rep"),
    ("pin_user1", "password123", "PIN"),
    ("platform_mgr1", "password123", "Platform Management"),
]

print("\nTesting authentication for all accounts...\n")

for username, password, role_name in test_accounts:
    print(f"Testing: {username} / {role_name}")
    
    # Step 1: Check if user exists
    user = User.find_by_username(username)
    if not user:
        print(f"   ❌ User '{username}' NOT FOUND in database")
        continue
    else:
        print(f"   ✅ User found - ID: {user.id}")
    
    # Step 2: Check role
    print(f"   - User role_id: {user.role_id}")
    if user.roles:
        print(f"   - User role name: {user.roles.get('role_name', 'N/A')}")
    
    # Step 3: Verify password
    password_match = user.verify_password(password)
    if password_match:
        print(f"   ✅ Password matches")
    else:
        print(f"   ❌ Password DOES NOT match")
        print(f"   - Stored password hash: {user.password[:50]}...")
    
    # Step 4: Check if active
    if user.is_active:
        print(f"   ✅ User is active")
    else:
        print(f"   ❌ User is INACTIVE")
    
    # Step 5: Try full authentication
    authenticated_user = User.authenticate(username, password, role_name)
    if authenticated_user:
        print(f"   ✅ AUTHENTICATION SUCCESSFUL")
    else:
        print(f"   ❌ AUTHENTICATION FAILED")
        
        # Check role mismatch
        role = Role.find_by_name(role_name)
        if role:
            print(f"   - Expected role_id: {role.id}, User's role_id: {user.role_id}")
            if role.id != user.role_id:
                print(f"   WARNING: ROLE MISMATCH!")
        else:
            print(f"   ❌ Role '{role_name}' NOT FOUND in database")
    
    print()

print("="*60)
print("CHECKING ROLES IN DATABASE")
print("="*60 + "\n")

roles = Role.all()
if roles:
    print(f"Found {len(roles)} roles:")
    for role in roles:
        print(f"   - ID: {role.id}, Name: '{role.role_name}', Code: {role.role_code}")
else:
    print("   ❌ NO ROLES FOUND in database!")

print("\n" + "="*60)
print("Debug complete!")
print("="*60)

