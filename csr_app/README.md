# CSR Application

Project developed for CSIT314 Software Development Methodologies.

## Overview
Full‑stack Customer Service Request (CSR) system using:
- Backend: Flask (Python) + Supabase PostgreSQL
- Frontend: Next.js 14 (React) + Tailwind CSS
- Architecture: BCE (Boundary‑Control‑Entity)

## Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- Git
- Supabase project (URL + anon/public key)

Verify versions:
```bash
python --version
node --version
npm --version
```

## Quick Start
Windows (PowerShell):
```bash
cd csr_app
.\run.ps1
```

Manual (all platforms – two terminals):
```bash
# Terminal 1: Backend
cd csr_app
python -m venv venv
venv\Scripts\activate   # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py           # http://localhost:5000

# Terminal 2: Frontend
cd csr_app
npm install
npm run dev             # http://localhost:3000
```

## Installation (Detailed)
1) Clone
```bash
git clone <your-repo-url>
cd csr_app
```

2) Backend setup
```bash
python -m venv venv
venv\Scripts\activate         # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

3) Environment variables
Create `.env` in `csr_app` (same folder as `app.py`). Minimal keys:
   ```env
SUPABASE_URL=your-project-url
   SUPABASE_KEY=your-anon-public-key
   FLASK_ENV=development
SECRET_KEY=dev-secret
```

4) Frontend dependencies
```bash
npm install
```

## Run
- Backend (Flask): `python app.py` → http://localhost:5000
- Frontend (Next.js): `npm run dev` → http://localhost:3000

## Useful Scripts
```bash
# Frontend
npm run dev       # start Next.js dev server
npm run build     # build production
npm run start     # run production build

# Backend
python app.py     # start Flask dev server
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

## Troubleshooting
- Port in use (5000/3000): stop existing processes, then retry.
- Missing packages: ensure venv is activated and re‑run `pip install -r requirements.txt` and `npm install`.
- Supabase errors: verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`.

## License
For coursework use within CSIT314. All rights reserved.