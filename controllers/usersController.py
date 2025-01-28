from flask import request, make_response
from werkzeug.security import generate_password_hash
from models.constants import Role
from models.users import Users
from db import db
def addUser():
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
        return make_response('Usuario registrado con exito.', 201)
    except Exception as e:
        return make_response("Error generando tu usuario, verifica la informacion", 400)

def editUsers():
    data = request.form
    user_id = data.get('user_id')
    username = data.get('username')
    name = data.get('name')
    password = generate_password_hash(data.get('password'), method='sha256')
    user = Users.query.filter_by(username=username).first()
    if user:
        return make_response('Ya hay un usuario registrado con ese correo.', 501)
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

def deleteUser():
    data = request.get_json()
    user_id = data.get('user_id')
    try:
        user = Users.find_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)