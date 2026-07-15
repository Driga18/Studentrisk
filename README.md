# Student Risk Dashboard

A Flask-based application for tracking and analyzing student risk levels based on academic performance, attendance, and financial metrics.

## Features

- ✅ SQLite database for persistent data storage
- ✅ Glassmorphism-inspired UI
- ✅ Student risk scoring and dashboard analytics
- ✅ CRUD API for student records
- ✅ Desktop application wrapper using PyWebView

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Install dependencies

```powershell
cd c:\Users\ASUS\Desktop\Student_Risk
python -m pip install -r requirements.txt
```

### Run as a web app

```powershell
python app.py
```

Open your browser to `http://127.0.0.1:5000/dashboard`.

### Run as a desktop app

```powershell
python desktop.py
```

This starts the Flask backend locally and opens a desktop window pointing to the dashboard.

## Docker Setup

### Build and run with Docker Compose (recommended)

```powershell
docker-compose up --build
```

### Build and run with Docker CLI

```powershell
docker build -t student-risk-app .
docker run -d -p 5000:5000 --name student_risk_dashboard student-risk-app
```

## File Structure

```
Student_Risk/
├── app.py
├── config.py
├── databaseOJ.py
├── desktop.py
├── routes.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── templates/
│   └── dashboard.html
├── static/
│   └── background.jpg
└── instance/
    └── student_risk.db
```

## API Endpoints

- `GET /students` - Get all students
- `POST /students` - Create new student
- `GET /students/<id>` - Get specific student
- `PUT /students/<id>` - Update student
- `DELETE /students/<id>` - Delete student
- `GET /` - Home page
- `GET /dashboard` - Main dashboard

## Notes

- The desktop wrapper uses `pywebview` to create a native window.
- The SQLite file is stored under `instance/student_risk.db`.

