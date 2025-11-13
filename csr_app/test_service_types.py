"""
Test script to check service_types table and identify the issue
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from entity.supabase_config import get_supabase, execute_with_retry
from entity.service_category import ServiceCategory

def test_table_structure():
    """Test if service_types table exists and check its structure"""
    print("\n=== Testing service_types table ===\n")
    
    supabase = get_supabase()
    
    # Test 1: Check if table exists and can be queried
    print("Test 1: Checking if service_types table exists...")
    try:
        result = execute_with_retry(
            lambda: supabase.table('service_types').select('*').limit(1).execute()
        )
        print(f"✓ Table exists! Found {len(result.data)} rows")
        if result.data:
            print(f"  Sample row: {result.data[0]}")
    except Exception as e:
        print(f"✗ Error accessing table: {str(e)}")
        return False
    
    # Test 2: Try to insert a test record
    print("\nTest 2: Trying to insert a test service type...")
    try:
        test_data = {'service_name': 'Test Service Type ' + str(os.urandom(4).hex())}
        result = execute_with_retry(
            lambda: supabase.table('service_types').insert(test_data).execute()
        )
        print(f"✓ Insert successful! ID: {result.data[0]['id']}")
        
        # Clean up test record
        test_id = result.data[0]['id']
        execute_with_retry(
            lambda: supabase.table('service_types').delete().eq('id', test_id).execute()
        )
        print(f"✓ Test record cleaned up")
    except Exception as e:
        print(f"✗ Insert failed: {str(e)}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        print(f"  Traceback:\n{traceback.format_exc()}")
        return False
    
    # Test 3: Test ServiceCategory entity
    print("\nTest 3: Testing ServiceCategory entity...")
    try:
        category = ServiceCategory()
        category.service_name = 'Test Category ' + str(os.urandom(4).hex())
        category.save()
        print(f"✓ ServiceCategory.save() successful! ID: {category.id}")
        
        # Clean up
        category.delete()
        print(f"✓ Test category cleaned up")
    except Exception as e:
        print(f"✗ ServiceCategory test failed: {str(e)}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        print(f"  Traceback:\n{traceback.format_exc()}")
        return False
    
    print("\n=== All tests passed! ===\n")
    return True

if __name__ == '__main__':
    success = test_table_structure()
    sys.exit(0 if success else 1)
