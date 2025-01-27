from flask import Blueprint, render_template, Response, make_response, request
from flask_login import login_required
from models.utils import is_admin
from models.users import Users
from models.constants import Role
from db import db
from werkzeug.security import generate_password_hash

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/changeactive/<id>', methods=['post'])
@is_admin
@login_required
def changeactive(id):
    Users.changeactive(id)
    return make_response("hecho")

@users.route('/changeinactive/<id>', methods=['post'])
@is_admin
@login_required
def changeinactive(id):
    Users.changeinactive(id)
    return make_response("hecho")

@users.route('/list')
@is_admin
@login_required
def users_list():
    users = Users.get_all()
    return users

@users.route('/all')
@login_required
@is_admin
def users_index():
    model = Users.get_all()
    return render_template('home/users/list.html', users=model)

