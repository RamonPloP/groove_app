from db import db
from models.students import Students

class Attendances(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    date = db.Column(db.Date)

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
        member = Students.find_by_id(self.member_id)
        return {
            'id': self.id,
            'member': str(member.id) + ' | ' + member.name + ' ' + member.last_name + ' ' + member.second_last_name,
            'date': self.date.strftime('%d/%m/%Y')
        }

    @classmethod
    def get_all(cls):
        classes = Attendances.query.order_by(Attendances.id.asc()).all()
        return classes

    @classmethod
    def find_by_id(cls, attendance_id):
        attendance = Attendances.query.filter_by(id=attendance_id).first()
        return attendance