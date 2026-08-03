from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    programme = db.Column(db.String(100), nullable=False)
    attendance = db.Column(db.Float, default=0.0)
    gpa = db.Column(db.Float, default=0.0)
    fees_balance = db.Column(db.Float, default=0.0)

    # Risk classification method
    def risk_level(self):
        if self.gpa < 2.0 or self.attendance < 50 or self.fees_balance > 1000:
            return "High"
        elif self.gpa < 2.5 or self.attendance < 70 or self.fees_balance > 500:
            return "Medium"
        else:
            return "Low"
