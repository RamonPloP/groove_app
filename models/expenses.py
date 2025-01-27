from db import db

class Expenses(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    expense_concept_id = db.Column(db.Integer, db.ForeignKey('expense_concepts.id'), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_types.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
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