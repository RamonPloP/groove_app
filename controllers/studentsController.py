from models.students import Students
from models.constants import SocialMediaType, DanceReasons, BloodType
from flask import request, make_response, send_file
from db import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
import hashlib
import pytz
from io import BytesIO
import barcode
from PIL import Image
from barcode.writer import ImageWriter
import os
import logging

logger = logging.getLogger(__name__)

def allowed_file_pdf(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def addEditStudent():
    data = request.get_json()

    if not data:
        return make_response("No se proporcionaron datos.", 400)

    student_id = data.get('id')

    # Si es una actualización, buscamos el estudiante existente
    if student_id:
        student = Students.find_by_id(student_id)
        if not student:
            return make_response("Estudiante no encontrado.", 404)
    else:
        student = Students()

    try:
        student.name = data.get('name')
        student.last_name = data.get('last_name')
        student.second_last_name = data.get('second_last_name')

        start_date_str = data.get('start_date')
        student.start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        student.expire_date = student.start_date + relativedelta(months=1)

        student.email = data.get('email')
        student.membership_id = data.get('membership_id')

        student.how_find_us = SocialMediaType(int(data.get('how_find_us')))

        student.dance_reason = DanceReasons(int(data.get('dance_reason')))

        student.address = data.get('address')
        student.birth_date = data.get('birth_date')
        student.birth_place = data.get('birth_place')
        student.nationality = data.get('nationality')

        if data.get('blood_type'):
            student.blood_type = BloodType(int(data.get('blood_type')))
        else:
            student.blood_type = None

        student.phone = data.get('phone')
        student.dad_name = data.get('dad_name')
        student.dad_phone = data.get('dad_phone')
        student.mom_name = data.get('mom_name')
        student.mom_phone = data.get('mom_phone')
        student.emergency_contact_name = data.get('emergency_contact_name')
        student.emergency_contact_phone = data.get('emergency_contact_phone')

        # Manejo de campos booleanos
        student.has_chronic_disease = True if data.get('has_chronic_disease') == 'true' else False
        student.chronic_disease = data.get('chronic_disease')
        student.has_allergies = True if data.get('has_allergies', False) == 'true' else False
        student.allergies = data.get('allergies')
        student.has_restricted_activities = True if data.get('has_restricted_activities', False) == 'true' else False
        student.restricted_activities = data.get('restricted_activities')
        student.has_mental_conditions = True if data.get('has_mental_conditions', False) == 'true' else False
        student.mental_conditions = data.get('mental_conditions')

        # Guardar en la base de datos
        if not student_id:
            db.session.add(student)

        db.session.commit()
        return make_response(f"Estudiante {'actualizado' if student_id else 'registrado'} con éxito.", 201)

    except Exception as err:
        logger.error(f"Error al guardar estudiante: {err}")
        return make_response(f"Error al guardar estudiante: {err}", 500)


def deleteStudent():
    data = request.get_json()
    student_id = data.get('studentToDelete')
    try:
        student = Students.find_by_id(student_id)
        student.status = 0
        student.end_date = datetime.now(pytz.timezone("America/Chihuahua"))
        db.session.commit()
        return make_response('Dado de baja existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)


def addRegulationPDF():
    UPLOAD_FOLDER = os.path.join('static', 'students_pdfs')
    item_id = request.form.get('item_id')
    try:
        item = Students.find_by_id(item_id)
        pdf = request.files['pdf']
        if pdf and allowed_file_pdf(pdf.filename):
            full_filename = os.path.join(UPLOAD_FOLDER, 'Reglamento-' + item.name + '_' + item.last_name +'.pdf')
            pdf.save(full_filename)
            item.regulation_pdf = "/" + full_filename
            db.session.commit()
            return make_response('Documento guardado con exito.', 201)
        else:
            return make_response("Formato de archivo no valido, Formato permitido solo PDF", 400)
    except Exception as e:
        return make_response(str(e), 400)

def createMemberCard(member_id):
    member = Students.find_by_id(member_id)
    if not member:
        return make_response('Miembro no encontrado.', 404)

    Code128 = barcode.get_barcode_class('code128')
    writer_options = {
        'font_size': 6,
        'text_distance': 3,
        'write_text': True,
    }

    # Determinar el contenido del código de barras
    if member.barcode:
        barcode_content = member.barcode
    else:
        # Generar un código hash si no existe
        hash_object = hashlib.sha256(str(member_id).encode())
        barcode_content = hash_object.hexdigest()[:12]
        member.barcode = barcode_content
        db.session.commit()

    # Generar el código de barras en memoria
    barcode_img = Code128(barcode_content, writer=ImageWriter())
    buffer = BytesIO()
    barcode_img.write(buffer, options=writer_options)
    buffer.seek(0)

    # Quitar fondo blanco (opcional)
    image = Image.open(buffer).convert("RGBA")
    datas = image.getdata()
    newData = []
    for item in datas:
        if item[0] > 250 and item[1] > 250 and item[2] > 250:
            newData.append((255, 255, 255, 0))  # Transparente
        else:
            newData.append(item)
    image.putdata(newData)

    # Guardar en buffer de salida final
    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    # Enviar como respuesta de archivo descargable
    return send_file(
        output_buffer,
        mimetype='image/png',
        as_attachment=True,
        download_name=f"{member.name}_{member_id}_barcode.png"
    )
