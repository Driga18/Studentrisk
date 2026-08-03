from app import app
from databaseOJ import db, Student

with app.app_context():
    existing = Student.query.filter_by(name='Tanatswa Moyo').first()
    if not existing:
        student = Student(
            name='Tanatswa Moyo',
            programme='Computer Science',
            attendance=88,
            gpa=3.2,
            fees_balance=150,
        )
        db.session.add(student)
        db.session.commit()
        print('SAMPLE_STUDENT_ADDED')
    else:
        print('SAMPLE_STUDENT_EXISTS')
