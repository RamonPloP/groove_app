from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models import income_concepts
from models import expense_concepts
from models import memberships
from models import classes
from models import payment_types
from models import leads
from models import teachers
from models import students
from models import incomes
from models import expenses
from models import users