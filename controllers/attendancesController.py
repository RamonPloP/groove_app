from models.students import Students
from models.attendances import Attendances
import pytz
from datetime import datetime
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

def addAttendance():
    data = request.get_json()
    try:
        barcode = data.get('barcode')
        member = Students.find_by_barcode(barcode)
        if member:
            tz = pytz.timezone('America/Chihuahua')
            today = datetime.now(tz).date()
            attendance = Attendances(
                member_id = member.id,
                date = today
            )
            db.session.add(attendance)
            db.session.commit()
        else:
            return make_response('No hay ningun miembro con este código de barras', 501)
    except ValidationError as err:
        logger.error(f"Error al guadar: {err.messages} con los datos : {data}")
        return make_response(f"Error al guadar: {err.messages} con los datos : {data}", 501)
    return make_response(f'✅ Asistencia registrada con exito para {member.name} {member.last_name} {member.second_last_name}', 201)

def deleteAttendance():
    data = request.get_json()
    attendance_id = data.get('attendance_id')
    try:
        attendance = Attendances.find_by_id(attendance_id)
        db.session.delete(attendance)
        db.session.commit()
        return make_response('Borrado de asistencia existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)