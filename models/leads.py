from db import db
from models.constants import SocialMediaType
from models.classes import Classes
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
    observations = db.Column(db.String(30))

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
        sample_class = Classes.find_by_id(self.sample_class).name
        social_media = SocialMediaType(self.social_media_link).name
        return {
            'id': self.id,
            'assist_date': self.assist_date.strftime('%d/%m/%Y'),
            'name': self.name,
            'age': self.age,
            'phone': self.phone,
            'sample_class': sample_class,
            'social_media_link': social_media,
            'observations': self.observations,
        }

    @classmethod
    def get_all(cls):
        leads = Leads.query.all()
        return leads

    @classmethod
    def find_by_id(cls, id):
        lead = Leads.query.filter_by(id=id).first()
        return lead

    @classmethod
    def find_by_name(cls, name):
        lead = Leads.query.filter_by(name=name).first()
        return lead