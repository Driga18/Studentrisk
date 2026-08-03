from flask import Blueprint, request, jsonify
from databaseOJ import db, Student   # import db and Student from models.py
# Define the blueprint
student_bp = Blueprint("students", __name__)

# CREATE
@student_bp.route("/", methods=["POST"])
def add_student():
    data = request.json
    student = Student(
        name=data["name"],
        programme=data.get("programme"),
        attendance=data.get("attendance", 0.0),
        gpa=data.get("gpa", 0.0),
        fees_balance=data.get("fees_balance", 0.0)
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

# READ
@student_bp.route("/", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "programme": s.programme,
        "attendance": s.attendance,
        "gpa": s.gpa,
        "fees_balance": s.fees_balance,
        "risk": s.risk_level()
    } for s in students])

@student_bp.route("/<int:id>", methods=["GET"])
def get_student(id):
    s = Student.query.get_or_404(id)
    return jsonify({
        "id": s.id,
        "name": s.name,
        "programme": s.programme,
        "attendance": s.attendance,
        "gpa": s.gpa,
        "fees_balance": s.fees_balance,
        "risk": s.risk_level()
    })

# UPDATE
@student_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    student.name = data.get("name", student.name)
    student.programme = data.get("programme", student.programme)
    student.attendance = data.get("attendance", student.attendance)
    student.gpa = data.get("gpa", student.gpa)
    student.fees_balance = data.get("fees_balance", student.fees_balance)
    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

# DELETE
@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})

