# Student Risk Dashboard

A Flask-based web application for tracking and analyzing student risk levels based on academic performance, attendance, and financial metrics.

## Features

- ✅ SQLite database for persistent data storage
- ✅ Beautiful glassmorphism UI with background imagery
- ✅ Real-time risk assessment charts (Progress Overview & Risk Distribution)
- ✅ Student management (Create, Read, Update, Delete)
- ✅ Interactive dashboard with student details
- ✅ Responsive web design

## Quick Start (Local)

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone/download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open browser to: `http://localhost:5000/dashboard`

## Docker Setup

### Build and Run with Docker Compose (Recommended)

```bash
# Build and run the container
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the container
docker-compose down

# View logs
docker-compose logs -f
```

The app will be available at: `http://localhost:5000`

### Build and Run with Docker CLI

```bash
# Build the image
docker build -t student-risk-app .

# Run the container
docker run -d -p 5000:5000 \
  -v $(pwd)/instance:/app/instance \
  --name student_risk_dashboard \
  student-risk-app

# View logs
docker logs -f student_risk_dashboard

# Stop the container
docker stop student_risk_dashboard
```

## File Structure

```
Student_Risk/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── databaseOJ.py         # Database models
├── routes.py             # API routes
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Files to exclude from Docker
├── .gitignore            # Files to exclude from Git
├── static/               # Static files (CSS, images)
│   └── background.jpg    # Dashboard background
├── templates/            # HTML templates
│   └── dashboard.html    # Main dashboard page
└── instance/             # SQLite database (auto-created)
    └── student_risk.db
```

## API Endpoints

### Students
- `GET /students` - Get all students
- `POST /students` - Create new student
- `GET /students/<id>` - Get specific student
- `PUT /students/<id>` - Update student
- `DELETE /students/<id>` - Delete student

### Web Pages
- `GET /` - Home page
- `GET /dashboard` - Main dashboard

## Database

The application uses SQLite for data storage. The database file (`student_risk.db`) is automatically created in the `instance/` directory on first run.

## Environment Variables

- `FLASK_ENV` - Set to `production` for Docker
- `FLASK_APP` - Default: `app.py`

## Technology Stack

- **Backend**: Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML, CSS, Chart.js
- **Containerization**: Docker, Docker Compose

## License

MIT
