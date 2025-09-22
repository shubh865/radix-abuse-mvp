# Radix Abuse Dashboard (MVP)

A minimal viable product (MVP) for detecting, reporting, and managing **domain abuse** such as phishing and malware.  
This project includes:
- **Backend:** FastAPI + MySQL + SQLAlchemy
- **Frontend:** React + Vite
- **Database:** MySQL

---

## Features
- Submit new abuse reports
- Auto-detect **high-risk domains** based on rules
- View all reports in a dashboard
- Filter by risk level, date range, and domain
- Update domain status (`REVIEWED`, `ESCALATED`, `SUSPENDED`)
- API with Swagger documentation

---

### Folder Structure
```
radix-abuse-mvp/
│
├── backend/                # FastAPI backend code
│   ├── app/                 # Main backend application
│   │   ├── api/             # API route files
│   │   ├── core/            # Core settings and configs
│   │   ├── models/          # SQLAlchemy database models
│   │   ├── schemas/         # Pydantic schemas for validation
│   │   ├── services/        # Business logic & helper services
│   │   └── main.py          # Entry point for FastAPI app
│   │
│   ├── migrations/          # Alembic database migration files
│   │
│   ├── requirements.txt     # Python dependencies for backend
│   └── .env.example         # Example environment variables
│
├── frontend/               # React + Vite frontend
│   ├── src/                 # Frontend source files
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page-level React components
│   │   ├── styles/          # CSS and styling files
│   │   └── main.jsx         # React entry point
│   │
│   ├── public/              # Static assets (favicon, etc.)
│   └── package.json         # Frontend dependencies
│
├── docs/                    # Documentation and notes
│   └── architecture.md      # System architecture details
│
├── .gitignore               # Ignored files and folders
├── README.md                # Project documentation
└── LICENSE                  # License information
```

---

## Setup Instructions
Backend Setup (FastAPI + MySQL)
### 1. Clone the repository
git clone https://github.com/<your-username>/radix-abuse-mvp.git
cd radix-abuse-mvp

# 1. Navigate to the backend folder
cd backend
# 2. Create a Python virtual environment
python -m venv .venv
# 3. Activate the virtual environment
# Windows (PowerShell)
.\.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
# 4. Install all dependencies
pip install -r requirements.txt

5. Configure the .env file

Create a .env file inside the backend folder and add the following:

DB_USER=radix_user
DB_PASS=your_password_here
DB_HOST=localhost
DB_NAME=radix_abuse

# 6. Run database migrations
alembic upgrade head

# 7. Start the FastAPI backend server
uvicorn app.main:app --reload

Uvicorn running on http://127.0.0.1:8000
