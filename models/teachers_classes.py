#from db import db


#class TeachersClasses(db.Model):
#    __tablename__ = 'teachers_classes'
#    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), primary_key=True)
#    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)

#    teacher = db.relationship('Teachers', backref=db.backref('teacher_classes', lazy=True))
#    class_ = db.relationship('Classes', backref=db.backref('class_teachers', lazy=True))

#    @classmethod
#    def find_by_teacher(cls, teacher_id):
#        return TeachersClasses.query.filter_by(teacher_id=teacher_id).all()