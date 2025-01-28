from models.classes import Classes
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

def addClass():
    data = request.get_json()
    # get de data from request
    name = data.get('name')
    if not data.get('id'):
        clase = Classes.query.filter_by(name=name).first()
        if clase:
            return make_response('Ya hay una clase registrada con ese nombre.', 501)
        try:
            clase = Classes(name=name)
        except ValidationError as err:
            logger.error(f"Error al guadar: {err.messages} con los datos : {data}")
            return make_response(f"Error al guadar: {err.messages} con los datos : {data}", 501)
        db.session.add(clase)
        db.session.commit()
        return make_response('Clase registrada con exito.', 201)
    else:
        class_id = data.get('id')
        clase = Classes.query.filter_by(name=name).first()
        if clase:
            return make_response('Ya hay una clase registrada con ese nombre.', 501)
        clase = Classes.query.filter_by(id=class_id).first()
        clase.name = name
        db.session.commit()
        return make_response('Clase actualizada con exito.', 201)

def deleteClass():
    data = request.get_json()
    class_id = data.get('class_id')
    try:
        clase = Classes.find_by_id(class_id)
        db.session.delete(clase)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)