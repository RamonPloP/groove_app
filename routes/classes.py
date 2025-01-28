from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models.utils import is_admin
from models.classes import Classes
from controllers.classesController import addClass, deleteClass
import logging

logger = logging.getLogger(__name__)

classes = Blueprint('classes', __name__, url_prefix='/classes')

@classes.route('/crud', methods=['POST'])
@is_admin
@login_required
def classes_crud():
    return addClass()

@classes.route('/<id>')
@is_admin
@login_required
def find_class(id):
    clase = Classes.find_by_id(id)
    return render_template('home/classes/modal_edit.html', clase=clase)

@classes.route('/delete', methods=['POST'])
@login_required
def class_delete():
    return deleteClass()

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