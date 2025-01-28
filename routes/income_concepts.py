from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.income_concepts import IncomeConcepts
from controllers.incomeConceptsController import addIncomeConcept, deleteIncomeConcept
import logging

logger = logging.getLogger(__name__)

income_concepts = Blueprint('income_concepts', __name__, url_prefix='/income-concepts')

@income_concepts.route('/crud', methods=['POST'])
@is_admin
@login_required
def income_concepts_crud():
    return addIncomeConcept()

@income_concepts.route('/<id>')
@is_admin
@login_required
def find_income_concept(id):
    income_concept = IncomeConcepts.find_by_id(id)
    return render_template('home/income_concepts/modal_edit.html', income_concept=income_concept)

@income_concepts.route('/delete', methods=['POST'])
@login_required
def income_concept_delete():
    return deleteIncomeConcept()

@income_concepts.route('/all')
@is_admin
@login_required
def income_concepts_list_view():
    income_concepts = IncomeConcepts.get_all()
    return render_template('home/income_concepts/list.html', income_concepts=income_concepts)

@income_concepts.route('/list')
@is_admin
@login_required
def classes_list():
    income_concepts = IncomeConcepts.get_all()
    income_concepts = [income_concept.to_dict() for income_concept in income_concepts]
    return jsonify(income_concepts)

@income_concepts.route('/add')
@is_admin
@login_required
def income_concepts_add():
    return render_template('home/income_concepts/modal_add.html')