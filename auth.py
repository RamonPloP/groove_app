from flask import Blueprint, render_template, redirect, url_for, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from models.users import Users

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        if  current_user.role == 3:
            return redirect(url_for('supervisors.index'))
        return redirect(url_for('main.dashboard'))
    return render_template('/login/login.html')

@auth.route('/loginp', methods=['POST'])
def login_post():
    # login code goes here
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    remember = True if data.get('remember') else False
    user = Users.query.filter_by(username=username).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        # flash('Please check your login details and try again.')
        return make_response('Usuario o contraseña incorrectos.', 301)
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return make_response('Inicio exitoso.', 201)



@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    username = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = Users.query.filter_by(
        username=username).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = Users(username=username,name= name,password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))