from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
import logging
main = Blueprint('main', __name__)

logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('home/dashboard.html')

