from datetime import datetime
from dateutil import relativedelta
import jinja2

def _jinja2_strftime(date):
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    return date.strftime("%d/%m/%Y")



def seniority(date):
    today = datetime.now()
    #time_diff = today - date
    delta = relativedelta.relativedelta(today, date)
    result = f'{delta.years} Años {delta.months} Meses'
    return result

def seniority_year(date):
    today = datetime.now()
    #time_diff = today - date
    delta = relativedelta.relativedelta(today, date)
    result = delta.years
    return result

def month_to_text(month):
    if month == '01':
        return "enero"
    if month == '02':
        return "febrero"
    if month == '03':
        return "marzo"
    if month == '04':
        return "abril"
    if month == '05':
        return "mayo"
    if month == '06':
        return "junio"
    if month == '07':
        return "julio"
    if month == '08':
        return "agosto"
    if month == '09':
        return "septiembre"
    if month == '10':
        return "octubre"
    if month == '11':
        return "noviembre"
    if month == '12':
        return "diciembre"



def birth_date_years(date):
    today = datetime.now()
    #time_diff = today - date
    delta = relativedelta.relativedelta(today, date)
    result = f'{delta.years} Años'
    return result


def vacations(date):
    today = datetime.now()
    delta = relativedelta.relativedelta(today, date)
    years = delta.years
    return {
        1: 12,
        2: 14,
        3: 16,
        4: 18,
        5: 20,
        **dict.fromkeys(range(6, 10), 22),
        **dict.fromkeys(range(11, 15), 24),
        **dict.fromkeys(range(16, 20), 26),
        **dict.fromkeys(range(21, 25), 28),
        **dict.fromkeys(range(26, 30), 30),
        **dict.fromkeys(range(31, 35), 32),
    }.get(years)



def status(status):
    if int(status) == 1:
        return 'ACTIVO'
    else:
        return 'INACTIVO'

def vacation_status(status):
    if int(status) == 0:
        return 'PENDIENTE'
    elif int(status) == 1:
        return 'AUTORIZADAS'
    elif int(status) == 2:
        return 'DENEGADAS'