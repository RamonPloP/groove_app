from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired
from models.classes import Classes


class TeacherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    payment = StringField('Payment', validators=[DataRequired()])

    classes = SelectMultipleField('Classes', coerce=int)

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.classes.choices = [(cls.id, cls.name) for cls in Classes.query.all()]
