from db import db

class IncomeConcepts(db.Model):
    __tablename__ = 'income_concepts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

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
            'name': self.name
        }

    @classmethod
    def get_all(cls):
        income_concepts = IncomeConcepts.query.order_by(IncomeConcepts.id.asc()).all()
        return income_concepts

    @classmethod
    def find_by_id(cls, id):
        income_concept = IncomeConcepts.query.filter_by(id=id).first()
        return income_concept

    @classmethod
    def find_by_name(cls, name):
        income_concept = IncomeConcepts.query.filter_by(name=name).first()
        return income_concept