# CSR Application - Diagram Documentation Index

## 📚 Overview

This directory contains comprehensive documentation for creating BCE (Boundary-Control-Entity) class diagrams and sequence diagrams for the CSR (Corporate Social Responsibility) Application.

---

## 📁 Document Structure

### 1. Complete BCE Class Diagrams
**File**: `COMPLETE_BCE_CLASS_DIAGRAMS.md`

**Contents**:
- BCE Architecture Overview
- Complete class diagrams for all modules:
  - Authentication Module
  - User Account Management
  - User Profile Management
  - Role Management
  - Request Management (PIN)
  - Shortlist Management (CSR)
- Cross-module relationships
- Database schema mapping
- UML notation guide
- PlantUML examples

**Use For**: Creating class diagrams that show the structure and relationships between Boundary, Control, and Entity layers.

---

### 2. Complete Sequence Diagrams
**File**: `COMPLETE_SEQUENCE_DIAGRAMS.md`

**Contents**:
- Detailed sequence flows for:
  - User Login
  - Token Verification
  - Create User Account
  - Create PIN Request
  - Browse Active Requests
  - Add to Shortlist
  - Update Shortlist Status
- Common patterns (authentication, pagination)
- Error handling sequences

**Use For**: Creating sequence diagrams that show the flow of operations from user action through all layers to the database and back.

---

### 3. Shortlist Feature Documentation
**File**: `SHORTLIST_SEQUENCE_BCE_DOCUMENTATION.md`

**Contents**:
- Detailed BCE architecture for shortlist feature
- Component mapping
- Sequence diagrams:
  - Add to Shortlist
  - Remove from Shortlist
  - View Shortlist
- Database schema for shortlist table
- API endpoint documentation
- Known issues and fixes

**Use For**: Deep dive into the shortlist feature implementation with specific examples.

---

### 4. User Account Management - BCE Class Diagrams
**File**: `USERACCOUNT_BCE_CLASS_DIAGRAMS.md`

**Contents**:
- Complete BCE Architecture for User Account module
- 5 Boundary classes (Create, View, Update, Suspend, Search)
- 5 Control classes with validation functions
- User Entity with 20+ methods
- Helper classes (Validators, Sanitizers, Helpers)
- Database schema (users and roles tables)
- Method visibility summary (all public)
- API endpoints reference (8 endpoints)
- Response codes and validation rules
- Security features and error handling

**Use For**: Understanding the complete structure of the User Account Management module, including all classes, methods, and their relationships.

---

### 5. User Account Management - Sequence Diagrams
**File**: `USERACCOUNT_SEQUENCE_DIAGRAMS.md`

**Contents**:
- 8 Complete sequence diagrams:
  1. Create User Account (Success + Error)
  2. View All Users
  3. View Single User (Success + Error)
  4. Update User Account
  5. Suspend User Account
  6. Activate User Account
  7. Delete User Account (Success + Error)
  8. Search Users
- Detailed interaction flows between all layers
- Authentication and validation patterns
- Database operations
- Activity logging

**Use For**: Understanding the complete flow of User Account operations from HTTP request through all BCE layers to the database and back.

---

### 6. User Account Management - Documentation Summary
**File**: `USERACCOUNT_DOCUMENTATION_SUMMARY.md`

**Contents**:
- Overview of all User Account documentation
- Quick reference for API endpoints
- Response codes summary
- Complete method listing (22 public methods/functions)
- Validation rules reference
- Security features overview
- Database schema reference
- Common patterns and best practices
- Testing recommendations
- Future enhancement ideas

**Use For**: Quick reference and index for all User Account Management documentation. Start here for an overview, then dive into specific BCE or Sequence diagram documents.

---

## 🎯 Quick Start Guide

### For Creating Class Diagrams

1. **Read**: `COMPLETE_BCE_CLASS_DIAGRAMS.md`
2. **Choose** the module you want to diagram
3. **Copy** the ASCII art structure as a template
4. **Customize** with your tool of choice:
   - Draw.io (visual editor)
   - PlantUML (text-based)
   - Lucidchart (collaborative)

**Example Structure**:
```
┌─────────────────┐
│  Boundary Layer │
├─────────────────┤
│ LoginBoundary   │
│ + login()       │
└───────┬─────────┘
        │ calls
┌───────▼─────────┐
│  Control Layer  │
├─────────────────┤
│ LoginController │
│ + login(data)   │
└───────┬─────────┘
        │ uses
┌───────▼─────────┐
│  Entity Layer   │
├─────────────────┤
│ User Entity     │
│ + authenticate()│
└───────┬─────────┘
        │ queries
        ▼
    [Database]
```

---

### For Creating Sequence Diagrams

1. **Read**: `COMPLETE_SEQUENCE_DIAGRAMS.md`
2. **Find** the use case you need
3. **Copy** the ASCII sequence as a template
4. **Implement** using:
   - Mermaid (markdown-based)
   - PlantUML (text-based)
   - draw.io (visual editor)

**Example Sequence**:
```
User → Browser → Boundary → Controller → Entity → Database
 │       │          │           │          │        │
 │───────>          │           │          │        │
 │       │──────────>           │          │        │
 │       │          │───────────>          │        │
 │       │          │           │──────────>        │
 │       │          │           │          │────────>
 │       │          │           │          │<────────
 │       │          │           │<──────────        │
 │       │          │<───────────          │        │
 │       │<──────────           │          │        │
 │<───────          │           │          │        │
```

---

## 🛠️ Recommended Tools

### For Class Diagrams

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| **Draw.io** | Visual | Free | Quick diagrams, presentations |
| **Lucidchart** | Visual | Freemium | Collaborative work, professional diagrams |
| **PlantUML** | Text | Free | Version control, automation |
| **StarUML** | Visual | Paid | Professional UML modeling |
| **Enterprise Architect** | Visual | Paid | Enterprise-grade modeling |

### For Sequence Diagrams

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| **Mermaid** | Text | Free | Documentation, GitHub markdown |
| **PlantUML** | Text | Free | Version control, automation |
| **SequenceDiagram.org** | Visual | Free | Quick online diagrams |
| **draw.io** | Visual | Free | Visual editing, presentations |
| **Lucidchart** | Visual | Freemium | Professional, collaborative |

---

## 📖 How to Read the Documentation

### Understanding BCE Layers

**Boundary Layer (B)**:
- Location: `src/controller/*/boundary/*.py`
- Purpose: Handle HTTP requests/responses
- Keywords: Routes, Blueprints, REST endpoints
- Look for: `@route`, `request`, `jsonify`

**Control Layer (C)**:
- Location: `src/controller/*/*.py` (controller files)
- Purpose: Business logic and rules
- Keywords: Validation, transformation, orchestration
- Look for: Static methods, business rules

**Entity Layer (E)**:
- Location: `src/entity/*.py`
- Purpose: Data access and persistence
- Keywords: CRUD operations, queries, database
- Look for: Supabase calls, SQL queries

---

## 🎨 Color Coding Convention

Use these colors when creating visual diagrams:

```
┌───────────────────────────────────────┐
│ Boundary Layer (UI/HTTP)   │ #3B82F6 │ Blue
│ Control Layer (Logic)      │ #10B981 │ Green
│ Entity Layer (Data)        │ #F59E0B │ Orange
│ Database                   │ #EF4444 │ Red
│ User/Actor                 │ #8B5CF6 │ Purple
│ External System            │ #6B7280 │ Gray
└───────────────────────────────────────┘
```

---

## 📋 Checklist for Creating Diagrams

### Class Diagram Checklist
- [ ] Shows all three BCE layers
- [ ] Includes class names and file paths
- [ ] Shows public methods with parameters
- [ ] Indicates relationships with arrows
- [ ] Labels arrows with relationship type (calls, uses, extends)
- [ ] Includes database table representation
- [ ] Shows inheritance or composition where applicable
- [ ] Uses consistent notation (UML standard)

### Sequence Diagram Checklist
- [ ] Shows all participants (actors and components)
- [ ] Includes lifelines for all participants
- [ ] Numbers each step sequentially
- [ ] Shows both requests and responses
- [ ] Includes authentication/authorization steps
- [ ] Shows database queries explicitly
- [ ] Indicates return values with types
- [ ] Covers error cases (alt/else blocks)
- [ ] Uses activation bars for processing time
- [ ] Labels async calls if applicable

---

## 🔗 Related Documentation

### In Main Project Directory
- `PROJECT_DOCUMENTATION.md` - Overall project overview
- `DATABASE_SCHEMA_EXPLAINED.md` - Database design details
- `DOCUMENTATION_INDEX.md` - Complete documentation index
- `QUICKSTART.md` - How to run the application

### In csr_app Directory
- `README.md` - Project README
- `LOGIN_CREDENTIALS.md` - Test user credentials
- `REUSABLE_CARD_COMPONENTS_GUIDE.md` - Frontend components

---

## 🎓 Educational Context

This application follows **2-layer BCE architecture**, which is commonly taught in:
- **CS/SE Courses**: Software Engineering, System Design
- **Common Names**: 
  - BCE Pattern (Boundary-Control-Entity)
  - 3-Tier Architecture (Presentation-Business-Data)
  - Layered Architecture
  - MVC Variant (Model-View-Controller)

**Benefits of BCE**:
1. **Separation of Concerns**: Each layer has distinct responsibilities
2. **Testability**: Layers can be tested independently
3. **Maintainability**: Changes in one layer don't affect others
4. **Scalability**: Easy to scale individual layers
5. **Educational**: Clear structure for learning software design

---

## 📊 Diagram Examples

### Full System Overview Diagram
```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                       │
│            (Next.js React - Not in BCE)                 │
│  /pin (PIN Dashboard) | /csr (CSR Dashboard) | /admin   │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP REST API
┌───────────────────────▼─────────────────────────────────┐
│                   BOUNDARY LAYER                         │
│  Login | Users | Profiles | Roles | Requests | Shortlist│
│  Flask Blueprints - Route Handlers                      │
└───────────────────────┬─────────────────────────────────┘
                        │ Method Calls
┌───────────────────────▼─────────────────────────────────┐
│                   CONTROL LAYER                          │
│  Business Logic - Validation - Transformation            │
│  LoginController | UserController | RequestController   │
└───────────────────────┬─────────────────────────────────┘
                        │ Database Operations
┌───────────────────────▼─────────────────────────────────┐
│                    ENTITY LAYER                          │
│  Data Access Objects - CRUD Operations                   │
│  User | Role | Profile | Request | Shortlist           │
└───────────────────────┬─────────────────────────────────┘
                        │ SQL Queries
┌───────────────────────▼─────────────────────────────────┐
│                  DATABASE LAYER                          │
│         Supabase (PostgreSQL)                            │
│  users | roles | user_profiles | requests | shortlist   │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Tips for Students/Developers

### When Creating Class Diagrams:
1. Start with one module (e.g., Authentication)
2. Draw vertically: Boundary → Control → Entity → Database
3. Show method signatures clearly
4. Don't overcomplicate - focus on main methods
5. Use consistent arrow styles

### When Creating Sequence Diagrams:
1. Choose a specific user story (e.g., "User logs in")
2. Include EVERY step, even simple ones
3. Show database queries explicitly
4. Include authentication checks
5. Show both success and error paths
6. Number each step for easy reference

### Common Mistakes to Avoid:
❌ Mixing layers (e.g., Boundary calling Entity directly)
❌ Skipping the authentication steps
❌ Forgetting to show database operations
❌ Missing return arrows
❌ Inconsistent naming (use actual class/method names)
❌ Too much or too little detail

---

## 🎯 Quick Reference

### File Locations
```
src/
├── controller/
│   ├── auth/
│   │   ├── boundary/
│   │   │   └── login_boundary.py         [Boundary]
│   │   └── login_controller.py           [Control]
│   ├── userAccount/
│   │   ├── boundary/                     [Boundary]
│   │   └── *_controller.py               [Control]
│   ├── request/
│   │   ├── boundary/                     [Boundary]
│   │   └── *_controller.py               [Control]
│   └── shortlist/
│       ├── boundary/                     [Boundary]
│       └── *_controller.py               [Control]
└── entity/
    ├── user.py                           [Entity]
    ├── role.py                           [Entity]
    ├── profile.py                        [Entity]
    ├── request.py                        [Entity]
    └── shortlist.py                      [Entity]
```

### HTTP Methods → Operations
```
POST   → Create (e.g., create user, create request)
GET    → Read (e.g., get user, list requests)
PUT    → Update (full replacement)
PATCH  → Update (partial update)
DELETE → Delete (remove resource)
```

### Database Tables
```
users          → User accounts and authentication
roles          → User roles (PIN, CSR Rep, Admin, etc.)
user_profiles  → Extended user information
requests       → Service requests created by PINs
shortlist      → CSR shortlisted requests
```

---

## 📞 Questions or Clarifications?

If you need clarification on any diagram or flow:

1. **Check**: The specific module documentation first
2. **Review**: The code in `src/controller/` and `src/entity/`
3. **Trace**: Follow a request through the codebase
4. **Test**: Use the API endpoints with Postman/curl

---

## 📝 Document Maintenance

**Created**: November 8, 2025  
**Last Updated**: November 8, 2025  
**Version**: 1.0  
**Maintainer**: Development Team

**Update Schedule**:
- Update diagrams when major features are added
- Review documentation each semester/term
- Keep file paths synchronized with actual code structure

---

## ✅ Summary

This directory provides everything you need to create professional BCE class diagrams and sequence diagrams for the CSR Application:

✓ **Complete class structures** for all modules  
✓ **Detailed sequence flows** for major use cases  
✓ **Real code examples** with file paths  
✓ **Tool recommendations** for creating diagrams  
✓ **Best practices** and common patterns  
✓ **Error handling** examples  

**Next Steps**:
1. Choose a module or use case to diagram
2. Read the relevant documentation file
3. Select your diagramming tool
4. Create your diagram following the examples
5. Validate against the actual code

Happy diagramming! 🎨📊




