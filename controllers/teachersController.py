from models.teachers import Teachers
from models.classes import Classes
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

def addTeacher():
    data = request.get_json()

    # Obtener los datos del request
    name = data.get('name')
    phone = data.get('phone')
    payment = int(data.get('payment'))  # Asegúrate de que la clave es 'payment'
    class_ids = data.get('classes', [])  # Asegúrate de que es una lista de IDs de clases

    if not data.get('id'):  # Si no se especifica un ID, estamos creando un nuevo profesor
        # Verificar si ya existe un profesor con el mismo nombre
        teacher = Teachers.query.filter_by(name=name).first()
        if teacher:
            return make_response('Ya hay un profesor registrado con ese nombre.', 501)

        try:
            # Crear el nuevo objeto Teacher
            teacher = Teachers(name=name, phone=phone, payment=payment)

            # Relacionar clases si se proporcionaron
            if class_ids:
                # Obtener las clases asociadas por ID
                classes = Classes.query.filter(Classes.id.in_(class_ids)).all()
                teacher.classes = classes  # Asignar clases al profesor

            db.session.add(teacher)
            db.session.commit()
            return make_response('Profesor registrado con éxito.', 201)

        except Exception as err:
            # Manejar errores en la base de datos
            return make_response(f"Error al guardar el profesor: {str(err)}", 500)

    else:  # Si el ID está presente, estamos actualizando un profesor existente
        teacher_id = data.get('id')
        teacher = Teachers.query.filter_by(id=teacher_id).first()
        if not teacher:
            return make_response('Profesor no encontrado.', 404)

        # Verificar si ya hay otro profesor con el mismo nombre (excepto el mismo)
        existing_teacher = Teachers.query.filter(Teachers.name == name, Teachers.id != int(data.get('id'))).first()
        if existing_teacher:
            return make_response('Ya hay un profesor registrado con ese nombre.', 501)

        # Actualizar los campos del profesor
        teacher.name = name
        teacher.phone = phone
        teacher.payment = payment

        # Relacionar clases si se proporcionaron
        if class_ids:
            # Obtener las clases asociadas por ID
            classes = Classes.query.filter(Classes.id.in_(class_ids)).all()
            teacher.classes = classes  # Actualizar las clases del profesor

        db.session.commit()
        return make_response('Profesor actualizado con éxito.', 201)


def deleteTeacher():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    try:
        teacher = Teachers.find_by_id(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)