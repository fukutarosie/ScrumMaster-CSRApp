# CSR Application

Full-stack Customer Service Request system for CSIT314 Software Development Methodologies.

---

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- Git
- Supabase project (URL + anon key)

---

## Setup & Run

### 1. Clone Repository
```bash
git clone https://github.com/fukutarosie/ScrumMaster-CSRApp.git
cd ScrumMaster-CSRApp/csr_app
```

### 2. Create `.env` File
Create `.env` in the `csr_app` folder with:
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
FLASK_ENV=development
SECRET_KEY=dev-secret
```

### 3. Run Database Migration (First Time Only)
Open Supabase SQL Editor and run **in order**:
1. `STEP_1_BACKUP_SQL.sql`
2. `STEP_2_RENAME_SQL.sql`
3. `STEP_3_VERIFY_SQL.sql`

### 4. Start Backend (Terminal 1)
```bash
cd csr_app
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
✅ Backend: http://localhost:5000

### 5. Start Frontend (Terminal 2)
```bash
cd csr_app/src
npm install
npm run dev
```
✅ Frontend: http://localhost:3000

### 6. Access Application
Open browser: http://localhost:3000

**Login Credentials:**
- Admin: `admin1` / `password123`
- PIN User: `pin_user1` / `password123`
- CSR Rep: `csr_rep1` / `password123`

---

## 🛠️ Useful Commands

### Backend (Flask)
```bash
# Start development server
python app.py

# With specific port
python app.py --port 5001

# Test imports
python -c "from src.entity.user import User; print('✓ User entity OK')"
```

### Frontend (Next.js)
```bash
# Development server
npm run dev

# Production build
npm run build
npm run start

# Lint code
npm run lint
```

### Virtual Environment
```bash
# Activate (do this every time you open a new terminal)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Deactivate
deactivate

# Verify activation (you should see "(venv)" in your prompt)
```

## Folder Structure (simplified)
```
csr_app/
├─ app.py                  # Flask entry
├─ requirements.txt
├─ package.json
├─ src/
│  ├─ app/                 # Next.js app router
│  ├─ api/                 # Flask blueprints (HTTP endpoints)
│  ├─ controller/          # Controllers (BCE: Boundary/Control)
│  ├─ entity/              # Entities & business logic
│  └─ utils/               # Validators, helpers, middleware
└─ tests/
   └─ test_login.py
```

## Testing
```bash
venv\Scripts\activate          # source venv/bin/activate on macOS/Linux
pytest -q                      # if pytest installed, or:
python tests/test_login.py
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **Port Already in Use (5000 or 3000)**
**Error:** `Address already in use` or `Port 5000 is already in use`

**Solution:**
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <process-id> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

#### 2. **Virtual Environment Not Activating**
**Error:** Commands like `pip` install globally instead of in venv

**Solution:**
```bash
# Make sure you're in the csr_app directory
cd csr_app

# Recreate virtual environment
rm -rf venv        # macOS/Linux
rmdir /s venv      # Windows

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

#### 3. **Module Not Found / Import Errors**
**Error:** `ModuleNotFoundError: No module named 'flask'` or similar

**Solution:**
```bash
# Ensure virtual environment is activated (you should see "(venv)" in prompt)
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. **Supabase Connection Errors**
**Error:** `Invalid API key` or `Connection refused`

**Solution:**
1. Check your `.env` file exists in `csr_app/` folder
2. Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
3. Ensure no extra spaces or quotes in `.env`:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. Restart the backend server after changing `.env`

#### 5. **Database Table Not Found**
**Error:** `Could not find the table 'public.users'` or similar

**Solution:**
Your database needs the migration! Run the SQL scripts:
1. Open Supabase SQL Editor
2. Run `STEP_1_BACKUP_SQL.sql`
3. Run `STEP_2_RENAME_SQL.sql`
4. Run `STEP_3_VERIFY_SQL.sql`

See "🔧 Important: Database Schema Migration" section above.

#### 6. **npm install Fails**
**Error:** `EACCES` permission errors or `gyp ERR!`

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json    # macOS/Linux
rmdir /s node_modules & del package-lock.json    # Windows

# Reinstall
npm install
```

#### 7. **Frontend Shows "Failed to Fetch" or Network Errors**
**Symptoms:** Login doesn't work, data doesn't load

**Solution:**
1. Verify backend is running: `http://localhost:5000/api/roles/public`
2. Check browser console for CORS errors
3. Ensure both terminals (backend + frontend) are running
4. Try clearing browser cache (Ctrl+Shift+Delete)

#### 8. **Python Command Not Found**
**Error:** `python: command not found`

**Solution:**
```bash
# Try using python3 instead
python3 --version
python3 -m venv venv
python3 app.py
```

---

## 📞 Getting Help

If you encounter issues:
1. Check the terminal output for error messages
2. Look in the Troubleshooting section above
3. Check `MIGRATION_COMPLETE.md` for database migration details
4. Review the `.env` file for correct Supabase credentials

---

## 📝 Features

- **User Management** (Admin)
  - Create, view, update, suspend user accounts
  - Role-based access control (Admin, PIN, CSR Rep)

- **PIN Requests** (PIN Users)
  - Create service requests with details and images
  - Track request status (Active, Fulfilled, Suspended)
  - View analytics (CSR views, shortlists)
  - Provide feedback and ratings for completed requests

- **CSR Volunteering** (CSR Reps)
  - Browse available service requests
  - Shortlist interesting opportunities
  - Mark requests as in-progress or completed
  - View volunteering history and ratings

- **Real-time Updates**
  - Request status tracking
  - Audit history for status changes
  - Automatic timestamp updates

---

## 🏗️ Architecture

**Backend (Flask + Supabase):**
- **Boundary Layer:** API endpoints (`src/api/`)
- **Control Layer:** Controllers (`src/controller/`)
- **Entity Layer:** Business logic and data models (`src/entity/`)
- **Utilities:** Validators, sanitizers, middleware (`src/utils/`)

**Frontend (Next.js):**
- **App Router:** Role-based dashboards (`src/app/(actors)/`)
- **Components:** Reusable UI components (`src/app/components/`)
- **Middleware:** Authentication and route protection

---

## 📄 License

For coursework use within CSIT314. All rights reserved.

---

## 🎓 Credits

Developed by the CSR ScrumMasters team for CSIT314 Software Development Methodologies, 2025.