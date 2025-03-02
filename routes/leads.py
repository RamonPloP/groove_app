from flask import Blueprint, render_template
from flask_login import login_required
from models.classes import Classes
from models.utils import is_admin
from models.leads import Leads
from db import db
from controllers.leadsController import addEditLead, deleteLead, addObservation
import logging

logger = logging.getLogger(__name__)

leads = Blueprint('leads', __name__, url_prefix='/leads')

@leads.route('/crud', methods=['POST'])
@is_admin
@login_required
def leads_crud():
    return addEditLead()

@leads.route('/<id>')
@is_admin
@login_required
def find_lead(id):
    classes = db.session.query(Classes).all()
    lead = Leads.find_by_id(id)
    return render_template('home/leads/modal_edit.html', lead=lead, classes=classes)

@leads.route('/delete', methods=['POST'])
@login_required
def lead_delete():
    return deleteLead()

@leads.route('/all')
@is_admin
@login_required
def leads_list_view():
    leads = Leads.get_all()
    return render_template('home/leads/list.html', leads=leads)

@leads.route('/add/observation/<id>')
@is_admin
@login_required
def leads_observations_view(id):
    lead = Leads.find_by_id(id)
    return render_template('home/leads/modal_add_observations.html', lead=lead)

@leads.route('/add/observation', methods=['POST'])
@is_admin
@login_required
def leads_observations_add():
    return addObservation()

@leads.route('/list')
@is_admin
@login_required
def leads_list():
    leads = Leads.get_all()
    leads = [lead.to_dict() for lead in leads]
    return leads

@leads.route('/add')
@is_admin
@login_required
def leads_add():
    classes = db.session.query(Classes).all()
    return render_template('home/leads/modal_add.html', classes=classes)
