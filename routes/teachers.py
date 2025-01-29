from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.teachers import Teachers
from controllers.teachersController import addTeacher, deleteTeacher
import logging

logger = logging.getLogger(__name__)

teachers = Blueprint('teachers', __name__, url_prefix='/teachers')

@teachers.route('/crud', methods=['POST'])
@is_admin
@login_required
def teachers_crud():
    return addTeacher()

@teachers.route('/<id>')
@is_admin
@login_required
def find_teacher(id):
    teacher = Teachers.find_by_id(id)

    teacher_classes = [
        {'id': cls.id, 'name': cls.name} for cls in teacher.classes
    ]

    return render_template('home/teachers/modal_edit.html', teacher=teacher,teacher_classes=teacher_classes)

@teachers.route('/delete', methods=['POST'])
@login_required
def teacher_delete():
    return deleteTeacher()

@teachers.route('/all')
@is_admin
@login_required
def teachers_list_view():
    teachers = Teachers.get_all()
    return render_template('home/teachers/list.html', teachers=teachers)

@teachers.route('/list')
@is_admin
@login_required
def classes_list():
    teachers = Teachers.get_all()
    teachers = [teacher.to_dict() for teacher in teachers]
    return jsonify(teachers)

@teachers.route('/add')
@is_admin
@login_required
def teachers_add():
    return render_template('home/teachers/modal_add.html')