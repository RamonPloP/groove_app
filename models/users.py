from flask_login import UserMixin
from sqlalchemy.orm import validates

from db import db
from datetime import datetime
from sqlalchemy import Integer, DateTime, String, Enum
from models.translates import get_translate
from models.constants import Role


class Users(db.Model,UserMixin):

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(150),nullable=False)
    username = db.Column(String(100), index=True, unique=True)
    password = db.Column(String(255))
    role = db.Column(Enum(Role))
    status = db.Column(db.Integer,default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @validates('name', 'username', 'password')
    def empty_string_to_null(self, key, value):
        if value is not None:
            if value.isspace():
                raise ValueError(f"{get_translate(key)} no puede contener solo espacios.")
        return value


    def __init__(self,name, username, password, role, status=1):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'role': self.role.name if self.role is not None else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def get_all(cls):
        users = Users.query.order_by(Users.id.asc()).all()
        return users

    @classmethod
    def find_by_id(cls, bank_id):
        user = Users.query.filter_by(id=bank_id).first()
        return user

    @classmethod
    def changeactive(cls, id):
        user = Users.find_by_id(id)
        if user:
            user.status = 1
            db.session.commit()
            return user.status
        return None

    @classmethod
    def changeinactive(cls, id):
        user = Users.find_by_id(id)
        if user:
            user.status = 0
            db.session.commit()
            return user.status
        return None