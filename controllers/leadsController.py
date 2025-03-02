from models.leads import Leads
from models.constants import SocialMediaType
from flask import request, make_response
from db import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def addEditLead():
    data = request.get_json()

    if not data:
        return make_response("No se proporcionaron datos.", 400)

    lead_id = data.get('lead_id')

    if lead_id:
        lead = Leads.find_by_id(lead_id)
        if not lead:
            return make_response("Lead no encontrado.", 404)
    else:
        lead = Leads()

    try:
        # Campos del formulario
        lead.name = data.get('name')  # Nombre
        lead.assist_date = datetime.strptime(data.get('assist_date'), '%Y-%m-%d') if data.get('assist_date') else None  # Fecha de agenda
        lead.age = data.get('age')  # Edad
        lead.phone = data.get('phone')  # Teléfono
        lead.social_media_link = SocialMediaType(int(data.get('how_find_us')))  # ¿Cómo nos encontró?
        lead.sample_class = data.get('class_id')  # Clase muestra

        # Guardar en la base de datos
        if not lead_id:
            db.session.add(lead)

        db.session.commit()
        return make_response(f"Lead {'actualizado' if lead_id else 'registrado'} con éxito.", 201)

    except Exception as err:
        logger.error(f"Error al guardar lead: {err}")
        return make_response(f"Error al guardar lead: {err}", 500)


def deleteLead():
    data = request.get_json()
    lead_id = data.get('leadToDelete')
    try:
        lead = Leads.find_by_id(lead_id)
        db.session.delete(lead)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)

def addObservation():
    data = request.get_json()
    lead_id = data.get('lead_id')
    observation = data.get('observations')

    try:
        lead = Leads.find_by_id(lead_id)
        lead.observations = observation
        db.session.commit()
        return make_response('Observación agregada exitosamente', 201)
    except Exception as e:
        return make_response(str(e), 400)