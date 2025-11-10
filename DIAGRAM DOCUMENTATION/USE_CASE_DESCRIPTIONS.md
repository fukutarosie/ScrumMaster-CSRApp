# Complete Use Case Descriptions

## System: Corporate Social Responsibility (CSR) Platform

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Actors](#actors)
3. [Authentication Use Cases](#authentication-use-cases)
4. [User Admin Use Cases](#user-admin-use-cases)
5. [Profile Management Use Cases](#profile-management-use-cases)
6. [Role Management Use Cases](#role-management-use-cases)
7. [PIN User Use Cases](#pin-user-use-cases)
8. [CSR Representative Use Cases](#csr-representative-use-cases)
9. [Platform Management Use Cases](#platform-management-use-cases)

---

## System Overview

The CSR Platform is a web-based application that connects Person-In-Need (PIN) users with Corporate Social Responsibility (CSR) representatives. The system facilitates the creation, management, and fulfillment of assistance requests while providing comprehensive administration and analytics capabilities.

### Key Features:
- User authentication and authorization
- Multi-role user management (User Admin, PIN, CSR Rep, Platform Management)
- Request creation and management
- Shortlisting and matching system
- Analytics and reporting
- Profile and role management

---

## Actors

### 1. User Admin
**Description**: System administrator responsible for managing user accounts, profiles, and roles.

**Responsibilities**:
- Create, view, update, and suspend user accounts
- Manage user profiles
- Create, update, and delete roles
- View system analytics

### 2. PIN (Person-In-Need)
**Description**: Individual or organization requesting assistance through the platform.

**Responsibilities**:
- Create assistance requests
- View and update own requests
- Track request status
- View shortlisted CSR representatives
- View request history

### 3. CSR Representative
**Description**: Corporate volunteer who browses and responds to assistance requests.

**Responsibilities**:
- Browse available requests
- Search and filter requests
- Shortlist requests of interest
- Manage shortlisted requests
- View shortlist history and statistics
- Update request status

### 4. Platform Management
**Description**: Senior administrator with oversight of platform operations and analytics.

**Responsibilities**:
- View platform-wide analytics
- Monitor system performance
- Access comprehensive reports

---

## Authentication Use Cases

### UC-AUTH-001: User Login

**Primary Actor**: Any User (User Admin, PIN, CSR Rep, Platform Management)

**Preconditions**:
- User has valid credentials
- User account is active

**Main Flow**:
1. User navigates to login page
2. System displays login form
3. User enters username, password, and selects role
4. System validates credentials
5. System verifies user role matches selected role
6. System generates JWT session token
7. System updates user's last login timestamp
8. System redirects user to role-specific dashboard
9. Use case ends

**Alternative Flows**:
- **3a. Invalid credentials**:
  - 3a1. System displays error message "Invalid credentials or user role mismatch"
  - 3a2. Use case returns to step 3
- **3b. Inactive account**:
  - 3b1. System displays error message "Account is inactive"
  - 3b2. Use case ends
- **3c. Missing required fields**:
  - 3c1. System displays validation errors
  - 3c2. Use case returns to step 3

**Postconditions**:
- User is authenticated and session is created
- User is redirected to appropriate dashboard

**Business Rules**:
- Password must be at least 8 characters
- Username must be at least 3 characters
- Account must be active
- Role must match user's assigned role

---

### UC-AUTH-002: User Logout

**Primary Actor**: Any Authenticated User

**Preconditions**:
- User is logged in with valid session token

**Main Flow**:
1. User clicks logout button
2. System validates session token
3. System invalidates session
4. System redirects user to login page
5. Use case ends

**Alternative Flows**:
- **2a. Invalid or expired token**:
  - 2a1. System redirects to login page
  - 2a2. Use case ends

**Postconditions**:
- User session is terminated
- User is redirected to login page

---

### UC-AUTH-003: Verify Session Token

**Primary Actor**: System

**Preconditions**:
- User has active session

**Main Flow**:
1. System receives request with authorization header
2. System extracts JWT token from header
3. System decodes and validates token
4. System retrieves user data from token payload
5. System loads user from database
6. System returns user information
7. Use case ends

**Alternative Flows**:
- **3a. Token expired**:
  - 3a1. System returns 401 Unauthorized error
  - 3a2. Use case ends
- **3b. Token invalid**:
  - 3b1. System returns 401 Unauthorized error
  - 3b2. Use case ends
- **5a. User not found**:
  - 5a1. System returns 401 Unauthorized error
  - 5a2. Use case ends

**Postconditions**:
- User identity is verified
- User information is available for request processing

---

## User Admin Use Cases

### UC-ADMIN-001: Create User Account

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- User Admin has access to user management

**Main Flow**:
1. User Admin navigates to create user page
2. System displays user creation form
3. User Admin enters username, password, email, full name, and selects role
4. User Admin submits form
5. System validates input data (format, length, required fields)
6. System checks username and email uniqueness
7. System hashes password
8. System creates User entity
9. System saves user to database
10. System logs user creation activity
11. System displays success message
12. Use case ends

**Alternative Flows**:
- **5a. Validation errors**:
  - 5a1. System displays validation error messages
  - 5a2. Use case returns to step 3
- **6a. Username already exists**:
  - 6a1. System displays error "Username already exists"
  - 6a2. Use case returns to step 3
- **6b. Email already exists**:
  - 6b1. System displays error "Email already exists"
  - 6b2. Use case returns to step 3

**Postconditions**:
- New user account is created in system
- User account is active
- Activity is logged

**Business Rules**:
- Username: 3-50 characters, alphanumeric and underscore only
- Password: minimum 8 characters
- Email: valid email format
- Full name: 2-100 characters
- Role ID must be valid existing role

---

### UC-ADMIN-002: View User Account

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Target user exists in system

**Main Flow**:
1. User Admin navigates to user management page
2. System displays list of users
3. User Admin selects specific user
4. System retrieves user data including role information
5. System displays user details
6. Use case ends

**Alternative Flows**:
- **4a. User not found**:
  - 4a1. System displays error "User not found"
  - 4a2. Use case ends

**Postconditions**:
- User details are displayed

---

### UC-ADMIN-003: Update User Account

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Target user exists in system

**Main Flow**:
1. User Admin views user account (UC-ADMIN-002)
2. User Admin clicks edit button
3. System displays edit form with current user data
4. User Admin modifies username, email, full name, or role
5. User Admin submits changes
6. System validates input data
7. System checks uniqueness (if username/email changed)
8. System updates User entity
9. System saves changes to database
10. System displays success message
11. Use case ends

**Alternative Flows**:
- **6a. Validation errors**:
  - 6a1. System displays validation error messages
  - 6a2. Use case returns to step 4
- **7a. Username/Email already exists**:
  - 7a1. System displays appropriate error message
  - 7a2. Use case returns to step 4

**Postconditions**:
- User account is updated
- Changes are persisted to database

**Business Rules**:
- Cannot change password through this use case
- Same validation rules as create user apply
- Cannot change own role (if editing own account)

---

### UC-ADMIN-004: Suspend User Account

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Target user exists and is active

**Main Flow**:
1. User Admin views user account (UC-ADMIN-002)
2. User Admin clicks suspend button
3. System displays confirmation dialog
4. User Admin confirms suspension
5. System sets user's is_active flag to false
6. System saves changes to database
7. System displays success message
8. Use case ends

**Alternative Flows**:
- **4a. User cancels suspension**:
  - 4a1. Use case ends without changes
- **6a. User already suspended**:
  - 6a1. System displays error "User is already suspended"
  - 6a2. Use case ends

**Postconditions**:
- User account is suspended (is_active = false)
- User cannot login

---

### UC-ADMIN-005: Search User Accounts

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated

**Main Flow**:
1. User Admin navigates to user management page
2. System displays search interface
3. User Admin enters search criteria (username, email, or full name)
4. User Admin submits search
5. System queries database with partial match (ILIKE)
6. System displays matching users
7. Use case ends

**Alternative Flows**:
- **5a. No users found**:
  - 5a1. System displays "No users found" message
  - 5a2. Use case ends

**Postconditions**:
- Matching users are displayed

---

## Profile Management Use Cases

### UC-PROFILE-001: Create User Profile

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated

**Main Flow**:
1. User Admin navigates to profile management
2. System displays create profile form
3. User Admin enters profile name and description
4. User Admin submits form
5. System validates input data
6. System checks profile name uniqueness
7. System creates Profile entity
8. System saves profile to database
9. System displays success message
10. Use case ends

**Alternative Flows**:
- **5a. Validation errors**:
  - 5a1. System displays validation error messages
  - 5a2. Use case returns to step 3
- **6a. Profile name already exists**:
  - 6a1. System displays error "Profile name already exists"
  - 6a2. Use case returns to step 3

**Postconditions**:
- New profile is created in system

**Business Rules**:
- Profile name must be at least 2 characters
- Profile name must be unique

---

### UC-PROFILE-002: View User Profile

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Profile exists

**Main Flow**:
1. User Admin navigates to profile management
2. System displays list of profiles
3. User Admin selects specific profile
4. System retrieves profile data
5. System displays profile details
6. Use case ends

**Postconditions**:
- Profile details are displayed

---

### UC-PROFILE-003: Update User Profile

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Profile exists

**Main Flow**:
1. User Admin views profile (UC-PROFILE-002)
2. User Admin clicks edit button
3. System displays edit form with current data
4. User Admin modifies profile name or description
5. User Admin submits changes
6. System validates input data
7. System checks uniqueness (if name changed)
8. System updates Profile entity
9. System saves changes with updated timestamp
10. System displays success message
11. Use case ends

**Alternative Flows**:
- **6a. Validation errors**: Same as create
- **7a. Name already exists**: Same as create

**Postconditions**:
- Profile is updated
- updated_at timestamp is set

---

### UC-PROFILE-004: Suspend User Profile

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Profile exists

**Main Flow**:
1. User Admin views profile (UC-PROFILE-002)
2. User Admin clicks suspend button
3. System displays confirmation dialog
4. User Admin confirms suspension
5. System updates profile status to suspended
6. System saves changes to database
7. System displays success message
8. Use case ends

**Postconditions**:
- Profile is suspended

---

### UC-PROFILE-005: Search User Profiles

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated

**Main Flow**:
1. User Admin navigates to profile management
2. System displays search interface
3. User Admin enters search criteria (profile name or description)
4. User Admin submits search
5. System queries database with partial match
6. System displays matching profiles
7. Use case ends

**Postconditions**:
- Matching profiles are displayed

---

## Role Management Use Cases

### UC-ROLE-001: Create Role

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated

**Main Flow**:
1. User Admin navigates to role management
2. System displays create role form
3. User Admin enters role name, role code, description, and dashboard route
4. User Admin submits form
5. System validates input data
6. System checks role name and code uniqueness
7. System creates Role entity
8. System saves role to database
9. System displays success message
10. Use case ends

**Alternative Flows**:
- **5a. Validation errors**:
  - 5a1. System displays validation errors
  - 5a2. Use case returns to step 3
- **6a. Role name or code already exists**:
  - 6a1. System displays error message
  - 6a2. Use case returns to step 3

**Postconditions**:
- New role is created

**Business Rules**:
- Role name: minimum 2 characters
- Role code: minimum 2 characters, typically uppercase
- Dashboard route: must be valid route path
- Role name and code must be unique

---

### UC-ROLE-002: View Role

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Role exists

**Main Flow**:
1. User Admin navigates to role management
2. System displays list of roles
3. User Admin selects specific role
4. System retrieves role data
5. System displays role details
6. Use case ends

**Postconditions**:
- Role details are displayed

---

### UC-ROLE-003: Update Role

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Role exists

**Main Flow**:
1. User Admin views role (UC-ROLE-002)
2. User Admin clicks edit button
3. System displays edit form with current data
4. User Admin modifies role details
5. User Admin submits changes
6. System validates input data
7. System checks uniqueness
8. System updates Role entity
9. System saves changes to database
10. System displays success message
11. Use case ends

**Postconditions**:
- Role is updated

---

### UC-ROLE-004: Delete Role

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated
- Role exists
- Role is not assigned to any users

**Main Flow**:
1. User Admin views role (UC-ROLE-002)
2. User Admin clicks delete button
3. System displays confirmation dialog
4. User Admin confirms deletion
5. System checks if role is assigned to users
6. System deletes role from database
7. System displays success message
8. Use case ends

**Alternative Flows**:
- **5a. Role is assigned to users**:
  - 5a1. System displays error "Cannot delete role assigned to users"
  - 5a2. Use case ends

**Postconditions**:
- Role is deleted from system

---

### UC-ROLE-005: Get All Roles

**Primary Actor**: User Admin

**Preconditions**:
- User Admin is authenticated

**Main Flow**:
1. User Admin navigates to role management
2. System retrieves all roles from database
3. System displays list of roles
4. Use case ends

**Postconditions**:
- All roles are displayed

---

### UC-ROLE-006: Get Public Roles

**Primary Actor**: System (for user registration)

**Preconditions**:
- None

**Main Flow**:
1. System needs list of roles for registration
2. System retrieves all roles except User Admin
3. System returns public roles
4. Use case ends

**Postconditions**:
- Public roles (non-admin) are returned

**Business Rules**:
- User Admin role should not be available for public registration

---

## PIN User Use Cases

### UC-PIN-001: Create New Request

**Primary Actor**: PIN User

**Preconditions**:
- PIN user is authenticated
- PIN user has role_id = 2 (PIN role)

**Main Flow**:
1. PIN user navigates to request creation page
2. System displays request form
3. PIN user enters title, description, selects service type, region, requested by date
4. PIN user uploads image (base64)
5. PIN user submits request
6. System validates input data
7. System validates user is PIN user
8. System validates service type exists
9. System processes and saves image
10. System creates Request entity
11. System sets status to ACTIVE
12. System saves request to database
13. System displays success message
14. Use case ends

**Alternative Flows**:
- **6a. Validation errors**:
  - 6a1. System displays validation errors
  - 6a2. Use case returns to step 3
- **7a. User is not PIN user**:
  - 7a1. System displays error "Unauthorized"
  - 7a2. Use case ends
- **8a. Invalid service type**:
  - 8a1. System displays error "Invalid service type"
  - 8a2. Use case returns to step 3
- **9a. Image upload fails**:
  - 9a1. System displays error "Image upload failed"
  - 9a2. Use case returns to step 4

**Postconditions**:
- New request is created with ACTIVE status
- Request is visible to CSR users
- Image is stored in system

**Business Rules**:
- Title: minimum 5 characters
- Description: minimum 10 characters
- Service type must be from predefined list
- Region must be specified
- Requested by date is required
- Image is required

---

### UC-PIN-002: View Own Requests

**Primary Actor**: PIN User

**Preconditions**:
- PIN user is authenticated

**Main Flow**:
1. PIN user navigates to dashboard
2. System retrieves all requests for PIN user
3. System displays requests in grid/list format
4. Use case ends

**Postconditions**:
- PIN user's requests are displayed

---

### UC-PIN-003: View Request Details

**Primary Actor**: PIN User

**Preconditions**:
- PIN user is authenticated
- Request exists and belongs to PIN user

**Main Flow**:
1. PIN user views own requests (UC-PIN-002)
2. PIN user clicks on specific request
3. System retrieves request details
4. System displays full request information
5. Use case ends

**Alternative Flows**:
- **3a. Request not found**:
  - 3a1. System displays error "Request not found"
  - 3a2. Use case ends
- **3b. Request belongs to different user**:
  - 3b1. System displays error "Unauthorized"
  - 3b2. Use case ends

**Postconditions**:
- Request details are displayed

---

### UC-PIN-004: Update Own Request

**Primary Actor**: PIN User

**Preconditions**:
- PIN user is authenticated
- Request exists, belongs to PIN user, and is ACTIVE

**Main Flow**:
1. PIN user views request details (UC-PIN-003)
2. PIN user clicks edit button
3. System displays edit form with current data
4. PIN user modifies title, description, service type, region, or date
5. PIN user optionally updates image
6. PIN user submits changes
7. System validates input data
8. System processes new image if provided
9. System updates Request entity
10. System sets updated_at timestamp
11. System saves changes to database
12. System displays success message
13. Use case ends

**Alternative Flows**:
- **7a. Validation errors**: Same as create
- **8a. Image upload fails**: Same as create
- **9a. Request is not ACTIVE**:
  - 9a1. System displays error "Cannot update non-active request"
  - 9a2. Use case ends

**Postconditions**:
- Request is updated
- updated_at timestamp is current

**Business Rules**:
- Can only update own requests
- Can only update ACTIVE requests
- Cannot change status through this use case

---

### UC-PIN-005: View Request History

**Primary Actor**: PIN User

**Preconditions**:
- PIN user is authenticated

**Main Flow**:
1. PIN user navigates to history page
2. System retrieves all requests for PIN user (including all statuses)
3. System displays requests with status indicators
4. Use case ends

**Postconditions**:
- All PIN user's requests are displayed with status

---

### UC-PIN-006: View Shortlisted CSR Users

**Primary Actor**: PIN User

**Preconditions**:
- PIN user is authenticated
- Request exists and belongs to PIN user
- Request has been shortlisted by CSR users

**Main Flow**:
1. PIN user views request details (UC-PIN-003)
2. System retrieves shortlist entries for request
3. System displays list of CSR users who shortlisted request
4. System shows shortlist status (SHORTLISTED, IN_PROGRESS, COMPLETED)
5. Use case ends

**Postconditions**:
- Shortlisted CSR users are displayed

---

## CSR Representative Use Cases

### UC-CSR-001: Browse Requests

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated

**Main Flow**:
1. CSR user navigates to browse page
2. System retrieves all ACTIVE, non-archived requests
3. System displays requests in grid format with preview
4. Use case ends

**Postconditions**:
- Active requests are displayed

---

### UC-CSR-002: Search Requests

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated

**Main Flow**:
1. CSR user navigates to browse page
2. CSR user enters search criteria (service type, region, keywords)
3. CSR user submits search
4. System queries requests matching criteria
5. System displays matching requests
6. Use case ends

**Alternative Flows**:
- **4a. No matching requests**:
  - 4a1. System displays "No requests found"
  - 4a2. Use case ends

**Postconditions**:
- Matching requests are displayed

---

### UC-CSR-003: View Request Details

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated
- Request is ACTIVE

**Main Flow**:
1. CSR user browses requests (UC-CSR-001)
2. CSR user clicks on specific request
3. System increments request view count
4. System retrieves request full details
5. System displays request information
6. Use case ends

**Postconditions**:
- Request details are displayed
- View count is incremented

---

### UC-CSR-004: Add Request to Shortlist

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated
- Request is ACTIVE
- Request not already shortlisted by this CSR user

**Main Flow**:
1. CSR user views request details (UC-CSR-003)
2. CSR user clicks "Add to Shortlist" button
3. System validates request is active
4. System checks for duplicate shortlist
5. System creates Shortlist entity
6. System sets status to SHORTLISTED
7. System sets shortlisted_at timestamp
8. System saves to database
9. System increments request shortlist_count
10. System displays success message
11. Use case ends

**Alternative Flows**:
- **3a. Request is not active**:
  - 3a1. System displays error "Request is not active"
  - 3a2. Use case ends
- **4a. Already shortlisted**:
  - 4a1. System displays error "Request already shortlisted"
  - 4a2. Use case ends

**Postconditions**:
- Request is added to CSR user's shortlist
- Request shortlist_count is incremented

---

### UC-CSR-005: View Shortlist

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated

**Main Flow**:
1. CSR user navigates to shortlist page
2. System retrieves all shortlist entries for CSR user
3. System joins with request details
4. System displays shortlisted requests with status
5. Use case ends

**Postconditions**:
- CSR user's shortlist is displayed

---

### UC-CSR-006: Remove from Shortlist

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated
- Request is in user's shortlist
- Shortlist status is SHORTLISTED (not in progress or completed)

**Main Flow**:
1. CSR user views shortlist (UC-CSR-005)
2. CSR user clicks remove button on request
3. System displays confirmation dialog
4. CSR user confirms removal
5. System retrieves shortlist entry
6. System deletes shortlist entry from database
7. System decrements request shortlist_count
8. System displays success message
9. Use case ends

**Alternative Flows**:
- **5a. Shortlist entry not found**:
  - 5a1. System displays error "Entry not found"
  - 5a2. Use case ends
- **5b. Shortlist status is not SHORTLISTED**:
  - 5b1. System displays error "Cannot remove in-progress or completed requests"
  - 5b2. Use case ends

**Postconditions**:
- Request is removed from shortlist
- Request shortlist_count is decremented

---

### UC-CSR-007: Update Shortlist Status

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated
- Request is in user's shortlist

**Main Flow**:
1. CSR user views shortlist (UC-CSR-005)
2. CSR user clicks update status button
3. System displays status options (IN_PROGRESS, COMPLETED, DECLINED)
4. CSR user selects new status
5. CSR user optionally enters notes, volunteered hours, completion date
6. CSR user submits update
7. System validates input data
8. System updates Shortlist entity
9. System sets updated_at timestamp
10. System saves changes to database
11. System displays success message
12. Use case ends

**Alternative Flows**:
- **7a. Invalid status transition**:
  - 7a1. System displays error "Invalid status transition"
  - 7a2. Use case returns to step 4

**Postconditions**:
- Shortlist status is updated
- Additional fields (hours, completion date) are saved if provided

**Business Rules**:
- Status transitions: SHORTLISTED → IN_PROGRESS → COMPLETED
- Status can change from any to DECLINED
- Completion date required when status is COMPLETED
- Volunteered hours optional

---

### UC-CSR-008: View Shortlist Statistics

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated

**Main Flow**:
1. CSR user navigates to shortlist page
2. System retrieves all shortlist entries for CSR user
3. System calculates statistics:
   - Total shortlisted
   - In progress count
   - Completed count
   - Declined count
   - Total volunteered hours
4. System displays statistics
5. Use case ends

**Postconditions**:
- Shortlist statistics are displayed

---

### UC-CSR-009: View Request History

**Primary Actor**: CSR Representative

**Preconditions**:
- CSR user is authenticated

**Main Flow**:
1. CSR user navigates to history page
2. System retrieves all completed and declined shortlist entries
3. System displays historical requests with outcomes
4. Use case ends

**Postconditions**:
- CSR user's history is displayed

---

## Platform Management Use Cases

### UC-PLATFORM-001: View Request Analytics

**Primary Actor**: Platform Management

**Preconditions**:
- Platform Management user is authenticated

**Main Flow**:
1. Platform user navigates to analytics dashboard
2. System retrieves request statistics:
   - Total requests by status
   - Requests by service type
   - Requests by region
   - Average view count
   - Average shortlist count
   - Fulfillment rate
3. System displays analytics with charts
4. Use case ends

**Postconditions**:
- Request analytics are displayed

---

### UC-PLATFORM-002: View Completed Matches

**Primary Actor**: Platform Management

**Preconditions**:
- Platform Management user is authenticated

**Main Flow**:
1. Platform user navigates to completed matches page
2. System retrieves shortlist entries with status = COMPLETED
3. System joins with request and CSR user data
4. System displays completed matches with details
5. Use case ends

**Postconditions**:
- Completed matches are displayed

---

### UC-PLATFORM-003: View Request Lookups

**Primary Actor**: Platform Management

**Preconditions**:
- Platform Management user is authenticated

**Main Flow**:
1. Platform user needs lookup data
2. System retrieves:
   - All service types
   - All regions (from requests)
   - All request statuses
3. System displays lookup data
4. Use case ends

**Postconditions**:
- Lookup data is available for filters and reports

---

## Non-Functional Requirements

### Security
- All passwords are hashed using pbkdf2:sha256
- JWT tokens used for session management (24-hour expiration)
- Role-based access control enforced at controller level
- Input sanitization for all user inputs
- Authorization checks before all operations

### Performance
- Image upload handling with base64 encoding
- Efficient database queries with retry mechanism
- Indexed foreign keys for fast lookups

### Usability
- Responsive web interface
- Clear error messages
- Confirmation dialogs for destructive actions
- Status indicators for requests and shortlists

### Reliability
- Retry mechanism for database operations
- Error logging for debugging
- Graceful error handling
- Activity logging for audit trail

---

## Data Validation Rules

### User Data
- Username: 3-50 characters, alphanumeric and underscore
- Password: minimum 8 characters
- Email: valid email format (contains @)
- Full name: 2-100 characters

### Request Data
- Title: minimum 5 characters
- Description: minimum 10 characters
- Service type: must exist in service_types table
- Region: required, non-empty string
- Requested by date: required, valid date format
- Image: required, valid base64 image data

### Profile Data
- Profile name: minimum 2 characters, unique
- Description: optional

### Role Data
- Role name: minimum 2 characters, unique
- Role code: minimum 2 characters, unique
- Dashboard route: required, valid path
- Description: optional

---

## Status Definitions

### Request Status
- **ACTIVE**: Request is active and visible to CSR users
- **SUSPENDED**: Request is temporarily suspended by admin or PIN user
- **FULFILLED**: Request has been completed
- **CANCELLED**: Request has been cancelled by PIN user

### Shortlist Status
- **SHORTLISTED**: CSR user has expressed interest
- **IN_PROGRESS**: CSR user is actively working on request
- **COMPLETED**: CSR user has completed the request
- **DECLINED**: CSR user has declined to proceed

### User Status
- **is_active = true**: User can login and use system
- **is_active = false**: User is suspended and cannot login

---

## End of Use Case Descriptions


