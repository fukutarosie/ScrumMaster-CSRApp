# A Corporate Social Responsibility (CSR) Web App to match Corporate Social Responsibility (CSR) corporate volunteers (CV) and Person-In-Needs (PINs)

Built with Next.js, Tailwind CSS, Flask, Supabase PostgreSQL, and BCE Architecture.

**Authors:** CSR ScrumMasters Team

---

## Getting Started

**Clone the repo**
```bash
git clone https://github.com/fukutarosie/ScrumMaster-CSRApp.git
cd ScrumMaster-CSRApp/csr_app
```

**Create `.env` file** (in `csr_app` folder)
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
FLASK_ENV=development
SECRET_KEY=dev-secret
```

**Set up virtual environment**
```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
```

**Install Python dependencies**
```bash
pip install -r requirements.txt
```

**Install NPM packages**
   ```bash
cd src
npm install
cd ..
```

**Start backend**
```bash
python app.py
```

**Start frontend** (in new terminal)
```bash
cd src
npm run dev
```

**Access application:** http://localhost:3000

---

## Default Login

- Admin: `admin1` / `password123`
- PIN User: `pin_user1` / `password123`
- CSR Rep: `csr_rep1` / `password123`

---

## Database Setup (First Time Only)

Run these SQL scripts in Supabase SQL Editor **in order**:
1. `STEP_1_BACKUP_SQL.sql`
2. `STEP_2_RENAME_SQL.sql`
3. `STEP_3_VERIFY_SQL.sql`


---

## 📄 License

For coursework use within CSIT314. All rights reserved.

---

## 🎓 Credits

Developed by the CSR ScrumMasters team for CSIT314 Software Development Methodologies, 2025.