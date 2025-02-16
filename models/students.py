from sqlalchemy import ForeignKey, Enum, desc
from datetime import datetime
from db import db

from models.constants import SocialMediaType, DanceReasons, BloodType

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    second_last_name = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    expire_date = db.Column(db.Date)
    email = db.Column(db.String(150))
    membership_id = db.Column(db.Integer, db.ForeignKey('memberships.id'), nullable=False)
    is_up_to_date = db.Column(db.Boolean, default=False, nullable=False)
    how_find_us = db.Column(Enum(SocialMediaType), nullable=False)
    dance_reason = db.Column(Enum(DanceReasons))
    regulation_pdf = db.Column(db.String(100))
    address = db.Column(db.String(250))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(100))
    nationality = db.Column(db.String(50))
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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'second_last_name': self.second_last_name,
            'start_date': self.start_date,
            'expire_date': self.expire_date,
            'email': self.email,
            'membership_id': self.membership_id,
            'membership': self.membership,
            'how_find_us': self.how_find_us,
            'how_find_us_text': self.how_find_us_text,
            'dance_reason': self.dance_reason,
            'dance_reason_text': self.dance_reason_text,
            'regulation_pdf': self.regulation_pdf,
            'address': self.address,
            'birth_date': self.birth_date,
            'birth_place': self.birth_place,
            'nationality': self.nationality,
            'blood_type': self.blood_type,
            'blood_type_text': self.blood_type_text,
            'phone': self.phone,
            'dad_name': self.dad_name,
            'dad_phone': self.dad_phone,
            'mom_name': self.mom_name,
            'mom_phone': self.mom_phone,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'has_chronic_disease': self.has_chronic_disease,
            'chronic_disease': self.chronic_disease,
            'has_allergies': self.has_allergies,
            'allergies': self.allergies,
            'has_restricted_activities': self.has_restricted_activities,
            'restricted_activities': self.restricted_activities,
            'has_mental_conditions': self.has_mental_conditions,
            'mental_conditions': self.mental_conditions,

        }

    def to_dict_expired_control(self):
        return {
            'id': self.id,
            'expire_date': self.expire_date.strftime('%d/%m/%Y'),
            'name': self.name,
            'membership_id': self.membership_id,
            'amount': self.amount
        }

    @classmethod
    def get_all(cls):
        students = Students.query.all()
        return students

    @classmethod
    def find_by_id(cls, id):
        student = Students.query.filter_by(id=id).first()
        return student

    @classmethod
    def find_by_name(cls, name):
        student = Students.query.filter_by(name=name).first()
        return student
