from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.students import Students
from models.teachers import Teachers
from models.utils import is_admin
from models.income_concepts import IncomeConcepts
from models.incomes import Incomes
from models.payment_types import PaymentTypes
from db import db
from controllers.incomesController import addEditIncome, deleteIncome
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

incomes = Blueprint('incomes', __name__, url_prefix='/incomes')

@incomes.route('/crud', methods=['POST'])
@is_admin
@login_required
def incomes_crud():
    return addEditIncome()

@incomes.route('/<id>')
@is_admin
@login_required
def find_income_concept(id):
    income_concept = Incomes.find_by_id(id)
    return render_template('home/incomes/modal_edit.html', income_concept=income_concept)

@incomes.route('/delete', methods=['POST'])
@login_required
def income_concept_delete():
    return deleteIncome()

@incomes.route('/all')
@is_admin
@login_required
def incomes_list_view():
    incomes = Incomes.get_all()
    return render_template('home/incomes/list.html', incomes=incomes)

@incomes.route('/list')
@is_admin
@login_required
def classes_list():
    incomes = Incomes.get_all()
    incomes = [income_concept.to_dict() for income_concept in incomes]
    for income in incomes:
        income['date'] = datetime.strftime(income['date'], '%d/%m/%Y')
    return jsonify(incomes)

@incomes.route('/add')
@is_admin
@login_required
def incomes_add():
    concepts = db.session.query(IncomeConcepts).all()
    payment_types = db.session.query(PaymentTypes).all()
    members = db.session.query(Students).filter(Students.is_up_to_date == 0).all()
    return render_template('home/incomes/modal_add.html', concepts=concepts, payment_types=payment_types, members=members)