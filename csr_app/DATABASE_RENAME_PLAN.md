# Database Table Rename Plan: Plural → Singular

## 🎯 Objective
Rename all database tables from **plural** to **singular** to align with documentation standards.

---

## 📋 Current State Analysis

### Current Table Names (Plural)
1. **`users`** → Target: **`user`**
2. **`roles`** → Target: **`role`**
3. **`requests`** → Target: **`request`**
4. **`shortlist`** → Target: **`shortlist`** ✅ (already singular)
5. **`request_status_history`** → Target: **`request_status_history`** ✅ (already singular)

### Additional Tables (Optional/Legacy)
6. **`profiles`** → Target: **`profile`** (legacy, may not be in use)
7. **`service_types`** → Target: **`service_type`** (lookup table)
8. **`user_activity_log`** → Target: **`user_activity_log`** ✅ (already singular)
9. **`csr_requests`** → Target: **`csr_request`** (may be legacy)

---

## 🔍 Code References Analysis

### Table: `users` → `user`
**Total References:** 15 occurrences in entity files

**Files to Update:**
- `src/entity/user.py` (15 occurrences)
  - Line 99: `.table('users')` - INSERT operation
  - Line 161: `.table('users')` - Check username uniqueness
  - Line 169: `.table('users')` - Check email uniqueness
  - Line 216: `.table('users')` - INSERT new user
  - Line 234: `.table('users')` - UPDATE user
  - Line 262: `.table('users')` - UPDATE password
  - Line 289: `.table('users')` - UPDATE last_login
  - Line 468: `.table('users')` - DELETE user
  - Line 491: `.table('users')` - SELECT count
  - Line 513: `.table('users')` - SELECT with roles JOIN
  - Line 537: `.table('users')` - SELECT by username
  - Line 641: `.table('users')` - SELECT all with roles JOIN
  - Line 666: `.table('users')` - SELECT by email
  - Line 682: `.table('users')` - UPDATE is_active

- `src/entity/request.py` (1 occurrence)
  - Line 170: `.table('users')` - Validate pin_user_id

**Foreign Key References in Other Tables:**
- `requests.pin_user_id` → references `users(id)`
- `shortlist.csr_user_id` → references `users(id)`
- `request_status_history.changed_by` → references `users(id)`

---

### Table: `roles` → `role`
**Total References:** 10 occurrences in entity files

**Files to Update:**
- `src/entity/role.py` (10 occurrences)
  - Line 86: `.table('roles')` - Initial validation query
  - Line 137: `.table('roles')` - Check role_name uniqueness
  - Line 145: `.table('roles')` - Check role_code uniqueness
  - Line 191: `.table('roles')` - INSERT new role
  - Line 206: `.table('roles')` - UPDATE role
  - Line 233: `.table('roles')` - DELETE role
  - Line 284: `.table('roles')` - Find by id
  - Line 367: `.table('roles')` - Find by role_name
  - Line 390: `.table('roles')` - Find by role_code
  - Line 410: `.table('roles')` - SELECT all roles

**JOIN References:**
- `src/entity/user.py`:
  - Line 513: `.select('*, roles(*)')` - JOIN syntax
  - Line 641: `.select('*, roles(*)')` - JOIN syntax

**Foreign Key References in Other Tables:**
- `users.role_id` → references `roles(id)`

---

### Table: `requests` → `request`
**Total References:** 18 occurrences in entity files

**Files to Update:**
- `src/entity/request.py` (18 occurrences)
  - Line 92: `.table('requests')` - Initial validation
  - Line 255: `.table('requests')` - INSERT new request
  - Line 280: `.table('requests')` - UPDATE request
  - Line 308: `.table('requests')` - DELETE request
  - Line 338: `.table('requests')` - Suspend request
  - Line 380: `.table('requests')` - Fulfill request
  - Line 414: `.table('requests')` - Archive request
  - Line 438: `.table('requests')` - Increment view_count
  - Line 455: `.table('requests')` - Increment shortlist_count
  - Line 472: `.table('requests')` - Decrement shortlist_count
  - Line 556: `.table('requests')` - SELECT with filters
  - Line 580: `.table('requests')` - Find by id
  - Line 603: `.table('requests')` - By PIN user
  - Line 633: `.table('requests')` - SELECT active requests
  - Line 664: `.table('requests')` - (possible duplicate check)

- `src/entity/shortlist.py` (1 occurrence)
  - Line 169: `.table('requests')` - Validate request_id

**JOIN References:**
- `src/entity/shortlist.py`:
  - Line 441: `.select('*, requests(*)')` - JOIN syntax
  - Line 507: `.select('*, requests(*)')` - JOIN syntax

**Foreign Key References in Other Tables:**
- `shortlist.request_id` → references `requests(id)`
- `request_status_history.request_id` → references `requests(id)`

---

### Table: `shortlist` ✅ (No Change Needed)
**Status:** Already singular
**Total References:** 11 occurrences in `src/entity/shortlist.py`

---

### Table: `request_status_history` ✅ (No Change Needed)
**Status:** Already singular
**Total References:** 2 occurrences in `src/entity/request.py`

---

### Table: `service_types` → `service_type`
**Total References:** 2 occurrences

**Files to Update:**
- `src/entity/request.py` (2 occurrences)
  - Line 196: `.table('service_types')` - Validate service_type
  - Line 664: `.table('service_types')` - Get all service types

---

### Table: `user_activity_log` ✅ (No Change Needed)
**Status:** Already singular
**Total References:** 1 occurrence in `src/entity/user.py` (Line 404)

---

### Legacy/Optional Tables
The following tables appear in backup files but may not be actively used:
- `profiles` (in `profile.py` and backups)
- `csr_requests` (in `csr_request.py`)
- `request_categories` (in request_backup.py)

**Recommendation:** Verify if these tables exist in Supabase before renaming.

---

## 🚨 Critical Considerations

### 1. **Foreign Key Constraints**
When renaming tables, PostgreSQL foreign key constraints must be updated. The constraints reference the old table names.

**Example:**
```sql
-- Old constraint
ALTER TABLE requests DROP CONSTRAINT requests_pin_user_id_fkey;
-- New constraint
ALTER TABLE request ADD CONSTRAINT request_pin_user_id_fkey 
    FOREIGN KEY (pin_user_id) REFERENCES user(id);
```

### 2. **JOIN Syntax**
Supabase uses special JOIN syntax with table names:
```python
# Before
.select('*, roles(*)')  # Joins with 'roles' table

# After
.select('*, role(*)')   # Must join with 'role' table
```

### 3. **Indexes**
All indexes on the tables must be recreated or renamed:
```sql
-- Check existing indexes
SELECT indexname FROM pg_indexes WHERE tablename = 'users';

-- Indexes are automatically renamed by PostgreSQL when using ALTER TABLE RENAME
```

### 4. **Triggers**
Any triggers on these tables must be checked and updated if they reference table names.

### 5. **Row Level Security (RLS) Policies**
Supabase may have RLS policies attached to these tables that need to be updated.

---

## 📝 Migration Strategy

### Option A: **SQL RENAME (Recommended)**
PostgreSQL's `ALTER TABLE RENAME` command preserves:
- ✅ Data
- ✅ Constraints (auto-renamed)
- ✅ Indexes (auto-renamed)
- ✅ Triggers (auto-renamed)
- ❌ Foreign key references (must be manually updated)

### Option B: **CREATE NEW + MIGRATE**
Create new singular tables and migrate data:
- ❌ More complex
- ❌ Requires downtime
- ✅ Safer for rollback

**Recommendation:** Use **Option A** with a rollback plan.

---

## 🔧 Migration SQL Script

### Phase 1: Backup Current State
```sql
-- Create backup schema
CREATE SCHEMA IF NOT EXISTS backup_schema;

-- Backup tables
CREATE TABLE backup_schema.users AS SELECT * FROM users;
CREATE TABLE backup_schema.roles AS SELECT * FROM roles;
CREATE TABLE backup_schema.requests AS SELECT * FROM requests;
CREATE TABLE backup_schema.service_types AS SELECT * FROM service_types;
```

### Phase 2: Rename Tables
```sql
-- IMPORTANT: Rename in order to avoid FK constraint conflicts

-- Step 1: Rename independent table (no dependencies)
ALTER TABLE roles RENAME TO role;

-- Step 2: Rename user table (depends on role)
ALTER TABLE users RENAME TO user;

-- Step 3: Rename requests (depends on user)
ALTER TABLE requests RENAME TO request;

-- Step 4: Update shortlist foreign key references (already singular)
-- No changes needed for shortlist table itself

-- Step 5: Rename service_types (independent)
ALTER TABLE service_types RENAME TO service_type;
```

### Phase 3: Update Foreign Key Constraints
```sql
-- Update FK constraint names to match new table names
-- PostgreSQL automatically renames most constraints, but verify:

-- Check current constraints
SELECT conname, conrelid::regclass, confrelid::regclass
FROM pg_constraint
WHERE contype = 'f';

-- If needed, manually rename constraints:
-- ALTER TABLE shortlist 
--   RENAME CONSTRAINT shortlist_csr_user_id_fkey 
--   TO shortlist_csr_user_id_fkey;  -- Usually auto-renamed
```

### Phase 4: Verify Integrity
```sql
-- Check all foreign keys are intact
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
ORDER BY tc.table_name;

-- Verify row counts
SELECT 'user' as table_name, COUNT(*) FROM "user"
UNION ALL
SELECT 'role', COUNT(*) FROM role
UNION ALL
SELECT 'request', COUNT(*) FROM request
UNION ALL
SELECT 'shortlist', COUNT(*) FROM shortlist;
```

---

## 🔄 Rollback Plan

If issues occur, rollback using:
```sql
-- Rollback renames (reverse order)
ALTER TABLE service_type RENAME TO service_types;
ALTER TABLE request RENAME TO requests;
ALTER TABLE "user" RENAME TO users;
ALTER TABLE role RENAME TO roles;

-- Restore from backup if data is corrupted
-- DROP TABLE users;
-- CREATE TABLE users AS SELECT * FROM backup_schema.users;
-- (Repeat for other tables)
```

---

## 💻 Code Update Summary

### Files Requiring Updates (44 occurrences total)

#### 1. `src/entity/user.py` (15 changes)
```python
# Before
supabase.table('users')

# After
supabase.table('user')
```

**AND** (2 changes for JOIN syntax)
```python
# Before
.select('*, roles(*)')

# After
.select('*, role(*)')
```

#### 2. `src/entity/role.py` (10 changes)
```python
# Before
supabase.table('roles')

# After
supabase.table('role')
```

#### 3. `src/entity/request.py` (20 changes)
```python
# Before
supabase.table('requests')
supabase.table('users')
supabase.table('service_types')

# After
supabase.table('request')
supabase.table('user')
supabase.table('service_type')
```

#### 4. `src/entity/shortlist.py` (3 changes)
```python
# Before
supabase.table('requests')
.select('*, requests(*)')

# After
supabase.table('request')
.select('*, request(*)')
```

---

## ✅ Testing Checklist

After migration, test the following:

### Backend Tests
- [ ] User login (validates `user` + `role` tables)
- [ ] User registration (INSERT into `user` table)
- [ ] Create PIN request (INSERT into `request` table)
- [ ] View requests (SELECT from `request` table)
- [ ] Add to shortlist (INSERT into `shortlist`, references `request` + `user`)
- [ ] Mark request as fulfilled (UPDATE `request`, INSERT into `request_status_history`)
- [ ] User admin CRUD (all operations on `user` and `role`)

### Frontend Tests
- [ ] Admin dashboard loads
- [ ] PIN dashboard loads
- [ ] CSR dashboard loads
- [ ] Create new request form works
- [ ] Shortlist page displays correctly
- [ ] History page displays completed matches

---

## 📊 Impact Assessment

### High Impact (Must Test Thoroughly)
1. **User authentication** - uses `user` + `role` tables
2. **Request CRUD** - core functionality
3. **Shortlist operations** - heavily used feature

### Medium Impact
4. **Service type filtering** - uses `service_type` lookup table

### Low Impact
5. **Activity logging** - `user_activity_log` already singular
6. **Status history** - `request_status_history` already singular

---

## ⏱️ Estimated Timeline

1. **SQL Migration** (5 minutes)
   - Backup: 1 min
   - Rename tables: 1 min
   - Verify constraints: 2 min
   - Test queries: 1 min

2. **Code Updates** (20 minutes)
   - Update entity files: 15 min
   - Test imports: 5 min

3. **Testing** (30 minutes)
   - Backend testing: 15 min
   - Frontend testing: 15 min

**Total:** ~1 hour (with rollback buffer)

---

## 🎯 Execution Plan

### Step 1: Database Migration (Do This First)
1. Open Supabase SQL Editor
2. Run Phase 1 (Backup) SQL
3. Run Phase 2 (Rename) SQL
4. Run Phase 4 (Verify) SQL
5. Take a screenshot of verification results

### Step 2: Code Updates (Do This Second)
1. Update `src/entity/user.py` (17 changes)
2. Update `src/entity/role.py` (10 changes)
3. Update `src/entity/request.py` (20 changes)
4. Update `src/entity/shortlist.py` (3 changes)
5. Search for any remaining references: `grep -r "table('users')" src/`

### Step 3: Testing (Do This Third)
1. Restart backend: `python app.py`
2. Restart frontend: `npm run dev`
3. Test all user flows (see checklist above)

### Step 4: Commit Changes
1. `git add .`
2. `git commit -m "Refactor: Rename database tables from plural to singular"`
3. `git push origin main`

---

## 🚨 BEFORE YOU START

### Pre-Migration Checklist
- [ ] Confirm no active users on the system
- [ ] Have Supabase dashboard open
- [ ] Have rollback SQL ready
- [ ] Have backup of entire codebase (`git status` clean)
- [ ] Confirm you have Supabase admin access
- [ ] Verify all table names exist in Supabase:
  ```sql
  SELECT tablename FROM pg_tables 
  WHERE schemaname = 'public' 
  ORDER BY tablename;
  ```

---

## 📞 Support

If any step fails:
1. **DO NOT PANIC** - Rollback is available
2. Run rollback SQL immediately
3. Check error messages carefully
4. Verify your Supabase permissions

---

**Ready to proceed?** Let me know, and I'll guide you through each step! 🚀

