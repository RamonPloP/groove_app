from sqlalchemy import ForeignKey, Enum
from db import db
from models.constants import SocialMediaType, DanceReasons, BloodType

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    email = db.Column(db.String(150))
    membership_id = db.Column(db.Integer, db.ForeignKey('memberships.id'), nullable=False)
    how_find_us = db.Column(Enum(SocialMediaType), nullable=False)
    dance_reason = db.Column(Enum(DanceReasons))
    regulation_pdf = db.Column(db.String(100))
    address = db.Column(db.String(250))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(100))
    nacionality = db.Column(db.String(50))
    blood_type = db.Column(Enum(BloodType), nullable=False)
    phone = db.Column(db.String(20))
    dad_name = db.Column(db.String(50))
    dad_phone = db.Column(db.String(20))
    mom_name = db.Column(db.String(50))
    mom_phone = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(50))
    emergency_contact_phone = db.Column(db.String(20))
    has_chronic_disease = db.Column(db.Boolean, nullable=False)
    chronic_disease = db.Column(db.String(50))
    has_allergies = db.Column(db.Boolean, nullable=False)
    allergies = db.Column(db.String(50))
    has_restricted_activities = db.Column(db.Boolean, nullable=False)
    restricted_activities = db.Column(db.String(50))
    has_mental_conditions = db.Column(db.Boolean, nullable=False)
    mental_conditions = db.Column(db.String(50))

    def __init__(self, **kwargs):
        for prop, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, prop, value)

    @classmethod
    def get_all(cls):
        students = Students.query.order_by(
            Students.id.asc())
        students.all()
        return students

    @classmethod
    def find_by_id(cls, student_id):
        student = Students.query.filter_by(id=student_id).first()
        return student
