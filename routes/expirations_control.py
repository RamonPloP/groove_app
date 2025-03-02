from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy.sql import func
from models.utils import is_admin
from models.memberships import Memberships
from models.students import Students
from datetime import datetime
from pytz import timezone
import logging
from db import db

logger = logging.getLogger(__name__)

expirations_control = Blueprint('expirations', __name__, url_prefix='/expirations')

@expirations_control.route('/all')
@login_required
@is_admin
def expirations_index():
    today = datetime.now(timezone('America/Chihuahua'))
    today = datetime.strftime(today, '%d/%m/%Y')
    return render_template('home/expirations_control/list.html', today=today)

@expirations_control.route('/list/<type>')
@login_required
@is_admin
def get_expirations(type):
    today = datetime.now(timezone('America/Chihuahua')).date()

    if type == 'expired':
        expired = db.session.query(Students).filter(func.date(Students.expire_date) < today, Students.is_up_to_date == False).all()
        for expire in expired:
            expire.amount = Memberships.find_by_id(expire.membership_id).cost
        expired = [expire.to_dict_expired_control() for expire in expired]
        return expired

    elif type == 'expire_today':
        expire_today = db.session.query(Students).filter(func.date(Students.expire_date) == today, Students.is_up_to_date == False).all()
        for expire in expire_today:
            expire.amount = Memberships.find_by_id(expire.membership_id).cost
        expire_today = [expire.to_dict_expired_control() for expire in expire_today]
        return expire_today

    elif type == 'expire_future':
        expire_future = db.session.query(Students).filter(func.date(Students.expire_date) > today).all()
        for expire in expire_future:
            expire.amount = Memberships.find_by_id(expire.membership_id).cost
        expire_future = [expire_future.to_dict_expired_control() for expire_future in expire_future]
        return expire_future

    return 'Tipo invalido'
