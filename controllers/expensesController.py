from models.expenses import Expenses
from models.expense_concepts import ExpenseConcepts
from models.teachers import Teachers
from models.payment_types import PaymentTypes
from flask import request, make_response, jsonify
from datetime import datetime
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)


def filter_expenses_by_date():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
    except ValueError as e:
        logger.error(f"Fecha inválida: {e}")
        return make_response("Fecha inválida. Usa el formato YYYY-MM-DD.", 400)

    query = db.session.query(Expenses)

    if start_date:
        query = query.filter(Expenses.date >= start_date)
    if end_date:
        query = query.filter(Expenses.date <= end_date)

    expenses = query.all()

    # Calcular el total de egresos
    total_expenses = sum(expense.amount for expense in expenses)

    # Agrupar por concepto de egreso
    expenses_by_concept = {}
    for expense in expenses:
        concept_name = expense.expense_concept
        expenses_by_concept[concept_name] = expenses_by_concept.get(concept_name, 0) + expense.amount

    # Convertir a lista para el frontend
    expenses_list = [expense.to_dict() for expense in expenses]
    for expense in expenses_list:
        expense['date'] = datetime.strftime(expense['date'], '%d/%m/%Y')

    response_data = {
        'expenses': expenses_list,
        'total_expenses': total_expenses,
        'expenses_by_concept': expenses_by_concept
    }

    return jsonify(response_data)


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