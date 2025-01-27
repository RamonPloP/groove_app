from flask import Blueprint, render_template, Response, make_response, request, jsonify
from flask_login import login_required, current_user
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
@users.route('/crud', methods=['POST'])
@is_admin
def users_crud():
    try:
        data = request.form
        username = data.get('username')
        name = data.get('name')
        password = data.get('password')
        role_post = int(data.get('role'))
        role = Role(role_post)
        user = Users.query.filter_by(username=username).first()
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            return make_response('El correo ya se encuentra registrado', 400)
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = Users(name=name,username=username,password=generate_password_hash(password, method='sha256'),role=role)
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return make_response('Usuario Regitrado con exito.', 201)
    except Exception as e:
        return make_response("Error generando tu usuario, verifica la informacion", 400)

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
    data = request.form
    user_id = data.get('user_id')
    username = data.get('username')
    name = data.get('name')
    password = generate_password_hash(data.get('password'), method='sha256')
    role_post = int(data.get('role'))
    role = Role(role_post)
    user = Users.query.filter_by(id=user_id).first()
    user.name = name
    if data.get('password') is not None and data.get('password') != '':
        user.password = password
    user.username = username
    user.role = role
    db.session.commit()
    return make_response('Usuario Actualizado con exito.', 201)

@users.route('/delete', methods=['POST'])
@login_required
def user_delete():
    data = request.get_json()
    user_id = data.get('user_id')
    try:
        user = Users.find_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)