from flask import Blueprint, render_template
from flask_login import login_required
from models.constants import SocialMediaType, BloodType, DanceReasons
from models.memberships import Memberships
from models.teachers import Teachers
from models.utils import is_admin
from models.students import Students
from datetime import datetime
from flask import request
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
        student.expire_date = student.expire_date.strftime('%Y/%m/%d')
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

@students.route('/active-members')
@is_admin
@login_required
def active_members_view():
    return render_template('home/students/actives.html')

@students.route('/active-members/get')
@is_admin
@login_required
def active_members():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        current_date = datetime.now()
        start_date = datetime(current_date.year, current_date.month, 1).date()
        end_date = current_date.date()

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    memberships = Memberships.get_all()
    info = []
    total_members = 0
    amount_total = 0

    for membership in memberships:
        active_students_query = db.session.query(Students).filter(Students.membership_id == membership.id).filter_by(
            status=1)

        active_students_query = active_students_query.filter(Students.start_date >= start_date,
                                                             Students.start_date <= end_date)

        active_students_count = active_students_query.count()

        total_members += active_students_count
        amount_total += membership.cost * active_students_count

        info.append({
            'name': membership.name,
            'actives': active_students_count,
            'total': membership.cost * active_students_count
        })

    inactive_students_count = db.session.query(Students).filter_by(status=0).filter(Students.start_date >= start_date,
                                                                                    Students.start_date <= end_date).count()

    data = [info, inactive_students_count, total_members, amount_total]

    return data
