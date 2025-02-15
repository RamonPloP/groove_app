from db import db
from sqlalchemy import desc

class Incomes(db.Model):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.String(50))
    description = db.Column(db.String(50))
    income_concept = db.Column(db.String(50), nullable=False)
    payment_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

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
            'member': self.member,
            'description': self.description,
            'income_concept': self.income_concept,
            'payment_type': self.payment_type,
            'date': self.date,
            'amount': self.amount
        }

    @classmethod
    def get_all(cls):
        income_concepts = Incomes.query.order_by(desc(Incomes.date)).all()
        return income_concepts

    @classmethod
    def find_by_id(cls, id):
        income_concepts = Incomes.query.filter_by(id=id).first()
        return income_concepts

    @classmethod
    def find_by_name(cls, name):
        income_concepts = Incomes.query.filter_by(name=name).first()
        return income_concepts