from models.memberships import Memberships
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

def addMembership():
    data = request.get_json()
    # get de data from request
    name = data.get('name')
    cost = int(data.get('cost'))
    if not data.get('id'):
        membership = Memberships.query.filter_by(name=name).first()
        if membership:
            return make_response('Ya hay una membresía registrada con ese nombre.', 501)
        try:
            membership = Memberships(name=name,cost=cost)
        except ValidationError as err:
            logger.error(f"Error al guadar: {err.messages} con los datos : {data}")
            return make_response(f"Error al guadar: {err.messages} con los datos : {data}", 501)
        db.session.add(membership)
        db.session.commit()
        return make_response('Membresía regitrada con exito.', 201)
    else:
        membership_id = data.get('id')
        membership = Memberships.query.filter_by(name=name).first()
        if membership:
            return make_response('Ya hay una membresía registrada con ese nombre.', 501)
        membership = Memberships.query.filter_by(id=membership_id).first()
        membership.name = name
        membership.cost = cost
        db.session.commit()
        return make_response('Membresía actualizada con exito.', 201)

def deleteMembership():
    data = request.get_json()
    membership_id = data.get('membership_id')
    try:
        membership = Memberships.find_by_id(membership_id)
        db.session.delete(membership)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)