from models.income_concepts import IncomeConcepts
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

def addIncomeConcept():
    data = request.get_json()
    # get de data from request
    name = data.get('name')
    if not data.get('id'):
        income_concept = IncomeConcepts.query.filter_by(name=name).first()
        if income_concept:
            return make_response('Ya hay un concepto registrado con ese nombre.', 501)
        try:
            income_concept = IncomeConcepts(name=name)
        except ValidationError as err:
            logger.error(f"Error al guadar: {err.messages} con los datos : {data}")
            return make_response(f"Error al guadar: {err.messages} con los datos : {data}", 501)
        db.session.add(income_concept)
        db.session.commit()
        return make_response('Concepto Regitrado con exito.', 201)
    else:
        income_concept_id = data.get('id')
        income_concept = IncomeConcepts.query.filter_by(name=name).first()
        if income_concept:
            return make_response('Ya hay un concepto registrado con ese nombre.', 501)
        income_concept = IncomeConcepts.query.filter_by(id=income_concept_id).first()
        income_concept.name = name
        db.session.commit()
        return make_response('Concepto actualizado con exito.', 201)

def deleteIncomeConcept():
    data = request.get_json()
    income_concept_id = data.get('income_concept_id')
    try:
        income_concept = IncomeConcepts.find_by_id(income_concept_id)
        db.session.delete(income_concept)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)