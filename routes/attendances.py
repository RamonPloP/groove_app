from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.attendances import Attendances
from controllers.attendancesController import addAttendance, deleteAttendance
import logging

logger = logging.getLogger(__name__)

attendances = Blueprint('attendances', __name__, url_prefix='/attendances')

@attendances.route('/crud', methods=['POST'])
@is_admin
@login_required
def attendances_crud():
    return addAttendance()

@attendances.route('/<id>')
@is_admin
@login_required
def find_class(id):
    attendance = Attendances.find_by_id(id)
    return render_template('home/classes/modal_edit.html', attendance=attendance)

@attendances.route('/delete', methods=['POST'])
@login_required
def attendance_delete():
    return deleteAttendance()

@attendances.route('/all')
@is_admin
@login_required
def attendances_list_view():
    attendances = Attendances.get_all()
    return render_template('home/attendances/list.html', attendances=attendances)

@attendances.route('/list')
@is_admin
@login_required
def attendances_list():
    attendances = Attendances.get_all()
    attendances = [attendance.to_dict() for attendance in attendances]
    return jsonify(attendances)

@attendances.route('/members-add')
@login_required
@is_admin
def attendances_add():
    return render_template('home/attendances/dashboard.html')

