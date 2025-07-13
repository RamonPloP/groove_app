from flask import Blueprint, render_template, jsonify
from flask_login import login_required

from models.payment_types import PaymentTypes
from models.teachers import Teachers
from models.utils import is_admin
from models.expense_concepts import ExpenseConcepts
from models.expenses import Expenses
from models.payment_types import PaymentTypes
from db import db
from controllers.expensesController import addEditExpense, deleteExpense, filter_expenses_by_date
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

expenses = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses.route('/crud', methods=['POST'])
@login_required
def expenses_crud():
    return addEditExpense()

@expenses.route('/<id>')
@login_required
def find_expense_concept(id):
    expense = Expenses.find_by_id(id)
    concepts = db.session.query(ExpenseConcepts).all()
    payment_types = db.session.query(PaymentTypes).all()
    teachers = db.session.query(Teachers).all()
    return render_template('home/expenses/modal_edit.html', expense=expense, concepts=concepts, payment_types=payment_types, teachers=teachers)

@expenses.route('/delete', methods=['POST'])
@login_required
def expense_concept_delete():
    return deleteExpense()

@expenses.route('/all')
@login_required
def expenses_list_view():
    return render_template('home/expenses/list.html')

@expenses.route('/list')
@login_required
def classes_list():
    return filter_expenses_by_date()

@expenses.route('/add')
@login_required
def expenses_add():
    concepts = db.session.query(ExpenseConcepts).all()
    payment_types = db.session.query(PaymentTypes).all()
    teachers = db.session.query(Teachers).all()
    return render_template('home/expenses/modal_add.html', concepts=concepts, payment_types=payment_types, teachers=teachers)