from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.constants import SocialMediaType, BloodType, DanceReasons
from models.memberships import Memberships
from models.teachers import Teachers
from models.utils import is_admin
from models.students import Students
from db import db
from controllers.studentsController import addEditStudent, deleteStudent, addRegulationPDF
import logging

logger = logging.getLogger(__name__)

students = Blueprint('students', __name__, url_prefix='/students')

@students.route('/crud', methods=['POST'])
@is_admin
@login_required
def students_crud():
    return addEditStudent()

@students.route('/<id>')
@is_admin
@login_required
def find_student_concept(id):
    memberships = db.session.query(Memberships).all()
    teachers = db.session.query(Teachers).all()
    student = Students.find_by_id(id)
    return render_template('home/students/modal_edit.html', member=student, memberships=memberships, teachers=teachers)

@students.route('/delete', methods=['POST'])
@login_required
def student_concept_delete():
    return deleteStudent()

@students.route('/all')
@is_admin
@login_required
def students_list_view():
    students = Students.get_all()
    return render_template('home/students/list.html', students=students)

@students.route('/list')
@is_admin
@login_required
def students_list():
    students = Students.get_all()
    for student in students:
        student.start_date = student.start_date.strftime('%Y/%m/%d')
        student.birth_date = student.birth_date.strftime('%Y/%m/%d')
        student.membership = Memberships.find_by_id(student.membership_id).name
        student.how_find_us_text = SocialMediaType(int(student.how_find_us)).name
        student.blood_type_text = str(BloodType(int(student.blood_type)))
        student.dance_reason_text = str(DanceReasons(int(student.dance_reason)))
    students = [student.to_dict() for student in students]
    return students

@students.route('/add')
@is_admin
@login_required
def students_add():
    memberships = db.session.query(Memberships).all()
    teachers = db.session.query(Teachers).all()
    return render_template('home/students/modal_add.html', teachers=teachers, memberships=memberships)

@students.route('/modal/regulation-pdf/<id>')
@is_admin
@login_required
def students_add_regulation_pdf_modal(id):
    student = Students.find_by_id(id)
    return render_template('home/students/modal_add_regulation.html', student=student)

@students.route('/add/regulation-pdf', methods=['POST'])
@is_admin
@login_required
def students_add_regulation_pdf():
    return addRegulationPDF()