import os
from pathlib import Path
import logging
from logging import handlers

logger = logging.getLogger()

class Config:
    # MYSQL
    mysql_db_username = os.environ.get('mysql_db_username')
    mysql_db_password =  os.environ.get('mysql_db_password')
    mysql_db_name =  os.environ.get('mysql_db_name')
    mysql_db_hostname =  os.environ.get('mysql_db_hostname')

    DEBUG = True
    PORT = os.environ.get('PORT')
    HOST = "localhost"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = '/static/employees_photos'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(
        DB_USER=mysql_db_username,
        DB_PASS=mysql_db_password,
        DB_ADDR=mysql_db_hostname,
        DB_NAME=mysql_db_name)

    basedir = os.path.abspath(os.path.dirname(__file__))
    root_dir = Path(basedir).parent
    logs_dir = os.path.join(basedir, "logs")
    os.makedirs(logs_dir, exist_ok=True)


    logger.setLevel(logging.INFO)
    format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'

    logHandler = handlers.TimedRotatingFileHandler(f'{logs_dir}/info.log', when='H', interval=1)
    logHandler.setLevel(logging.INFO)
    logHandler.setFormatter(logging.Formatter(format))
    logger.addHandler(logHandler)

    errorLogHandler = handlers.TimedRotatingFileHandler(f'{logs_dir}/error.log', when='H', interval=1)
    errorLogHandler.setLevel(logging.ERROR)
    errorLogHandler.setFormatter(logging.Formatter(format))
    logger.addHandler(errorLogHandler)