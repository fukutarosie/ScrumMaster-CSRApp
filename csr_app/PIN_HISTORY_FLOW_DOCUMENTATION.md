# PIN History / Completed Matches - Code Flow Documentation

## Overview
This document explains how the "View History" feature works for PIN users to see their completed/fulfilled requests with matched CSR representatives.

---

## 🌐 User Journey

1. **PIN User** logs in and navigates to `/pin/history` or clicks "View History" from a fulfilled request detail page
2. **Frontend** makes a GET request to `/api/requests/history` with optional filters (date range, service type)
3. **Backend** authenticates the user, fetches fulfilled requests, applies filters, and returns paginated results
4. **Frontend** displays completed matches with CSR details, ratings, feedback, and completion dates

---

## 📂 File Structure

```
Frontend:
└── csr_app/src/app/(actors)/pin/history/page.js

Backend:
├── csr_app/src/api/request/get_completed_matches.py (Boundary)
├── csr_app/src/controller/request/get_completed_matches_controller.py (Controller)
└── csr_app/src/entity/request.py (Entity)
    └── csr_app/src/entity/shortlist.py (Entity)
```

---

## 🔄 Complete Code Flow (Request → Response)

### Step 1: Frontend Component Load (`page.js`)

**File:** `csr_app/src/app/(actors)/pin/history/page.js`

```javascript
// Lines 32-51: Authentication & Initial Load
useEffect(() => {
  const token = localStorage.getItem('token');
  const userData = localStorage.getItem('user');
  
  // Validate authentication
  if (!token || !userData) {
    router.push('/');
    return;
  }
  
  // Validate role
  const parsedUser = JSON.parse(userData);
  if (parsedUser.role.role_name !== 'PIN') {
    router.push('/');
    return;
  }
  
  setUser(parsedUser);
  fetchCompletedMatches(); // Initial data fetch
  fetchServiceTypes();     // Load filter options
}, [router]);
```

**Key Points:**
- Client-side authentication check (token + role validation)
- Loads user data from `localStorage`
- Redirects non-PIN users
- Fetches initial data and filter options

---

### Step 2: Frontend Data Fetching (`fetchCompletedMatches`)

**File:** `csr_app/src/app/(actors)/pin/history/page.js` (Lines 60-112)

```javascript
const fetchCompletedMatches = async () => {
  setLoading(true);
  setError('');
  
  try {
    const token = getToken();
    if (!token) {
      setError('Not authenticated');
      toast.error('Please log in again');
      return;
    }

    // Build query parameters
    const params = {
      page: currentPage,
      limit: 10
    };
    
    // Add optional filters
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    if (serviceType) params.service_type = serviceType;

    // Make API request
    const response = await axios.get('http://localhost:5000/api/requests/history', {
      headers: { 'Authorization': `Bearer ${token}` },
      params
    });

    // Handle response
    if (response.data.success) {
      setMatches(response.data.data || []);
      
      if (response.data.pagination) {
        setTotalPages(response.data.pagination.pages || 1);
        setTotalItems(response.data.pagination.total || 0);
      }
    }
  } catch (err) {
    console.error('[ERROR] Failed to fetch completed matches:', err);
    setError(err.response?.data?.message || 'Failed to fetch completed matches');
    toast.error(err.response?.data?.message || 'Failed to fetch completed matches');
  } finally {
    setLoading(false);
  }
};
```

**API Call Example:**
```
GET http://localhost:5000/api/requests/history?page=1&limit=10&start_date=2025-11-01&end_date=2025-11-11&service_type=Food Distribution
Headers: { Authorization: "Bearer <JWT_TOKEN>" }
```

**Key Points:**
- Attaches JWT token in Authorization header
- Sends pagination parameters (`page`, `limit`)
- Sends optional filters (`start_date`, `end_date`, `service_type`)
- Updates UI state based on response
- Handles errors gracefully

---

### Step 3: Backend Boundary Layer (HTTP Entry Point)

**File:** `csr_app/src/api/request/get_completed_matches.py`

```python
@get_completed_matches_boundary.route('/history', methods=['GET'])
@require_role('PIN')  # Middleware: Ensures only PIN users can access
def get_history():
    """Get completed matches (fulfilled requests) for authenticated PIN user"""
    
    # Extract JWT token from Authorization header
    auth_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    # Parse query parameters
    start_date = request.args.get('start_date', '').strip() or None
    end_date = request.args.get('end_date', '').strip() or None
    service_type = request.args.get('service_type', '').strip() or None
    page = request.args.get('page', '1')
    limit = request.args.get('limit', '10')
    
    # Instantiate controller and execute
    controller = GetCompletedMatchesController(
        auth_token, 
        start_date, 
        end_date, 
        page, 
        limit, 
        service_type
    )
    response, status = controller.execute()
    return jsonify(response), status
```

**Key Points:**
- `@require_role('PIN')` middleware validates the user's role before processing
- Extracts and cleans query parameters
- Instantiates `GetCompletedMatchesController` (OOP pattern)
- Returns JSON response with appropriate HTTP status code

---

### Step 4: Backend Controller Layer (Business Logic)

**File:** `csr_app/src/controller/request/get_completed_matches_controller.py`

#### 4.1 Controller Initialization (Lines 22-32)

```python
def __init__(self, auth_token: str, start_date: str = None, end_date: str = None,
             page_str: str = None, limit_str: str = None, service_type: str = None):
    """Initialize controller with request parameters"""
    self.auth_token = auth_token
    self.start_date = start_date
    self.end_date = end_date
    self.page_str = page_str
    self.limit_str = limit_str
    self.service_type = service_type.lower() if service_type else None
    self.user = None
    self.requests = []
```

#### 4.2 User Authentication (Lines 34-37)

```python
def authenticate_user(self) -> bool:
    """Authenticate user from token"""
    self.user = User.verify_token(self.auth_token)
    return self.user is not None
```

**Entity Call:**
- `User.verify_token(auth_token)` → Decodes JWT, verifies signature, fetches user from DB
- Returns `User` object or `None`

#### 4.3 Main Execution Flow (Lines 49-156)

```python
def execute(self) -> Tuple[Dict, int]:
    """Execute completed matches retrieval"""
    try:
        # 1. Authenticate
        if not self.authenticate_user():
            return (ResponseHelpers.error_response('Invalid or expired token', 401), 401)
        
        # 2. Get fulfilled requests for this PIN user
        self.requests = Request.by_pin_user(self.user.id)
        self.requests = [r for r in self.requests if r.status == Request.STATUS_FULFILLED]
        
        print(f"[DEBUG] Total fulfilled requests: {len(self.requests)}")
        
        # 3. Apply date filters
        if self.start_date:
            self.requests = [
                r for r in self.requests
                if self._is_on_or_after(r.fulfilled_at, self.start_date)
            ]
        if self.end_date:
            self.requests = [
                r for r in self.requests
                if self._is_on_or_before(r.fulfilled_at, self.end_date)
            ]
        
        # 4. Apply service type filter
        if self.service_type:
            self.requests = [
                r for r in self.requests
                if (r.service_type or '').lower() == self.service_type
            ]
        
        # 5. Parse pagination
        page, limit = self.parse_pagination()
        
        # 6. Apply pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_requests = self.requests[start:end]
        
        # 7. Convert to dictionaries & enrich with assignment data
        requests_data = []
        for req in paginated_requests:
            try:
                req_dict = req.to_dict()
                
                # Get assignment/match info
                assignment = Shortlist.active_assignment_for_request(req.id)
                if assignment:
                    req_dict['assignment_status'] = assignment.status
                    req_dict['active_assignment'] = assignment.to_assignment_dict()
                else:
                    req_dict['assignment_status'] = None
                    req_dict['active_assignment'] = None
                
                requests_data.append(req_dict)
            except Exception as e:
                print(f"[ERROR] Failed to process request {req.id}: {str(e)}")
                continue  # Skip problematic requests
        
        # 8. Build pagination info
        pagination = {
            'page': page,
            'limit': limit,
            'total': len(self.requests),
            'pages': (len(self.requests) + limit - 1) // limit
        }
        
        # 9. Return response
        response_data = {
            'success': True,
            'message': 'Completed matches retrieved successfully',
            'data': requests_data,
            'pagination': pagination
        }
        
        return (response_data, 200)
        
    except Exception as e:
        print(f"[ERROR] Get completed matches failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return (ResponseHelpers.error_response('Internal server error'), 500)
```

**Entity Calls:**
1. `User.verify_token(auth_token)` → Authenticates user
2. `Request.by_pin_user(user_id)` → Fetches all requests created by this PIN user
3. `Shortlist.active_assignment_for_request(request_id)` → Gets CSR assignment details for each request

#### 4.4 Date Filtering Helper Methods (Lines 159-199)

```python
def _parse_date(self, date_str: str) -> datetime:
    """Parse ISO datetime string or date string safely"""
    if not date_str:
        return None
    try:
        # Handle ISO datetime (e.g., "2025-11-10T15:30:00" or "2025-11-10T15:30:00Z")
        cleaned = date_str.replace('Z', '+00:00')
        return datetime.fromisoformat(cleaned)
    except Exception:
        try:
            # Handle date only (e.g., "2025-11-10")
            return datetime.strptime(date_str, '%Y-%m-%d')
        except Exception as e:
            print(f"[ERROR] Failed to parse date '{date_str}': {str(e)}")
            return None

def _is_on_or_after(self, date_str: str, start_date_str: str) -> bool:
    """Check if date is on or after start date"""
    if not date_str:
        return True  # Include requests without fulfilled_at date
    date_val = self._parse_date(date_str)
    start_val = self._parse_date(start_date_str)
    if not date_val or not start_val:
        return True  # Include if date parsing fails
    return date_val.date() >= start_val.date()

def _is_on_or_before(self, date_str: str, end_date_str: str) -> bool:
    """Check if date is on or before end date"""
    if not date_str:
        return True  # Include requests without fulfilled_at date
    date_val = self._parse_date(date_str)
    end_val = self._parse_date(end_date_str)
    if not date_val or not end_val:
        return True  # Include if date parsing fails
    return date_val.date() <= end_val.date()
```

**Key Points:**
- Handles both ISO datetime format (`2025-11-10T15:30:00Z`) and date-only format (`2025-11-10`)
- Gracefully handles missing or invalid dates (includes them in results to prevent data loss)
- Uses `.date()` for comparison to ignore time component

---

### Step 5: Backend Entity Layer (Database Operations)

#### 5.1 Request Entity - Fetch User's Requests

**File:** `csr_app/src/entity/request.py`

```python
@staticmethod
def by_pin_user(pin_user_id: int):
    """Get all requests created by a specific PIN user"""
    try:
        response = supabase.table('requests').select('*').eq('created_by', pin_user_id).execute()
        if response.data:
            return [Request.from_dict(req_data) for req_data in response.data]
        return []
    except Exception as e:
        print(f"[ERROR] Failed to fetch requests for PIN user {pin_user_id}: {str(e)}")
        return []
```

**Database Query:**
```sql
SELECT * FROM requests WHERE created_by = <pin_user_id>;
```

#### 5.2 Shortlist Entity - Fetch Assignment Details

**File:** `csr_app/src/entity/shortlist.py`

```python
@staticmethod
def active_assignment_for_request(request_id: int):
    """Get the active CSR assignment for a request"""
    try:
        response = supabase.table('shortlist') \
            .select('*, users:csr_user_id(id, username, full_name)') \
            .eq('request_id', request_id) \
            .in_('status', [Shortlist.STATUS_IN_PROGRESS, Shortlist.STATUS_COMPLETED]) \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return Shortlist.from_dict(response.data[0])
        return None
    except Exception as e:
        print(f"[ERROR] Failed to fetch assignment for request {request_id}: {str(e)}")
        return None
```

**Database Query:**
```sql
SELECT 
  shortlist.*, 
  users.id, users.username, users.full_name
FROM shortlist
LEFT JOIN users ON shortlist.csr_user_id = users.id
WHERE shortlist.request_id = <request_id>
  AND shortlist.status IN ('IN_PROGRESS', 'COMPLETED')
ORDER BY shortlist.created_at DESC
LIMIT 1;
```

**Key Points:**
- Fetches the most recent assignment for the request
- Joins with `users` table to get CSR Rep details
- Only includes `IN_PROGRESS` or `COMPLETED` assignments

#### 5.3 Shortlist Entity - Convert to Dictionary

```python
def to_assignment_dict(self):
    """Convert Shortlist to assignment dictionary for API response"""
    return {
        'id': self.id,
        'csr_user_id': self.csr_user_id,
        'status': self.status,
        'notes': self.notes,
        'volunteered_hours': self.volunteered_hours,  # Actually a rating (1-5)
        'completion_date': self.completion_date,
        'feedback_from_pin': self.feedback_from_pin,
        'csr_user': self.csr_user  # Nested user object from join
    }
```

---

### Step 6: Backend Response Structure

**Example Response:**

```json
{
  "success": true,
  "message": "Completed matches retrieved successfully",
  "data": [
    {
      "id": 5,
      "title": "NTUC Companionship Visit @ Yew Tee",
      "description": "Elderly companionship program",
      "category": "Social Care",
      "service_type": "Companionship",
      "status": "FULFILLED",
      "created_at": "2025-11-05T10:30:00Z",
      "fulfilled_at": "2025-11-10T14:00:00Z",
      "location_city": "Singapore",
      "location_detail": "Yew Tee Community Center",
      "priority": "HIGH",
      "view_count": 25,
      "shortlist_count": 3,
      "matched_csr": [
        {
          "id": 12,
          "csr_user_id": 8,
          "status": "COMPLETED",
          "notes": "Great experience helping seniors!",
          "volunteered_hours": 4.5,  // Rating: 4.5/5
          "completion_date": "2025-11-10",
          "feedback_from_pin": "Very professional and caring CSR!",
          "csr_user": {
            "id": 8,
            "username": "alice_csr",
            "full_name": "Alice Tan"
          }
        }
      ],
      "assignment_status": "COMPLETED",
      "active_assignment": {
        "id": 12,
        "csr_user_id": 8,
        "status": "COMPLETED",
        "notes": "Great experience helping seniors!",
        "volunteered_hours": 4.5,
        "completion_date": "2025-11-10",
        "feedback_from_pin": "Very professional and caring CSR!",
        "csr_user": {
          "id": 8,
          "username": "alice_csr",
          "full_name": "Alice Tan"
        }
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 15,
    "pages": 2
  }
}
```

---

### Step 7: Frontend Rendering

**File:** `csr_app/src/app/(actors)/pin/history/page.js` (Lines 261-382)

```javascript
matches.map((match) => (
  <div key={match.id} className="bg-white rounded-lg shadow overflow-hidden">
    <div className="p-6">
      {/* Request Title & Description */}
      <h3 className="text-lg font-bold text-gray-900 mb-2">{match.title}</h3>
      <p className="text-sm text-gray-600 mb-2">{match.description}</p>
      
      {/* Tags */}
      <div className="flex flex-wrap gap-2 mb-3">
        <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
          {match.category}
        </span>
        {match.service_type && (
          <span className="px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded-full">
            {match.service_type}
          </span>
        )}
        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
          FULFILLED
        </span>
      </div>
      
      {/* Fulfilled Date */}
      <div className="text-right ml-4">
        <p className="text-sm text-gray-500">Fulfilled on</p>
        <p className="text-sm font-semibold text-gray-900">{formatDate(match.fulfilled_at)}</p>
      </div>
      
      {/* CSR Match Details */}
      {match.matched_csr && match.matched_csr.length > 0 ? (
        <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded">
          <h4 className="font-semibold text-green-900 mb-3">Matched CSR Representative</h4>
          {match.matched_csr.map((csr) => (
            <div key={csr.id} className="space-y-2">
              {/* CSR User ID */}
              <div>
                <p className="text-green-700 font-medium">CSR User ID</p>
                <p className="text-green-900">#{csr.csr_user_id}</p>
              </div>
              
              {/* Volunteer Rating */}
              {csr.volunteered_rating && (
                <div>
                  <p className="text-green-700 font-medium">Volunteer Rating</p>
                  <p className="text-green-900">⭐ {csr.volunteered_hours}/5</p>
                </div>
              )}
              
              {/* Completion Date */}
              {csr.completion_date && (
                <div className="text-sm">
                  <p className="text-green-700 font-medium">Completion Date</p>
                  <p className="text-green-900">{formatDate(csr.completion_date)}</p>
                </div>
              )}
              
              {/* CSR Notes */}
              {csr.notes && (
                <div className="text-sm">
                  <p className="text-green-700 font-medium">CSR Notes</p>
                  <p className="text-green-900 italic">"{csr.notes}"</p>
                </div>
              )}
              
              {/* PIN Feedback */}
              {csr.feedback_from_pin && (
                <div className="text-sm">
                  <p className="text-green-700 font-medium">Your Feedback</p>
                  <p className="text-green-900 italic">"{csr.feedback_from_pin}"</p>
                </div>
              )}
              
              {/* Add Feedback Button (if not provided) */}
              {!csr.feedback_from_pin && (
                <button
                  onClick={() => router.push(`/pin/request/${match.id}?action=feedback`)}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  + Add Feedback for CSR
                </button>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-gray-50 border-l-4 border-gray-400 p-4 rounded">
          <p className="text-gray-600 text-sm">
            This request was marked as fulfilled but no CSR match details are available.
          </p>
        </div>
      )}
      
      {/* Request Stats */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-500">Created</p>
            <p className="font-medium">{formatDate(match.created_at)}</p>
          </div>
          <div>
            <p className="text-gray-500">Priority</p>
            <p className="font-medium">{match.priority}</p>
          </div>
          <div>
            <p className="text-gray-500">Views</p>
            <p className="font-medium">👁️ {match.view_count || 0}</p>
          </div>
          <div>
            <p className="text-gray-500">Shortlists</p>
            <p className="font-medium">⭐ {match.shortlist_count || 0}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
))
```

---

## 🔍 Key Features & Filters

### 1. Date Range Filtering (Lines 162-199)

```javascript
<input
  type="date"
  value={startDate}
  onChange={(e) => {
    const newStartDate = e.target.value;
    setStartDate(newStartDate);
    setCurrentPage(1);
    
    // Validate date range
    if (endDate && newStartDate && new Date(newStartDate) > new Date(endDate)) {
      setDateError('From Date cannot be after To Date');
    } else {
      setDateError('');
    }
  }}
  className={`w-full px-4 py-2 border rounded-lg ${dateError ? 'border-red-500' : 'border-gray-300'}`}
/>
```

**Features:**
- Client-side validation (From Date cannot be after To Date)
- Visual error feedback (red border + error message)
- Resets pagination when filter changes

### 2. Service Type Filtering (Lines 202-219)

```javascript
<select
  value={serviceType}
  onChange={(e) => {
    setCurrentPage(1);
    setServiceType(e.target.value);
  }}
  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
>
  <option value="">All Service Types</option>
  {serviceTypes.map((type) => (
    <option key={type.id} value={type.service_name}>
      {type.service_name}
    </option>
  ))}
</select>
```

**Features:**
- Dropdown populated from backend service types
- "All Service Types" option to clear filter
- Resets pagination when filter changes

### 3. Pagination (Lines 387-409)

```javascript
{totalPages > 1 && (
  <div className="mt-6 flex justify-center">
    <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
      <button
        onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
        disabled={currentPage === 1}
        className="relative inline-flex items-center px-4 py-2 rounded-l-md border"
      >
        Previous
      </button>
      <span className="relative inline-flex items-center px-4 py-2 border">
        Page {currentPage} of {totalPages}
      </span>
      <button
        onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
        disabled={currentPage === totalPages}
        className="relative inline-flex items-center px-4 py-2 rounded-r-md border"
      >
        Next
      </button>
    </nav>
  </div>
)}
```

**Features:**
- Only shown when multiple pages exist
- Previous/Next buttons with disabled states
- Page counter display

---

## 📊 Database Schema

### Relevant Tables

#### 1. `requests` Table
```sql
id                SERIAL PRIMARY KEY
title             VARCHAR(255) NOT NULL
description       TEXT
category          VARCHAR(100)
service_type      VARCHAR(100)
status            VARCHAR(50) -- 'ACTIVE', 'FULFILLED', 'SUSPENDED'
created_by        INTEGER REFERENCES users(id)
created_at        TIMESTAMP DEFAULT NOW()
fulfilled_at      TIMESTAMP
location_city     VARCHAR(100)
location_detail   TEXT
priority          VARCHAR(20)
view_count        INTEGER DEFAULT 0
shortlist_count   INTEGER DEFAULT 0
```

#### 2. `shortlist` Table
```sql
id                  SERIAL PRIMARY KEY
request_id          INTEGER REFERENCES requests(id)
csr_user_id         INTEGER REFERENCES users(id)
status              VARCHAR(50) -- 'SHORTLISTED', 'IN_PROGRESS', 'COMPLETED', 'WITHDRAWN'
notes               TEXT
volunteered_hours   DECIMAL(3,1) -- Actually a rating (1-5 scale)
completion_date     DATE
feedback_from_pin   TEXT
created_at          TIMESTAMP DEFAULT NOW()
```

#### 3. `users` Table
```sql
id          SERIAL PRIMARY KEY
username    VARCHAR(100) UNIQUE NOT NULL
full_name   VARCHAR(255)
email       VARCHAR(255) UNIQUE NOT NULL
role_id     INTEGER REFERENCES roles(id)
```

---

## 🔐 Security & Permissions

### 1. Middleware: `@require_role('PIN')`

**File:** `csr_app/src/controller/auth/auth_middleware.py`

- Validates JWT token
- Extracts user from token
- Checks if user has 'PIN' role
- Returns 403 Forbidden if role doesn't match

### 2. Data Isolation

- Controller uses `Request.by_pin_user(user.id)` to ensure PIN users can only see **their own** requests
- Never fetches other users' data

---

## 🐛 Error Handling

### Frontend Error Handling

```javascript
try {
  const response = await axios.get('http://localhost:5000/api/requests/history', {
    headers: { 'Authorization': `Bearer ${token}` },
    params
  });
  
  if (response.data.success) {
    setMatches(response.data.data || []);
  } else {
    toast.error(response.data.message || 'Failed to fetch completed matches');
  }
} catch (err) {
  console.error('[ERROR] Failed to fetch completed matches:', err);
  toast.error(err.response?.data?.message || 'Failed to fetch completed matches');
}
```

### Backend Error Handling

```python
try:
    # ... processing ...
    return (response_data, 200)
except Exception as e:
    print(f"[ERROR] Get completed matches failed: {str(e)}")
    import traceback
    traceback.print_exc()
    return (ResponseHelpers.error_response('Internal server error'), 500)
```

**Features:**
- Graceful degradation (skips problematic requests, continues processing)
- Detailed logging with tracebacks
- User-friendly error messages
- HTTP status codes (401, 403, 500)

---

## 🎯 Summary

| Layer | File | Responsibility |
|-------|------|----------------|
| **Frontend** | `pin/history/page.js` | UI, authentication check, API calls, rendering |
| **Boundary** | `get_completed_matches.py` | HTTP entry point, parameter extraction, middleware |
| **Controller** | `get_completed_matches_controller.py` | Business logic, filtering, pagination, orchestration |
| **Entity** | `request.py`, `shortlist.py` | Database queries, data transformation |

**Flow:**
1. Frontend sends GET `/api/requests/history?page=1&limit=10&start_date=2025-11-01`
2. Boundary extracts params, validates role, instantiates controller
3. Controller authenticates user, fetches requests, applies filters, paginates
4. Entity queries DB for requests and shortlist assignments
5. Controller enriches data, formats response
6. Boundary returns JSON response
7. Frontend renders completed matches with CSR details

**Key Techniques:**
- **OOP:** Controller as a class with instance methods
- **Separation of Concerns:** Boundary → Controller → Entity
- **Defensive Programming:** Graceful error handling, missing data tolerance
- **Performance:** Pagination to limit data transfer
- **Security:** JWT authentication, role-based access control, data isolation

