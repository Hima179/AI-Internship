# Universal AI University — Student Mental Health & Counseling Analytics System

An integrated digital mental health screening and counseling platform developed during the Summer Internship Project (SIP) at Universal AI University by Himanshu Pathak (B-Tech AI/ML).

---

## 🏛️ System Overview

The system bridges students, faculty mentors, and licensed campus counsellors into a unified diagnostic and intervention workflow:

1. **Student Wellness Intake Portal** (`student-survey-portal/`):
   - Fast, mobile-responsive psychological wellness intake surveys (PHQ-9, GAD-7, and custom clinical metrics).
   - Automated risk triaging that flags high-acuity cases immediately.

2. **Counsellor Analytics Dashboard** (`uai-counsellor-dashboard/`):
   - Modern React + Vite dashboard for counsellors to review student submissions, track longitudinal wellbeing trends, and schedule follow-ups.

3. **Backend API & Clinical Scoring Engine** (`app/`):
   - Python Flask core orchestrating authentication, role-based access control (Student, Faculty Mentor, Counsellor, Administrator), automated risk score calculation (`app/scoring.py`), and dynamic PDF generation (`app/reports.py`).

4. **Multi-Service Launcher** (`integrated_launcher/`):
   - Service orchestrator running Flask backend, intake portal, and counsellor dashboard concurrently.

5. **SIP Documentation & Benchmarks**:
   - Automated scripts for generating formal university handbook submissions, weekly milestone reports, presentations, and system benchmark latency figures.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy, ReportLab, PyMuPDF
- **Frontend**: React, Vite, Tailwind CSS, Lucide Icons, Framer Motion
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Deployment & CI/CD**: Docker, GitHub Actions, Railway / Render configuration

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Hima179/AI-Internship.git
cd AI-Internship
```

### 2. Setup Python Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Backend Server
```bash
python run.py
```

### 4. Run Frontend Applications
```bash
# Student Survey Portal
cd student-survey-portal
# Counsellor Dashboard
cd ../uai-counsellor-dashboard
npm install
npm run dev
```

---

## 👤 Author
**Himanshu Pathak**  
B-Tech AI & Machine Learning  
Universal AI University
