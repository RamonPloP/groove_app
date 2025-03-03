from models.incomes import Incomes
from models.income_concepts import IncomeConcepts
from sqlalchemy.exc import IntegrityError
from models.payment_types import PaymentTypes
from models.students import Students
from flask import request, make_response, jsonify
from models.memberships import Memberships
from db import db
from marshmallow import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def filter_incomes_by_date():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
    except ValueError as e:
        logger.error(f"Fecha inválida: {e}")
        return make_response("Fecha inválida. Usa el formato YYYY-MM-DD.", 400)

    query = db.session.query(Incomes)

    if start_date:
        query = query.filter(Incomes.date >= start_date)
    if end_date:
        query = query.filter(Incomes.date <= end_date)

    incomes = query.all()

    # Calcular el total de ingresos
    total_incomes = sum(income.amount for income in incomes)

    # Agrupar por concepto de ingreso
    incomes_by_concept = {}
    for income in incomes:
        concept_name = income.income_concept
        incomes_by_concept[concept_name] = incomes_by_concept.get(concept_name, 0) + income.amount

    # Convertir a lista para el frontend
    incomes_list = [income.to_dict() for income in incomes]

    for income in incomes_list:
        income['date'] = datetime.strftime(income['date'], '%d/%m/%Y')

    # Formatear los datos de la gráfica
    chart_data = []
    for concept, total in incomes_by_concept.items():
        chart_data.append({'concept': concept, 'total': total})

    response_data = {
        'incomes': incomes_list,
        'total_incomes': total_incomes,
        'incomes_by_concept': incomes_by_concept,
        'chart_data': chart_data  # Incluye los datos de la gráfica
    }

    return jsonify(response_data)

def addEditIncome():
    data = request.get_json()
    date = data.get('date')
    if data.get('concept') != 'other':
        concept_id = int(data.get('concept'))
        concept = IncomeConcepts.find_by_id(concept_id).name if concept_id else None
    else:
        concept_id = 'Otro'
        concept = 'Otro'

    member = int(data.get('member')) if data.get('member') else None
    if concept_id in [4, 5]:
        member = Students.find_by_id(int(data.get('member')))
        member.is_up_to_date = True
        member.expire_date = member.expire_date + relativedelta(months=1)
        try:
            db.session.add(member)
            db.session.commit()
        except ValidationError as err:
            logger.error(f"Error al guardar: {err.messages} con los datos : {data}")
            return make_response(f"Error al guardar: {err.messages} con los datos : {data}", 501)

        member = Students.find_by_id(int(data.get('member'))).name

    description = data.get('desc') if concept_id in [8, 9] or concept_id == "Otro" else None

    payment_type = PaymentTypes.find_by_id(data.get('payment')).name
    total = data.get('total')
    if concept_id == 4:
        member_ = Students.find_by_id(int(data.get('member'))).membership_id
        total = int(Memberships.find_by_id(member_).cost)

    if not data.get('id'):
        income = Incomes(
            date=date,
            income_concept=concept,
            description=description,
            payment_type=payment_type,
            amount=total,
            member=member
        )

        try:
            db.session.add(income)
            db.session.commit()
            return make_response('Ingreso registrado con éxito.', 201)
        except ValidationError as err:
            logger.error(f"Error al guardar: {err.messages} con los datos : {data}")
            return make_response(f"Error al guardar: {err.messages} con los datos : {data}", 501)
        except IntegrityError:
            db.session.rollback()
            return make_response("Error de integridad en la base de datos.", 500)

    else:  # Actualizar ingreso
        income_id = data.get('id')
        income = Incomes.query.filter_by(id=income_id).first()

        if not income:
            return make_response('Ingreso no encontrado.', 404)

        income.date = date
        income.income_concept_id = concept
        income.payment_type_id = payment_type
        income.amount = total
        income.member_id = member  # Se actualiza solo si el concepto lo requiere

        # Si el concepto es 8, 9 o "other", actualizamos 'description'
        if concept_id in [8, 9] or concept_id == "other":
            income.description = description

        try:
            db.session.commit()
            return make_response('Ingreso actualizado con éxito.', 201)
        except ValidationError as err:
            logger.error(f"Error al actualizar: {err.messages} con los datos : {data}")
            return make_response(f"Error al actualizar: {err.messages} con los datos : {data}", 501)
        except IntegrityError:
            db.session.rollback()
            return make_response("Error de integridad en la base de datos.", 500)



def deleteIncome():
    data = request.get_json()
    income_concept_id = data.get('income_concept_id')
    try:
        income_concept = Incomes.find_by_id(income_concept_id)
        db.session.delete(income_concept)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)