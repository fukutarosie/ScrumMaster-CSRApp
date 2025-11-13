"""
Database Seeding Script for Test Data
Seeds roles and user accounts from JSON files into Supabase
"""

import json
import os
import sys
import io

# Fix Windows console encoding issue
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.entity.role import Role
from src.entity.user import User


def seed_roles():
    """Seed roles from roles.json"""
    print("\n" + "="*60)
    print("🎭 SEEDING ROLES")
    print("="*60)
    
    current_dir = os.path.dirname(__file__)
    roles_path = os.path.join(current_dir, 'test_data', 'roles.json')
    
    with open(roles_path, 'r') as f:
        roles = json.load(f)
    
    created_count = 0
    skipped_count = 0
    
    for role_data in roles:
        # Check if role already exists
        existing_role = Role.find_by_name(role_data['role_name'])
        
        if existing_role:
            print(f"   ⚠️  {role_data['role_name']} - Already exists, skipping")
            skipped_count += 1
            continue
        
        # Create new role
        role = Role()
        role.role_name = role_data['role_name']
        role.role_code = role_data['role_code']
        role.description = role_data['description']
        role.dashboard_route = role_data['dashboard_route']
        
        if role.save():
            print(f"   ✅ {role_data['role_name']} ({role_data['role_code']})")
            created_count += 1
        else:
            print(f"   ❌ {role_data['role_name']} - Failed to create")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Created: {created_count}")
    print(f"   ⚠️  Skipped: {skipped_count}")
    print(f"   📋 Total: {len(roles)}")


def seed_users():
    """Seed user accounts from user_accounts.json"""
    print("\n" + "="*60)
    print("👥 SEEDING USER ACCOUNTS")
    print("="*60)
    
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'test_data', 'user_accounts.json')
    
    with open(users_path, 'r') as f:
        users = json.load(f)
    
    created_count = 0
    skipped_count = 0
    error_count = 0
    
    # Get role mappings
    role_cache = {}
    print("\n🔍 Loading roles...")
    for role_name in ['User Admin', 'PIN', 'CSR Rep', 'Platform Management']:
        role = Role.find_by_name(role_name)
        if role:
            role_cache[role_name] = role
            print(f"   ✅ {role_name} (ID: {role.id})")
        else:
            print(f"   ❌ {role_name} - Not found!")
    
    print(f"\n📝 Creating {len(users)} users...")
    
    for i, user_data in enumerate(users, 1):
        # Check if user already exists
        existing_user = User.find_by_username(user_data['username'])
        if existing_user:
            print(f"   [{i:3d}/100] ⚠️  {user_data['username']} - Already exists")
            skipped_count += 1
            continue
        
        # Check if email already exists
        existing_email = User.find_by_email(user_data['email'])
        if existing_email:
            print(f"   [{i:3d}/100] ⚠️  {user_data['email']} - Email already exists")
            skipped_count += 1
            continue
        
        # Get role ID
        role = role_cache.get(user_data['role_name'])
        if not role:
            print(f"   [{i:3d}/100] ❌ {user_data['username']} - Role '{user_data['role_name']}' not found")
            error_count += 1
            continue
        
        # Create new user
        user = User()
        user.username = user_data['username']
        user.email = user_data['email']
        user.full_name = user_data['full_name']
        user.role_id = role.id
        user.set_password(user_data['password'])  # Hash the password
        user.is_active = True
        
        if user.save():
            print(f"   [{i:3d}/100] ✅ {user_data['username']} ({user_data['role_name']})")
            created_count += 1
        else:
            print(f"   [{i:3d}/100] ❌ {user_data['username']} - Failed to save")
            error_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Created: {created_count}")
    print(f"   ⚠️  Skipped: {skipped_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📋 Total: {len(users)}")


def delete_test_users():
    """Delete all test users from user_accounts.json"""
    print("\n" + "="*60)
    print("🗑️  DELETING TEST USER ACCOUNTS")
    print("="*60)
    
    current_dir = os.path.dirname(__file__)
    users_path = os.path.join(current_dir, 'test_data', 'user_accounts.json')
    
    with open(users_path, 'r') as f:
        users = json.load(f)
    
    deleted_count = 0
    not_found_count = 0
    
    for i, user_data in enumerate(users, 1):
        user = User.find_by_username(user_data['username'])
        if user:
            if user.delete():
                print(f"   [{i:3d}/100] ✅ Deleted {user_data['username']}")
                deleted_count += 1
            else:
                print(f"   [{i:3d}/100] ❌ Failed to delete {user_data['username']}")
        else:
            not_found_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Deleted: {deleted_count}")
    print(f"   ⚠️  Not Found: {not_found_count}")
    print(f"   📋 Total: {len(users)}")


def delete_test_roles():
    """Delete test roles (WARNING: Use with caution!)"""
    print("\n" + "="*60)
    print("🗑️  DELETING TEST ROLES")
    print("="*60)
    print("⚠️  WARNING: This will delete roles and may break existing data!")
    
    confirm = input("\nType 'DELETE' to confirm: ")
    if confirm != "DELETE":
        print("❌ Cancelled")
        return
    
    current_dir = os.path.dirname(__file__)
    roles_path = os.path.join(current_dir, 'test_data', 'roles.json')
    
    with open(roles_path, 'r') as f:
        roles = json.load(f)
    
    deleted_count = 0
    not_found_count = 0
    
    for role_data in roles:
        role = Role.find_by_name(role_data['role_name'])
        if role:
            if role.delete():
                print(f"   ✅ Deleted {role_data['role_name']}")
                deleted_count += 1
            else:
                print(f"   ❌ Failed to delete {role_data['role_name']}")
        else:
            print(f"   ⚠️  {role_data['role_name']} - Not found")
            not_found_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Deleted: {deleted_count}")
    print(f"   ⚠️  Not Found: {not_found_count}")
    print(f"   📋 Total: {len(roles)}")


def seed_all():
    """Seed both roles and users"""
    print("\n" + "="*60)
    print("🚀 SEEDING ALL TEST DATA")
    print("="*60)
    
    seed_roles()
    seed_users()
    
    print("\n" + "="*60)
    print("✅ SEEDING COMPLETE")
    print("="*60)


def delete_all():
    """Delete all test data"""
    print("\n" + "="*60)
    print("🗑️  DELETING ALL TEST DATA")
    print("="*60)
    print("⚠️  WARNING: This will delete all test users!")
    
    confirm = input("\nType 'DELETE' to confirm: ")
    if confirm != "DELETE":
        print("❌ Cancelled")
        return
    
    delete_test_users()
    # Uncomment if you want to delete roles too
    # delete_test_roles()
    
    print("\n" + "="*60)
    print("✅ DELETION COMPLETE")
    print("="*60)


def main():
    """Main menu for seeding/deleting test data"""
    print("\n" + "="*60)
    print("🌱 CSR TEST DATA SEEDING UTILITY")
    print("="*60)
    print("\nOptions:")
    print("  1. Seed all (roles + users)")
    print("  2. Seed roles only")
    print("  3. Seed users only")
    print("  4. Delete all test users")
    print("  5. Delete test roles (dangerous!)")
    print("  6. Exit")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        seed_all()
    elif choice == "2":
        seed_roles()
    elif choice == "3":
        seed_users()
    elif choice == "4":
        delete_test_users()
    elif choice == "5":
        delete_test_roles()
    elif choice == "6":
        print("👋 Goodbye!")
        return
    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

