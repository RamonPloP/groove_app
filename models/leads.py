from db import db
from models.constants import SocialMediaType
from sqlalchemy import Enum

class Leads(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=True)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    sample_class = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    social_media_link = db.Column(Enum(SocialMediaType), nullable=False)
    assist_date = db.Column(db.Date, nullable=False)
    observations = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        for prop, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
            setattr(self, prop, value)