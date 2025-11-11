# Table Rename Summary: Confirmed Schema

## ✅ Confirmed Tables in Your Supabase Database

Based on the verification script, here are the tables that **actually exist** in your Supabase instance:

### Tables That Need Renaming (Plural → Singular)

| Current Name (Plural) | New Name (Singular) | Status | Code References |
|-----------------------|---------------------|--------|----------------|
| **`users`** | **`user`** | ⚠️ MUST RENAME | 17 occurrences |
| **`roles`** | **`role`** | ⚠️ MUST RENAME | 12 occurrences |
| **`requests`** | **`request`** | ⚠️ MUST RENAME | 21 occurrences |
| **`service_types`** | **`service_type`** | ⚠️ MUST RENAME | 2 occurrences |

### Tables Already Singular (No Change Needed)

| Table Name | Status | Purpose |
|------------|--------|---------|
| **`shortlist`** | ✅ ALREADY SINGULAR | CSR shortlist/assignments |
| **`request_status_history`** | ✅ ALREADY SINGULAR | Request audit log |

### Tables Not Found

| Table Name | Status | Notes |
|------------|--------|-------|
| **`user_activity_log`** | ❌ NOT FOUND | Referenced in code but doesn't exist in DB |

---

## 📊 Impact Assessment

### Total Code Changes Required: **52 occurrences**

1. **`users` → `user`**: 17 changes
   - `src/entity/user.py`: 15 changes
   - `src/entity/request.py`: 1 change
   - JOIN syntax `.select('*, roles(*)')` → `.select('*, role(*)')`: 2 changes

2. **`roles` → `role`**: 12 changes
   - `src/entity/role.py`: 10 changes
   - `src/entity/user.py` (JOIN syntax): 2 changes

3. **`requests` → `request`**: 21 changes
   - `src/entity/request.py`: 18 changes
   - `src/entity/shortlist.py`: 1 change
   - JOIN syntax `.select('*, requests(*)')` → `.select('*, request(*)')`: 2 changes

4. **`service_types` → `service_type`**: 2 changes
   - `src/entity/request.py`: 2 changes

---

## 🗂️ Foreign Key Relationships (Must Be Preserved)

```
role (id) ←─────┐
                │
                │ 1:N
                │
user (id) ──────┴──────┬───────────────────┐
  ↑                    │                   │
  │ 1:N                │ 1:N               │
  │                    ↓                   ↓
  │              request (id)          shortlist
  │                    ↑                   │
  │                    │ N:1               │
  │                    └───────────────────┘
  │
  │ 1:N (optional)
  │
request_status_history
```

**Key Constraints:**
- `user.role_id` → `role.id`
- `request.pin_user_id` → `user.id`
- `shortlist.csr_user_id` → `user.id`
- `shortlist.request_id` → `request.id`
- `request_status_history.request_id` → `request.id`
- `request_status_history.changed_by` → `user.id` (optional)

---

## 🚀 Step-by-Step Execution Plan

### Phase 1: Database Rename (5 minutes)

**Run this SQL in Supabase SQL Editor:**

```sql
-- ====================================
-- PHASE 1: BACKUP (SAFETY FIRST!)
-- ====================================
CREATE SCHEMA IF NOT EXISTS backup_schema;

CREATE TABLE backup_schema.users AS SELECT * FROM users;
CREATE TABLE backup_schema.roles AS SELECT * FROM roles;
CREATE TABLE backup_schema.requests AS SELECT * FROM requests;
CREATE TABLE backup_schema.service_types AS SELECT * FROM service_types;

-- ====================================
-- PHASE 2: RENAME TABLES (ORDER MATTERS!)
-- ====================================

-- Step 1: Rename independent table (no FK dependencies)
ALTER TABLE service_types RENAME TO service_type;

-- Step 2: Rename roles (no FK dependencies on other tables)
ALTER TABLE roles RENAME TO role;

-- Step 3: Rename users (depends on role)
ALTER TABLE users RENAME TO "user";  -- Note: "user" is a reserved word, so we quote it

-- Step 4: Rename requests (depends on user)
ALTER TABLE requests RENAME TO request;

-- Note: shortlist and request_status_history are already singular!

-- ====================================
-- PHASE 3: VERIFY INTEGRITY
-- ====================================

-- Check all tables exist
SELECT tablename FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN ('user', 'role', 'request', 'shortlist', 'request_status_history', 'service_type')
ORDER BY tablename;

-- Check foreign keys are intact
SELECT 
    tc.table_name, 
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name;

-- Verify row counts
SELECT 'user' as table_name, COUNT(*) as row_count FROM "user"
UNION ALL
SELECT 'role', COUNT(*) FROM role
UNION ALL
SELECT 'request', COUNT(*) FROM request
UNION ALL
SELECT 'shortlist', COUNT(*) FROM shortlist
UNION ALL
SELECT 'request_status_history', COUNT(*) FROM request_status_history
UNION ALL
SELECT 'service_type', COUNT(*) FROM service_type;
```

### Phase 2: Code Updates (20 minutes)

I will use automated scripts to update all code references. The files to update are:

1. `src/entity/user.py` (17 changes)
2. `src/entity/role.py` (10 changes)
3. `src/entity/request.py` (21 changes)
4. `src/entity/shortlist.py` (3 changes)

**Note:** I'll use `replace_all=True` for each table name to ensure all occurrences are updated.

### Phase 3: Testing (15 minutes)

After updates, test these critical flows:
- [ ] User login
- [ ] Create PIN request
- [ ] View requests
- [ ] Add to shortlist
- [ ] User admin dashboard

---

## 🔄 Rollback Plan (If Needed)

If anything goes wrong, run this SQL:

```sql
-- ROLLBACK: Rename tables back to plural
ALTER TABLE service_type RENAME TO service_types;
ALTER TABLE request RENAME TO requests;
ALTER TABLE "user" RENAME TO users;
ALTER TABLE role RENAME TO roles;

-- If data is corrupted, restore from backup:
-- DROP TABLE users CASCADE;
-- CREATE TABLE users AS SELECT * FROM backup_schema.users;
-- (Repeat for other tables and recreate foreign keys)
```

---

## ⚠️ CRITICAL NOTES

### 1. Reserved Word: `user`
PostgreSQL treats `user` as a **reserved word**, so we must quote it in SQL:
```sql
ALTER TABLE users RENAME TO "user";
```

However, in Python code with Supabase, we can use it **without quotes**:
```python
supabase.table('user')  # ✅ Works fine
```

### 2. Order of Renaming Matters
We must rename in this specific order to avoid breaking foreign key constraints:
1. `service_types` (no dependencies)
2. `roles` (no dependencies)
3. `users` (depends on `roles`)
4. `requests` (depends on `users`)

### 3. JOIN Syntax Changes
PostgreSQL automatically updates foreign key constraint names when you rename tables, **but** Supabase's JOIN syntax uses the table name explicitly:

```python
# Before
.select('*, roles(*)')    # Joins with 'roles' table
.select('*, requests(*)')  # Joins with 'requests' table

# After
.select('*, role(*)')     # Must join with 'role' table
.select('*, request(*)')   # Must join with 'request' table
```

---

## 📝 Quick Start Checklist

Ready to proceed? Follow these steps:

- [ ] **Step 1:** Review this document and `DATABASE_RENAME_PLAN.md`
- [ ] **Step 2:** Ensure no active users on the system
- [ ] **Step 3:** Take a full Supabase backup (optional but recommended)
- [ ] **Step 4:** Run Phase 1 SQL (Backup + Rename) in Supabase SQL Editor
- [ ] **Step 5:** Verify Phase 3 SQL queries return correct results
- [ ] **Step 6:** Let me know, and I'll update all Python code automatically
- [ ] **Step 7:** Restart backend and frontend
- [ ] **Step 8:** Test all critical user flows
- [ ] **Step 9:** Commit changes to Git
- [ ] **Step 10:** Celebrate! 🎉

---

## 🎯 Ready When You Are!

Once you've reviewed this plan, let me know if you'd like to proceed. I can:

1. ✅ Guide you through the SQL migration step-by-step
2. ✅ Automatically update all 52 code occurrences
3. ✅ Test the application after changes
4. ✅ Create detailed documentation of what was changed
5. ✅ Help you rollback if needed

**Your database will be in a clean, singular-named state aligned with your documentation!** 🚀

---

## 📞 Questions Before We Start?

- Do you want me to show you the exact SQL commands first?
- Do you want to review the code changes before I apply them?
- Do you have any concerns about the migration?

Let me know, and I'll guide you through each step! 💪

