from db import db
from sqlalchemy import desc

class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    expense_concept = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))
    payment_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

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
            'date': self.date,
            'expense_concept': self.expense_concept,
            'description': self.description,
            'payment_type': self.payment_type,
            'amount': self.amount
        }

    @classmethod
    def get_all(cls):
        expense_concepts = Expenses.query.order_by(desc(Expenses.date)).all()
        return expense_concepts

    @classmethod
    def find_by_id(cls, id):
        expense_concept = Expenses.query.filter_by(id=id).first()
        return expense_concept

    @classmethod
    def find_by_name(cls, name):
        expense_concept = Expenses.query.filter_by(name=name).first()
        return expense_concept