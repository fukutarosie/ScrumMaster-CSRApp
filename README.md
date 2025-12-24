# Corporate Social Responsibility (CSR) Web App

CSR Web App matches Corporate Social Responsibility (CSR) corporate volunteers (CV) and Person-In-Needs (PINs). Built with Next.js, Tailwind CSS, Flask, Supabase PostgreSQL, BCE Architecture and Test-Driven Development (TDD).

**Authors:** CSR ScrumMasters Team

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Supabase account (for database)

### 1. Clone the Repository
```bash
git clone https://github.com/fukutarosie/ScrumMaster-CSRApp.git
cd ScrumMaster-CSRApp
```

### 2. Backend Setup (Flask)

**Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
```

**Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**Create `environment.env` file** (in project root):
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Start Flask backend:**
```bash
python app.py
```
Backend will run at: http://localhost:5000

### 3. Frontend Setup (Next.js)

**Install NPM packages:**
```bash
npm install
```

**Create `.env.local` file** (in project root, optional for local development):
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```
*Note: This defaults to `http://localhost:5000` if not set, so it's optional for local development.*

**Start Next.js frontend:**
```bash
npm run dev
```
Frontend will run at: http://localhost:3000

### 4. Access the Application
Open your browser and navigate to: **http://localhost:3000**

### 4. Access the Application
Open your browser and navigate to: **http://localhost:3000**

---

## Default Login Credentials

| Role                  | Username        | Password      |
|-----------------------|-----------------|---------------|
| Admin                 | `admin1`        | `password123` |
| PIN User              | `pin_user1`     | `password123` |
| CSR Representative    | `csr_rep1`      | `password123` |
| Platform Management   | `platform_mgr1` | `password123` |

---

## Deployment to Vercel

### Prerequisites
1. Deploy your Flask backend to a hosting service (Render, Railway, etc.)
2. Get your backend production URL (e.g., `https://your-app.onrender.com`)

### Steps
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and import your repository
3. Add environment variable in Vercel dashboard:
   - **Key:** `NEXT_PUBLIC_API_URL`
   - **Value:** Your Flask backend URL (e.g., `https://your-app.onrender.com`)
4. Deploy!

---

## Project Structure

```
ScrumMaster-CSRApp/
├── app.py                 # Flask backend entry point
├── requirements.txt       # Python dependencies
├── environment.env        # Backend environment variables (create this)
├── package.json           # Node.js dependencies
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── vercel.json           # Vercel deployment config
├── src/
│   ├── app/              # Next.js app directory (frontend pages)
│   ├── config/           # API configuration
│   ├── controller/       # Flask controllers (business logic)
│   ├── entity/           # Database entities/models
│   ├── api/              # Flask API boundaries (routes)
│   └── utils/            # Utility functions
├── static/               # Static files (uploads, etc.)
└── tests/                # Test files
```

---

## 🎓 Credits

Developed by the CSR ScrumMasters team for CSIT314 Software Development Methodologies, 2025.