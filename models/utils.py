from functools import wraps

import flask_login
from flask import render_template
from flask_login import current_user

from models.constants import Role


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(flask_login.current_user, "id") and \
                flask_login.current_user.role in [Role.ADMIN]:
            return func(*args, **kwargs)
        return render_template('home/page-401.html'), 401

    return wrapper

def is_rh(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(flask_login.current_user, "id") and flask_login.current_user.role in [
            Role.RH,
            Role.ADMIN,Role.RH_SUPERVISOR, Role.SUPER_ADMIN
        ]:
            return func(*args, **kwargs)
        return render_template('home/page-401.html'), 401
    return wrapper


def is_supervisor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(flask_login.current_user, "id") and flask_login.current_user.role in [
            Role.SUPERVISOR,Role.RH_SUPERVISOR
        ]:
            return func(*args, **kwargs)
        return render_template('home/page-401.html'), 401
    return wrapper

def is_car_inventory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(flask_login.current_user, "id") and flask_login.current_user.role in [
            Role.ADMIN, Role.SUPER_ADMIN,Role.RH,Role.CARS_INVENTORY
        ]:
            return func(*args, **kwargs)
        return render_template('home/page-401.html'), 401
    return wrapper

def is_admin_supervisor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(flask_login.current_user, "id") and flask_login.current_user.role in [Role.ADMIN_SUPERVISOR]:
            return func(*args, **kwargs)
        return render_template('home/page-401.html'), 401
    return wrapper()
