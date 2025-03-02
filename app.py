from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from db import db
from config import Config
from models.users import Users
from auth import auth as auth_blueprint
from main import main as main_blueprint
from models.template_filters import birth_date_years, status, vacations, seniority, _jinja2_strftime, vacation_status, month_to_text
from routes.admin import admin as admin_blueprint
from routes.users import users as users_blueprint
from routes.classes import classes as classes_blueprint
from routes.income_concepts import income_concepts as income_concepts_blueprint
from routes.expense_concepts import expense_concepts as expense_concepts_blueprint
from routes.payment_types import payment_types as payment_types_blueprint
from routes.memberships import memberships as memberships_blueprint
from routes.teachers import teachers as teachers_blueprint
from routes.expenses import expenses as expenses_blueprint
from routes.students import students as students_blueprint
from routes.incomes import incomes as incomes_blueprint
from routes.expirations_control import expirations_control as expirations_control_blueprint
from routes.leads import leads as leads_blueprint

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(classes_blueprint)
    app.register_blueprint(income_concepts_blueprint)
    app.register_blueprint(expense_concepts_blueprint)
    app.register_blueprint(payment_types_blueprint)
    app.register_blueprint(memberships_blueprint)
    app.register_blueprint(students_blueprint)
    app.register_blueprint(teachers_blueprint)
    app.register_blueprint(expenses_blueprint)
    app.register_blueprint(incomes_blueprint)
    app.register_blueprint(expirations_control_blueprint)
    app.register_blueprint(leads_blueprint)

    app.register_blueprint(users_blueprint)
    app.jinja_env.filters['birth_date_years'] = birth_date_years
    app.jinja_env.filters['strftime'] = _jinja2_strftime
    app.jinja_env.filters['seniority'] = seniority
    app.jinja_env.filters['vacations'] = vacations
    app.jinja_env.filters['status'] = status
    app.jinja_env.filters['vacation_status'] = vacation_status
    app.jinja_env.filters['month_to_text'] = month_to_text
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()


