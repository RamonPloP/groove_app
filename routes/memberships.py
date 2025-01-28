from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.memberships import Memberships
from controllers.membershipsController import addMembership, deleteMembership
import logging

logger = logging.getLogger(__name__)

memberships = Blueprint('memberships', __name__, url_prefix='/memberships')

@memberships.route('/crud', methods=['POST'])
@is_admin
@login_required
def memberships_crud():
    return addMembership()

@memberships.route('/<id>')
@is_admin
@login_required
def find_membership(id):
    membership = Memberships.find_by_id(id)
    return render_template('home/memberships/modal_edit.html', membership=membership)

@memberships.route('/delete', methods=['POST'])
@login_required
def membership_delete():
    return deleteMembership()

@memberships.route('/all')
@is_admin
@login_required
def memberships_list_view():
    memberships = Memberships.get_all()
    return render_template('home/memberships/list.html', memberships=memberships)

@memberships.route('/list')
@is_admin
@login_required
def classes_list():
    memberships = Memberships.get_all()
    memberships = [membership.to_dict() for membership in memberships]
    return jsonify(memberships)

@memberships.route('/add')
@is_admin
@login_required
def memberships_add():
    return render_template('home/memberships/modal_add.html')