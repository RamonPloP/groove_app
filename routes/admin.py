from flask import Blueprint, render_template
from pytz import timezone

from db import db
from datetime import datetime
from models.users import Users
from models.utils import is_admin
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/attendance-list')
@is_admin
def admin_attendance_list():
    clients = (db.session.query(Users.id, Users.name).filter(Users.role == 'SUPERVISOR').all())
    today = datetime.now(timezone('America/Chihuahua'))
    return render_template('home/admin/list.html', clients=clients, today=today)
