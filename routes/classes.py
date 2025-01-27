from flask import Blueprint, render_template, Response, make_response, request, jsonify
from flask_login import login_required, current_user
from models.utils import is_admin
from models.classes import Classes
from db import db
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

classes = Blueprint('classes', __name__, url_prefix='/classes')

@classes.route('/crud', methods=['POST'])
@is_admin
@login_required
def classes_crud():
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
            logger.error(f"Error al guadar banco: {err.messages} con los datos : {data}")
        db.session.add(clase)
        db.session.commit()
        return make_response('Banco Regitrado con exito.', 201)
    else:
        class_id = data.get('id')
        bank = Classes.query.filter_by(id=class_id).first()
        bank.name = name
        db.session.commit()
        return make_response('Clase actualizada con exito.', 201)

@classes.route('/<id>')
@is_admin
@login_required
def find_class(id):
    clase = Classes.find_by_id(id)
    return render_template('home/classes/modal_edit.html', clase=clase)

@classes.route('/delete', methods=['POST'])
@login_required
def class_delete():
    data = request.get_json()
    class_id = data.get('class_id')
    try:
        clase = Classes.find_by_id(class_id)
        db.session.delete(clase)
        db.session.commit()
        return make_response('Borrado existoso.', 201)
    except Exception as e:
        return make_response(str(e), 400)

@classes.route('/all')
@is_admin
@login_required
def classes_list_view():
    classes = Classes.get_all()
    return render_template('home/classes/list.html', classes=classes)

@classes.route('/list')
@is_admin
@login_required
def classes_list():
    clases = Classes.get_all()
    clases = [clase.to_dict() for clase in clases]
    return jsonify(clases)

@classes.route('/add')
@is_admin
@login_required
def classes_add():
    return render_template('home/classes/modal_add.html')