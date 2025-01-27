from flask import render_template
import logging
logger = logging.getLogger(__name__)

def index_logic():
    return render_template('employees/list.html')