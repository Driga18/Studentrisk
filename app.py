from flask import Flask, render_template
from databaseOJ import db, Student
from routes import student_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Bind db to this app
db.init_app(app)

# Register routes
app.register_blueprint(student_bp, url_prefix="/students")

@app.route("/")
def home():
    return "Student Risk Tracking System is running!"

# Dashboard route
@app.route("/dashboard")
def dashboard():
    students = Student.query.all()
    students_data = [{
        "id": s.id,
        "name": s.name,
        "programme": s.programme,
        "gpa": s.gpa,
        "attendance": s.attendance,
        "fees_balance": s.fees_balance,
        "risk": s.risk_level()
    } for s in students]
    return render_template("dashboard.html", students=students_data)

@app.route("/test-risk")
def test_risk():
    s = Student(name="Test", programme="Eng", attendance=40, gpa=1.8, fees_balance=1200)
    return s.risk_level()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the 'students' table in SQLite
    app.run(host="0.0.0.0", port=5000, debug=False)
