import pytest

from app import app
from databaseOJ import db, Student


@pytest.fixture()
def client(tmp_path):
    database_path = tmp_path / "test_student_risk.db"
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()


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
