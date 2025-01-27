import os
import sys
from datetime import datetime
import base64
from flask import render_template, request, make_response, send_from_directory
from sqlalchemy import func
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
import csv
from flask_login import current_user
from db import db
from models.users import Users
import logging
from pytz import timezone
logger = logging.getLogger(__name__)

def index_logic():
    return render_template('employees/list.html')