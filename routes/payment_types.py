from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.payment_types import PaymentTypes
from controllers.paymentTypesController import addPaymentType, deletePaymentType
import logging

logger = logging.getLogger(__name__)

payment_types = Blueprint('payment_types', __name__, url_prefix='/payment-types')

@payment_types.route('/crud', methods=['POST'])
@is_admin
@login_required
def payment_types_crud():
    return addPaymentType()

@payment_types.route('/<id>')
@is_admin
@login_required
def find_payment_type(id):
    payment_type = PaymentTypes.find_by_id(id)
    return render_template('home/payment_types/modal_edit.html', payment_type=payment_type)

@payment_types.route('/delete', methods=['POST'])
@login_required
def payment_type_delete():
    return deletePaymentType()

@payment_types.route('/all')
@is_admin
@login_required
def payment_types_list_view():
    payment_types = PaymentTypes.get_all()
    return render_template('home/payment_types/list.html', payment_types=payment_types)

@payment_types.route('/list')
@is_admin
@login_required
def classes_list():
    payment_types = PaymentTypes.get_all()
    payment_types = [payment_type.to_dict() for payment_type in payment_types]
    return jsonify(payment_types)

@payment_types.route('/add')
@is_admin
@login_required
def payment_types_add():
    return render_template('home/payment_types/modal_add.html')