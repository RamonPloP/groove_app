from models.expenses import Expenses
from models.expense_concepts import ExpenseConcepts
from models.teachers import Teachers
from models.payment_types import PaymentTypes
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)


def addEditExpense():
    data = request.get_json()
    date = data.get('date')
    concept = ExpenseConcepts.find_by_id(data.get('concept')).name
    description = data.get('desc') if data.get('desc') else None
    staff = data.get('staff')
    if staff:
        if staff != 'other':
            staff = Teachers.find_by_id(staff).name
            description = staff
    payment_type = PaymentTypes.find_by_id(data.get('payment')).name
    total = data.get('total')

    if not data.get('id'):
        if concept == 8:
            expense = Expenses(date=date, expense_concept=concept, description=description,
                               payment_type=payment_type, amount=total)
        elif concept == 7:
            expense = Expenses(date=date, expense_concept=concept, description=staff, payment_type=payment_type,
                               amount=total)
        else:
            expense = Expenses(date=date, expense_concept=concept, description=description, payment_type=payment_type,
                               amount=total)

        try:
            db.session.add(expense)
            db.session.commit()
            return make_response('Egreso registrado con éxito.', 201)
        except ValidationError as err:
            logger.error(f"Error al guardar: {err.messages} con los datos : {data}")
            return make_response(f"Error al guardar: {err.messages} con los datos : {data}", 501)

    else:
        expense_id = data.get('id')
        expense = Expenses.query.filter_by(id=expense_id).first()

        if not expense:
            return make_response('Egreso no encontrado.', 404)

        expense.date = date
        expense.expense_concept_id = concept
        expense.payment_type_id = payment_type
        expense.amount = total

        # Si el concepto es 8, actualizamos 'description'; si es 7, actualizamos con el valor de 'staff'
        if concept == 8:
            expense.description = description
        elif concept == 7:
            expense.description = staff

        try:
            db.session.commit()
            return make_response('Egreso actualizado con éxito.', 201)
        except ValidationError as err:
            logger.error(f"Error al actualizar: {err.messages} con los datos : {data}")
            return make_response(f"Error al actualizar: {err.messages} con los datos : {data}", 501)


def deleteExpense():
    data = request.get_json()
    expense_concept_id = data.get('expense_concept_id')
    try:
        expense_concept = Expenses.find_by_id(expense_concept_id)
        db.session.delete(expense_concept)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)