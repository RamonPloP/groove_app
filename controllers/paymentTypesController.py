from models.payment_types import PaymentTypes
from flask import request, make_response
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

def addPaymentType():
    data = request.get_json()
    # get de data from request
    name = data.get('name')
    if not data.get('id'):
        payment_type = PaymentTypes.query.filter_by(name=name).first()
        if payment_type:
            return make_response('Ya hay un tipo de pago registrado con ese nombre.', 501)
        try:
            payment_type = PaymentTypes(name=name)
        except ValidationError as err:
            logger.error(f"Error al guadar: {err.messages} con los datos : {data}")
            return make_response(f"Error al guadar: {err.messages} con los datos : {data}", 501)
        db.session.add(payment_type)
        db.session.commit()
        return make_response('Tipo de pago registrado con exito.', 201)
    else:
        payment_type_id = data.get('id')
        payment_type = PaymentTypes.query.filter_by(name=name).first()
        if payment_type:
            return make_response('Ya hay un tipo de pago registrado con ese nombre.', 501)
        payment_type = PaymentTypes.query.filter_by(id=payment_type_id).first()
        payment_type.name = name
        db.session.commit()
        return make_response('Tipo de pago actualizado con exito.', 201)

def deletePaymentType():
    data = request.get_json()
    payment_type_id = data.get('payment_type_id')
    try:
        payment_type = PaymentTypes.find_by_id(payment_type_id)
        db.session.delete(payment_type)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)