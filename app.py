from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
from databaseOJ import db, Student
from routes import student_bp
from config import Config

migrate = Migrate()


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)
    app.config.setdefault("INITIALIZE_DATABASE", False)

    # Bind db and migration support to this app
    db.init_app(app)
    migrate.init_app(app, db)

    @app.before_first_request
    def run_migrations():
        if app.testing:
            return

        try:
            upgrade()
            app.logger.info("Database migration applied successfully.")
        except Exception as exc:
            app.logger.warning("Database migration failed: %s", exc)

    def initialize_database():
        """Create the database tables if the database is reachable."""
        if app.testing:
            return

        try:
            with app.app_context():
                db.create_all()
        except Exception as exc:
            app.logger.warning("Database initialization skipped: %s", exc)

    app.initialize_database = initialize_database

    # Register routes
    app.register_blueprint(student_bp, url_prefix="/students")

    @app.route("/")
    def home():
        return "Student Risk Tracking System is running!"

    # Dashboard route
    @app.route("/dashboard")
    def dashboard():
        try:
            students = Student.query.all()
        except Exception as exc:
            app.logger.warning("Unable to load students from the database: %s", exc)
            students = []

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

    # Run initialization without breaking app startup if MySQL is unavailable.
    if app.config.get("INITIALIZE_DATABASE"):
        initialize_database()
    return app


app = create_app()


def initialize_database():
    return app.initialize_database()


if __name__ == "__main__":
    app.config["INITIALIZE_DATABASE"] = True
    app.initialize_database()
    app.run(host="0.0.0.0", debug=True)
