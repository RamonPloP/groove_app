from db import db

# Tabla intermedia para la relación Many-to-Many
teachers_classes = db.Table('teachers_classes',
                            db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
                            db.Column('class_id', db.Integer, db.ForeignKey('classes.id'), primary_key=True)
                            )


class Teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    payment = db.Column(db.Integer, nullable=False)

    # Relación Many-to-Many con Class
    classes = db.relationship('Classes', secondary=teachers_classes, backref=db.backref('teachers', lazy='dynamic'))

    def __init__(self, **kwargs):
        for prop, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            setattr(self, prop, value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'payment': self.payment,
            'classes': [cls.name for cls in self.classes]  # Muestra los nombres de las clases asociadas
        }

    @classmethod
    def get_all(cls):
        return Teachers.query.order_by(Teachers.id.asc()).all()

    @classmethod
    def find_by_id(cls, id):
        return Teachers.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return Teachers.query.filter_by(name=name).first()
