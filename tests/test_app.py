import importlib
import runpy
from pathlib import Path

import pytest

from config import Config
from databaseOJ import db, Student
from app import create_app


@pytest.fixture()
def client(tmp_path):
    database_path = tmp_path / "test_student_risk.db"
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
        INITIALIZE_DATABASE=False,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_default_database_is_mysql():
    assert Config.SQLALCHEMY_DATABASE_URI.startswith("sqlite://")


def test_config_defaults_to_supplied_mysql_password(monkeypatch):
    monkeypatch.delenv("MYSQL_PASSWORD", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("USE_SQLITE", "0")

    reloaded_config = importlib.reload(__import__("config"))

    assert "Tanatswa%401212" in reloaded_config.Config.SQLALCHEMY_DATABASE_URI


def test_copy_entrypoint_starts_without_nameerror(monkeypatch):
    monkeypatch.setattr("flask.app.Flask.run", lambda *args, **kwargs: None)

    entrypoint = Path(__file__).resolve().parent.parent / "app - Copy (2).py"
    result = runpy.run_path(str(entrypoint), run_name="__main__")

    assert result["app"] is not None


def test_dashboard_loads(client):
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Student Risk Dashboard" in response.data


def test_student_crud_api(client):
    create_response = client.post(
        "/students/",
        json={
            "name": "Amina Dlamini",
            "programme": "Computer Science",
            "attendance": 82,
            "gpa": 3.1,
            "fees_balance": 0,
        },
    )
    assert create_response.status_code == 201

    students = client.get("/students/").get_json()
    assert len(students) == 1
    assert students[0]["name"] == "Amina Dlamini"
    assert students[0]["risk"] == "Low"

    student_id = students[0]["id"]
    update_response = client.put(
        f"/students/{student_id}",
        json={"attendance": 40},
    )
    assert update_response.status_code == 200
    assert client.get(f"/students/{student_id}").get_json()["risk"] == "High"

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200
    assert client.get("/students/").get_json() == []


@pytest.mark.parametrize(
    ("attendance", "gpa", "fees_balance", "expected_risk"),
    [
        (90, 3.0, 0, "Low"),
        (65, 3.0, 0, "Medium"),
        (90, 1.8, 0, "High"),
    ],
)
def test_risk_levels(attendance, gpa, fees_balance, expected_risk):
    student = Student(
        name="Test Student",
        programme="Testing",
        attendance=attendance,
        gpa=gpa,
        fees_balance=fees_balance,
    )

    assert student.risk_level() == expected_risk
