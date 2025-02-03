from models.classes import Classes
from models.teachers import Teachers, teachers_classes
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
    teachers_with_class = (db.session.query(Teachers)
                           .join(teachers_classes, teachers_classes.c.teacher_id == Teachers.id)
                           .filter(teachers_classes.c.class_id == class_id)
                           .all())

    if teachers_with_class:
        response = 'Aun hay maestros que imparten esta clase: '
        for teacher in teachers_with_class:
            response += teacher.name + ', '

        response += ' desvincule esta clase de los profesores para poder eliminarla.'
        return make_response(response,500)
    try:
        clase = Classes.find_by_id(class_id)
        db.session.delete(clase)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)