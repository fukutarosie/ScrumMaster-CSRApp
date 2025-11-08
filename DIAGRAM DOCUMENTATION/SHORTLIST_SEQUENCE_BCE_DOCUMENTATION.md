# Shortlist Feature - Sequence & BCE Diagram Documentation

## 📋 Table of Contents
1. [BCE Architecture Overview](#bce-architecture-overview)
2. [Component Mapping](#component-mapping)
3. [Sequence Diagram: Add to Shortlist](#sequence-diagram-add-to-shortlist)
4. [Sequence Diagram: Remove from Shortlist](#sequence-diagram-remove-from-shortlist)
5. [Sequence Diagram: View Shortlist](#sequence-diagram-view-shortlist)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)

---

## 🏗️ BCE Architecture Overview

### Boundary Layer (UI/Presentation)
**Location**: `src/app/csr/page.js` and `src/app/csr/shortlist/page.js`

**Responsibilities**:
- User interface rendering
- User input handling
- HTTP requests to backend
- State management (React)
- Visual feedback (stars, badges, alerts)

**Technologies**: Next.js (React), Tailwind CSS, Axios

---

### Control Layer (Business Logic)
**Location**: `src/controller/shortlist/`

**Files**:
- `add_to_shortlist_controller.py` - Add request to shortlist logic
- `remove_from_shortlist_controller.py` - Remove request from shortlist logic
- `get_shortlist_controller.py` - Retrieve user's shortlist logic
- `update_shortlist_status_controller.py` - Update shortlist status/notes logic

**Responsibilities**:
- Token validation and authentication
- Business rule enforcement
- Request validation
- Data transformation
- Error handling
- Calling entity layer methods

**Technologies**: Python, Flask

---

### Entity Layer (Data Access)
**Location**: `src/entity/shortlist.py`

**Key Methods**:
- `add_to_shortlist(csr_user_id, request_id, notes)` - Insert shortlist record
- `remove_from_shortlist(shortlist_id, csr_user_id)` - Delete shortlist record
- `search_shortlist(csr_user_id, status, limit, offset)` - Query shortlist items
- `update_shortlist_status(shortlist_id, csr_user_id, status, notes, hours)` - Update record

**Responsibilities**:
- Direct database operations (CRUD)
- SQL query construction
- Data validation
- Supabase client interaction
- Relationship management (joins)

**Technologies**: Python, Supabase (PostgreSQL)

---

## 🗺️ Component Mapping

### Frontend Components (Boundary)
```
src/app/csr/page.js                    ← Browse & shortlist requests
src/app/csr/shortlist/page.js          ← Manage shortlist
src/app/components/RequestCard.js       ← Display individual request card
src/app/components/RequestCardGrid.js   ← Grid layout for cards
src/app/components/Header.js            ← Page header
src/app/components/Alert.js             ← Success/error messages
```

### Backend Boundary (HTTP Layer)
```
src/controller/shortlist/boundary/
├── add_to_shortlist_boundary.py          ← POST /api/shortlist
├── remove_from_shortlist_boundary.py     ← DELETE /api/shortlist/{id}
├── get_shortlist_boundary.py             ← GET /api/shortlist
└── update_shortlist_status_boundary.py   ← PATCH /api/shortlist/{id}/status
```

### Backend Control (Business Logic)
```
src/controller/shortlist/
├── add_to_shortlist_controller.py         ← Validate & add logic
├── remove_from_shortlist_controller.py    ← Validate & remove logic
├── get_shortlist_controller.py            ← Fetch & format logic
└── update_shortlist_status_controller.py  ← Update & validate logic
```

### Backend Entity (Database)
```
src/entity/
├── shortlist.py     ← Shortlist database operations
├── request.py       ← Request database operations
└── user.py          ← User authentication & database operations
```

---

## 📊 Sequence Diagram: Add to Shortlist

### Actors & Components
- **CSR Rep** (User)
- **Browser** (Frontend/Boundary)
- **Add Shortlist Boundary** (`add_to_shortlist_boundary.py`)
- **Add Shortlist Controller** (`add_to_shortlist_controller.py`)
- **Shortlist Entity** (`shortlist.py`)
- **Database** (Supabase PostgreSQL)

### Sequence Flow

```
CSR Rep                    Browser                Add Boundary          Add Controller         Shortlist Entity      Database
   |                          |                         |                       |                      |                |
   |  1. Click star (☆)       |                         |                       |                      |                |
   |------------------------->|                         |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 2. handleToggleShortlist(requestId)            |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 3. POST /api/shortlist  |                       |                      |                |
   |                          |    {request_id: 13}     |                       |                      |                |
   |                          |    Authorization: JWT   |                       |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          |                         | 4. add_shortlist()    |                      |                |
   |                          |                         |    (auth_token, data) |                      |                |
   |                          |                         |---------------------->|                      |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 5. verify_session_token()            |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |<---------------------|                |
   |                          |                         |                       | user_data {id: 42}   |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 6. validate_required_fields()        |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |<---------------------|                |
   |                          |                         |                       | is_valid: true       |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 7. add_to_shortlist()|                |
   |                          |                         |                       |    (csr_user_id: 42, |                |
   |                          |                         |                       |     request_id: 13)  |                |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       |                      | 8. INSERT INTO shortlist
   |                          |                         |                       |                      | (csr_user_id, request_id, status)
   |                          |                         |                       |                      | VALUES (42, 13, 'SHORTLISTED')
   |                          |                         |                       |                      |--------------->|
   |                          |                         |                       |                      |<---------------|
   |                          |                         |                       |                      | {id: 9, ...}   |
   |                          |                         |                       |<---------------------|                |
   |                          |                         |                       | shortlist_entry      |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 9. increment_shortlist_count()       |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |                      | UPDATE requests
   |                          |                         |                       |                      | SET shortlist_count++
   |                          |                         |                       |                      |--------------->|
   |                          |                         |                       |<---------------------|                |
   |                          |                         |<----------------------|                      |                |
   |                          |                         | {success: true,       |                      |                |
   |                          |                         |  message: "Added",    |                      |                |
   |                          |                         |  data: {...}}         |                      |                |
   |                          |<------------------------|                       |                      |                |
   |                          | 201 Created             |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 10. setShortlistedIds([...prev, 13])           |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 11. fetchShortlistedIds() (re-sync)             |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |  12. Star changes to ⭐   |                         |                       |                      |                |
   |  Purple badge appears    |                         |                       |                      |                |
   |<-------------------------|                         |                       |                      |                |
```

### Key Points
1. **Authentication**: JWT token validated before any operation
2. **Validation**: Required fields checked (request_id)
3. **Business Logic**: Controller checks if request exists and is active
4. **Database Constraint**: UNIQUE(csr_user_id, request_id) prevents duplicates
5. **Optimistic Update**: Frontend updates UI before re-fetching for better UX
6. **Analytics**: Shortlist count incremented on request for reporting

---

## 📊 Sequence Diagram: Remove from Shortlist

### Sequence Flow

```
CSR Rep                    Browser                Get Boundary          Delete Boundary        Shortlist Entity      Database
   |                          |                         |                       |                      |                |
   |  1. Click star (⭐)       |                         |                       |                      |                |
   |------------------------->|                         |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 2. handleToggleShortlist(requestId)            |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 3. GET /api/shortlist   |                       |                      |                |
   |                          |    Authorization: JWT   |                       |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          |                         | 4. get_shortlist()    |                      |                |
   |                          |                         |---------------------->|                      |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 5. search_shortlist()|                |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |                      | SELECT * FROM shortlist
   |                          |                         |                       |                      | WHERE csr_user_id=42
   |                          |                         |                       |                      | JOIN requests
   |                          |                         |                       |                      |--------------->|
   |                          |                         |                       |<---------------------|                |
   |                          |                         |<----------------------| [{id:9, request_id:13, ...}]
   |                          |<------------------------|                       |                      |                |
   |                          | [{success: true,        |                       |                      |                |
   |                          |   data: [...]}]         |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 6. Find item where request_id===13              |                      |                |
   |                          |    shortlistItem.id = 9 |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 7. DELETE /api/shortlist/9                      |                      |                |
   |                          |    Authorization: JWT   |                       |                      |                |
   |                          |--------------------------------------------------->|                      |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 8. remove_shortlist()|                |
   |                          |                         |                       |    (token, id:9)     |                |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 9. verify_session_token()            |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |<---------------------|                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 10. remove_from_shortlist()          |
   |                          |                         |                       |     (id:9, user:42)  |                |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |                      | DELETE FROM shortlist
   |                          |                         |                       |                      | WHERE id=9
   |                          |                         |                       |                      | AND csr_user_id=42
   |                          |                         |                       |                      |--------------->|
   |                          |                         |                       |<---------------------|                |
   |                          |                         |<----------------------| success: true        |                |
   |                          |<-------------------------------------------------|                      |                |
   |                          | 200 OK                  |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 11. setShortlistedIds(prev.filter(id !== 13))   |                      |                |
   |                          |                         |                       |                      |                |
   |  12. Star changes to ☆   |                         |                       |                      |                |
   |  Badge removed           |                         |                       |                      |                |
   |<-------------------------|                         |                       |                      |                |
```

### Key Points
1. **Two-Step Process**: Must fetch to get shortlist item ID, then delete
2. **Security**: DELETE requires both shortlist_id AND csr_user_id match
3. **Ownership Check**: Entity ensures user can only delete their own items
4. **State Sync**: Frontend updates local state then re-fetches for accuracy

---

## 📊 Sequence Diagram: View Shortlist (Page Load)

### Sequence Flow

```
CSR Rep                    Browser                Get Boundary          Get Controller         Shortlist Entity      Database
   |                          |                         |                       |                      |                |
   |  1. Navigate to /csr     |                         |                       |                      |                |
   |------------------------->|                         |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 2. useEffect() runs     |                       |                      |                |
   |                          |    fetchShortlistedIds()|                       |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 3. GET /api/shortlist   |                       |                      |                |
   |                          |    Authorization: JWT   |                       |                      |                |
   |                          |------------------------>|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          |                         | 4. get_shortlist()    |                      |                |
   |                          |                         |    (auth_token, params)|                     |                |
   |                          |                         |---------------------->|                      |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 5. verify_session_token()            |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |<---------------------|                |
   |                          |                         |                       | user_data {id: 42}   |                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       | 6. search_shortlist()|                |
   |                          |                         |                       |    (csr_user_id: 42, |                |
   |                          |                         |                       |     status: null,    |                |
   |                          |                         |                       |     limit: 50,       |                |
   |                          |                         |                       |     offset: 0)       |                |
   |                          |                         |                       |--------------------->|                |
   |                          |                         |                       |                      |                |
   |                          |                         |                       |                      | SELECT s.*, r.*
   |                          |                         |                       |                      | FROM shortlist s
   |                          |                         |                       |                      | JOIN requests r
   |                          |                         |                       |                      | ON s.request_id = r.id
   |                          |                         |                       |                      | WHERE s.csr_user_id = 42
   |                          |                         |                       |                      | ORDER BY s.shortlisted_at DESC
   |                          |                         |                       |                      | LIMIT 50 OFFSET 0
   |                          |                         |                       |                      |--------------->|
   |                          |                         |                       |<---------------------|                |
   |                          |                         |                       | [6 shortlist items]  |                |
   |                          |                         |<----------------------|                      |                |
   |                          |                         | {success: true,       |                      |                |
   |                          |                         |  data: [             |                      |                |
   |                          |                         |    {id: 3, request_id: 14, ...},            |                |
   |                          |                         |    {id: 4, request_id: 13, ...},            |                |
   |                          |                         |    ...               |                      |                |
   |                          |                         |  ]}                  |                      |                |
   |                          |<------------------------|                       |                      |                |
   |                          | [Array wrapper fix]     |                       |                      |                |
   |                          | response.data[0]        |                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 7. Extract request_ids  |                       |                      |                |
   |                          |    [14, 13, 10, 8, 5, 7]|                       |                      |                |
   |                          |                         |                       |                      |                |
   |                          | 8. setShortlistedIds([14,13,10,8,5,7])          |                      |                |
   |                          |                         |                       |                      |                |
   |  9. Cards with IDs       |                         |                       |                      |                |
   |  14,13,10,8,5,7 show ⭐   |                         |                       |                      |                |
   |  Other cards show ☆      |                         |                       |                      |                |
   |<-------------------------|                         |                       |                      |                |
```

### Key Points
1. **Automatic Loading**: fetchShortlistedIds() called on component mount
2. **Array Wrapper Fix**: Backend returns `[{success, data}]` instead of `{success, data}`
3. **ID Extraction**: Frontend maps to get only request_id values for quick lookup
4. **Visual Indicators**: UI uses includes() check to show stars and badges
5. **Performance**: Only IDs stored in state, full data fetched when needed

---

## 🗄️ Database Schema

### Shortlist Table
```sql
CREATE TABLE shortlist (
    id SERIAL PRIMARY KEY,
    csr_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    request_id INTEGER NOT NULL REFERENCES requests(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'SHORTLISTED',
    notes TEXT,
    volunteered_hours DECIMAL(5,2),
    completion_date TIMESTAMP,
    feedback_from_pin TEXT,
    shortlisted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    UNIQUE(csr_user_id, request_id)  -- Prevent duplicate shortlists
);

-- Indexes for performance
CREATE INDEX idx_shortlist_csr_user ON shortlist(csr_user_id);
CREATE INDEX idx_shortlist_request ON shortlist(request_id);
CREATE INDEX idx_shortlist_status ON shortlist(status);
```

### Status Values
- `SHORTLISTED` - Request saved for later
- `IN_PROGRESS` - CSR actively working on request
- `COMPLETED` - Request fulfilled
- `DECLINED` - CSR decided not to proceed

### Relationships
```
shortlist.csr_user_id → users.id (Many-to-One)
shortlist.request_id → requests.id (Many-to-One)
```

---

## 🔌 API Endpoints

### 1. GET /api/shortlist
**Purpose**: Retrieve user's shortlist items

**Authentication**: Required (JWT Bearer token)

**Query Parameters**:
- `status` (optional): Filter by status (SHORTLISTED, IN_PROGRESS, etc.)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 50)

**Response Format**:
```json
[{
  "success": true,
  "message": "Shortlist retrieved successfully",
  "data": [
    {
      "id": 3,
      "csr_user_id": 42,
      "request_id": 14,
      "status": "SHORTLISTED",
      "notes": null,
      "volunteered_hours": null,
      "shortlisted_at": "2024-11-07T10:30:00Z",
      "requests": {
        "id": 14,
        "title": "Food Distribution Drive",
        "description": "...",
        "service_type": "Community Service",
        "status": "ACTIVE"
      }
    }
  ]
}]
```

**Files Involved**:
- Boundary: `src/controller/shortlist/boundary/get_shortlist_boundary.py`
- Control: `src/controller/shortlist/get_shortlist_controller.py`
- Entity: `src/entity/shortlist.py` → `search_shortlist()`

---

### 2. POST /api/shortlist
**Purpose**: Add request to shortlist

**Authentication**: Required (JWT Bearer token)

**Request Body**:
```json
{
  "request_id": 13,
  "notes": "Interested in helping with this" // optional
}
```

**Response Format**:
```json
{
  "success": true,
  "message": "Request added to shortlist successfully",
  "data": {
    "id": 9,
    "csr_user_id": 42,
    "request_id": 13,
    "status": "SHORTLISTED",
    "shortlisted_at": "2024-11-07T11:00:00Z"
  }
}
```

**Validation**:
- Request must exist
- Request must be ACTIVE status
- User cannot shortlist same request twice (DB constraint)

**Files Involved**:
- Boundary: `src/controller/shortlist/boundary/add_to_shortlist_boundary.py`
- Control: `src/controller/shortlist/add_to_shortlist_controller.py`
- Entity: `src/entity/shortlist.py` → `add_to_shortlist()`

---

### 3. DELETE /api/shortlist/{id}
**Purpose**: Remove request from shortlist

**Authentication**: Required (JWT Bearer token)

**URL Parameters**:
- `id`: Shortlist item ID (not request ID!)

**Response Format**:
```json
{
  "success": true,
  "message": "Removed from shortlist successfully"
}
```

**Security**:
- User can only delete their own shortlist items
- Both shortlist_id AND csr_user_id must match

**Files Involved**:
- Boundary: `src/controller/shortlist/boundary/remove_from_shortlist_boundary.py`
- Control: `src/controller/shortlist/remove_from_shortlist_controller.py`
- Entity: `src/entity/shortlist.py` → `remove_from_shortlist()`

---

### 4. PATCH /api/shortlist/{id}/status
**Purpose**: Update shortlist item status/notes

**Authentication**: Required (JWT Bearer token)

**Request Body**:
```json
{
  "status": "COMPLETED",
  "notes": "Successfully helped with distribution",
  "volunteered_hours": 5.5
}
```

**Response Format**:
```json
{
  "success": true,
  "message": "Shortlist status updated successfully",
  "data": {
    "id": 9,
    "status": "COMPLETED",
    "volunteered_hours": 5.5
  }
}
```

**Files Involved**:
- Boundary: `src/controller/shortlist/boundary/update_shortlist_status_boundary.py`
- Control: `src/controller/shortlist/update_shortlist_status_controller.py`
- Entity: `src/entity/shortlist.py` → `update_shortlist_status()`

---

## 🎨 Visual Indicators

### Star Icon States
```
☆ (Outline)  - Not shortlisted
⭐ (Filled)   - Shortlisted
```

### Badge Overlay
```css
Purple badge with "✓ SHORTLISTED" appears on card image when shortlisted
```

### Status Badges (in shortlist page)
```
SHORTLISTED   → Purple badge
IN_PROGRESS   → Blue badge
COMPLETED     → Green badge
DECLINED      → Red badge
```

---

## 🔐 Security Features

1. **JWT Authentication**: All API calls require valid Bearer token
2. **Role-Based Access**: Only CSR Reps can access shortlist features
3. **Ownership Validation**: Users can only view/modify their own shortlist
4. **SQL Injection Prevention**: Supabase parameterized queries
5. **CSRF Protection**: Token-based auth prevents CSRF attacks

---

## 🐛 Known Issues & Fixes

### Array Wrapper Issue
**Problem**: Backend returns `[{success, data}]` instead of `{success, data}`

**Solution**: 
```javascript
const responseData = Array.isArray(response.data) 
  ? response.data[0] 
  : response.data;
```

**Files Fixed**: 
- `src/app/csr/page.js` (fetchShortlistedIds, handleToggleShortlist)

---

## 📝 Notes for Diagrams

### For Sequence Diagrams:
1. Show all layers: Frontend → Boundary → Control → Entity → Database
2. Include token validation steps
3. Show data transformation between layers
4. Include error paths (optional)
5. Mark return values with data structures

### For BCE Diagrams:
1. Draw three columns: Boundary | Control | Entity
2. Show component names and file paths
3. Draw arrows for method calls
4. Label each arrow with method name and parameters
5. Show database as separate box connected to Entity

### Color Coding Suggestion:
- Boundary (UI): Blue
- Control (Logic): Green
- Entity (Data): Orange
- Database: Red
- User Actions: Purple

---

**Document Version**: 1.0  
**Last Updated**: November 7, 2025  
**Author**: GitHub Copilot  
**Purpose**: Supporting documentation for sequence and BCE diagrams
