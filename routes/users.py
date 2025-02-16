from flask import Blueprint, render_template, make_response, jsonify
from flask_login import login_required, current_user
from models.utils import is_admin
from models.users import Users
from models.constants import Role
from controllers.usersController import addUser, editUsers, deleteUser
import logging

logger = logging.getLogger(__name__)
users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/changeactive/<id>', methods=['post'])
@is_admin
@login_required
def changeactive(id):
    Users.changeactive(id)
    return make_response("Hecho")

@users.route('/changeinactive/<id>', methods=['post'])
@is_admin
@login_required
def changeinactive(id):
    Users.changeinactive(id)
    return make_response("Hecho")
@users.route('/crud', methods=['POST'])
@is_admin
def users_crud():
    return addUser()

@users.route('/list')
@is_admin
@login_required
def users_list():
    users = Users.get_all()
    users = [user.to_dict() for user in users]
    return jsonify(users)

@users.route('/all')
@login_required
@is_admin
def users_index():
    model = Users.get_all()
    return render_template('home/users/list.html', users=model, current_user=current_user)

@users.route('/add')
@is_admin
@login_required
def users_add():
    return render_template('home/users/modal_add.html')

@users.route('/<id>')
@is_admin
@login_required
def find_user(id):
    user = Users.find_by_id(id)
    return render_template('home/users/modal_edit.html', user=user,role=Role, current_user=current_user)

@users.route('/edit', methods=['POST'])
@is_admin
def users_edit():
    return editUsers()

@users.route('/delete', methods=['POST'])
@login_required
def user_delete():
    return deleteUser()