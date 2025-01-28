from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.expense_concepts import ExpenseConcepts
from controllers.expenseConceptsController import addExpenseConcept, deleteExpenseConcept
import logging

logger = logging.getLogger(__name__)

expense_concepts = Blueprint('expense_concepts', __name__, url_prefix='/expense-concepts')

@expense_concepts.route('/crud', methods=['POST'])
@is_admin
@login_required
def expense_concepts_crud():
    return addExpenseConcept()

@expense_concepts.route('/<id>')
@is_admin
@login_required
def find_expense_concept(id):
    expense_concept = ExpenseConcepts.find_by_id(id)
    return render_template('home/expense_concepts/modal_edit.html', expense_concept=expense_concept)

@expense_concepts.route('/delete', methods=['POST'])
@login_required
def expense_concept_delete():
    return deleteExpenseConcept()

@expense_concepts.route('/all')
@is_admin
@login_required
def expense_concepts_list_view():
    expense_concepts = ExpenseConcepts.get_all()
    return render_template('home/expense_concepts/list.html', expense_concepts=expense_concepts)

@expense_concepts.route('/list')
@is_admin
@login_required
def classes_list():
    expense_concepts = ExpenseConcepts.get_all()
    expense_concepts = [expense_concept.to_dict() for expense_concept in expense_concepts]
    return jsonify(expense_concepts)

@expense_concepts.route('/add')
@is_admin
@login_required
def expense_concepts_add():
    return render_template('home/expense_concepts/modal_add.html')