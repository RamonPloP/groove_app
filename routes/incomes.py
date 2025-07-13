from flask import Blueprint, render_template, jsonify
from flask_login import login_required

from models.memberships import Memberships
from models.students import Students
from models.utils import is_admin
from models.income_concepts import IncomeConcepts
from models.incomes import Incomes
from models.payment_types import PaymentTypes
from db import db
from controllers.incomesController import addEditIncome, deleteIncome, filter_incomes_by_date
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

incomes = Blueprint('incomes', __name__, url_prefix='/incomes')

@incomes.route('/crud', methods=['POST'])
@login_required
def incomes_crud():
    return addEditIncome()

@incomes.route('/<id>')
@login_required
def edit_income(id):
    income = Incomes.find_by_id(id)
    concepts = db.session.query(IncomeConcepts).all()
    payment_types = db.session.query(PaymentTypes).all()
    members = Students.get_all_actives()
    return render_template('home/incomes/modal_edit.html', income=income, concepts=concepts, payment_types=payment_types, members=members)

@incomes.route('/delete', methods=['POST'])
@login_required
def income_concept_delete():
    return deleteIncome()

@incomes.route('/all')
@login_required
def incomes_list_view():
    incomes = Incomes.get_all()
    return render_template('home/incomes/list.html', incomes=incomes)

@incomes.route('/list')
@login_required
def classes_list():
    return filter_incomes_by_date()

@incomes.route('/add')
@login_required
def incomes_add():
    concepts = db.session.query(IncomeConcepts).all()
    payment_types = db.session.query(PaymentTypes).all()
    members = Students.get_all_actives()
    return render_template('home/incomes/modal_add.html', concepts=concepts, payment_types=payment_types, members=members)