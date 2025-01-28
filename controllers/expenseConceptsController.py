from models.expense_concepts import ExpenseConcepts
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

def addExpenseConcept():
    data = request.get_json()
    # get de data from request
    name = data.get('name')
    if not data.get('id'):
        expense_concept = ExpenseConcepts.query.filter_by(name=name).first()
        if expense_concept:
            return make_response('Ya hay un concepto registrado con ese nombre.', 501)
        try:
            expense_concept = ExpenseConcepts(name=name)
        except ValidationError as err:
            logger.error(f"Error al guadar banco: {err.messages} con los datos : {data}")
        db.session.add(expense_concept)
        db.session.commit()
        return make_response('Concepto Regitrado con exito.', 201)
    else:
        expense_concept_id = data.get('id')
        expense_concept = ExpenseConcepts.query.filter_by(id=expense_concept_id).first()
        expense_concept.name = name
        db.session.commit()
        return make_response('Clase actualizada con exito.', 201)

def deleteExpenseConcept():
    data = request.get_json()
    expense_concept_id = data.get('expense_concept_id')
    try:
        expense_concept = ExpenseConcepts.find_by_id(expense_concept_id)
        db.session.delete(expense_concept)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)