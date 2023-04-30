from models import db, Country, Timezone, Currency, \
    Holiday, Employer, SalaryAgreement, SalaryEarned, \
    Paycheck, PaycheckItem

import pendulum
import pycountry
import pytz


def insert(model, data):
    for row in data:
        db.session.add(model(**row))
    db.session.commit()


# TODO: Make Country data incremental to keep the id
def populate_country():
    data=[{
        'code_2': country.alpha_2,
        'code_3': country.alpha_3,
        'name': country.name,
        'is_enabled': True,
    } for country in pycountry.countries]
    insert(Country, data=data)

# TODO: Make Country data incremental to keep the id
def populate_timezone():
    data = []
    for code, timezones in pytz.country_timezones.items():
        country_id = Country.query.filter_by(code_2=code).first().id
        data.extend(
            {
                'country_id': country_id,
                'code': timezone,
                'is_enabled': True,
            }
            for timezone in timezones
        )
    insert(Timezone, data=data)


def populate_currency():
    insert(Currency, data=[
        {'code': 'ARS', 'description': 'Peso Argentino'},
        {'code': 'USD', 'description': 'Dolar Estadounidense'},
    ])


def populate_holiday():
    holidays = {
        'AR': {
            # 2022
            '2022-01-01': 'Año Nuevo',
            '2022-02-28': 'Carnaval',
            '2022-03-01': 'Carnaval',
            '2022-03-24': 'Día Nacional de la Memoria por la Verdad y la Justicia',
            '2022-04-02': 'Día del Veterano y de los Caídos en la Guerra de Malvinas',
            '2022-04-14': 'Jueves Santo',
            '2022-04-15': 'Viernes Santo',
            '2022-05-01': 'Día del Trabajador',
            '2022-05-18': 'Censo Nacional',
            '2022-05-25': 'Día de la Revolución de Mayo',
            '2022-06-17': 'Día Paso a la Inmortalidad del Gral. Don Martín Miguel de Güemes',
            '2022-06-20': 'Día Paso a la Inmortalidad del General Manuel Belgrano',
            '2022-07-09': 'Día de la Independencia',
            '2022-08-15': 'Día Paso a la Inmortalidad del Gral. José de San Martín',
            '2022-10-07': 'Puente Turístico',
            '2022-10-10': 'Día del Respeto a la Diversidad Cultural',
            '2022-11-20': 'Día de la Soberanía Nacional',
            '2022-11-21': 'Puente Turístico',
            '2022-12-08': 'Inmaculada Concepción de María',
            '2022-12-09': 'Puente Turístico',
            '2022-12-25': 'Navidad',
            # 2023
            '2023-01-01': 'Año Nuevo',
            '2023-02-20': 'Carnaval',
            '2023-02-21': 'Carnaval',
            '2023-03-24': 'Día Nacional de la Memoria por la Verdad y la Justicia',
            '2023-04-02': 'Día del Veterano y de los Caídos en la Guerra de Malvinas',
            '2023-04-06': 'Jueves Santo',
            '2023-04-07': 'Viernes Santo',
            '2023-05-01': 'Día del Trabajador',
            '2023-05-25': 'Día de la Revolución de Mayo',
            '2023-05-26': 'Puente Turístico',
            '2023-06-17': 'Día Paso a la Inmortalidad del Gral. Don Martín Miguel de Güemes',
            '2023-06-19': 'Puente Turístico',
            '2023-06-20': 'Día Paso a la Inmortalidad del General Manuel Belgrano',
            '2023-07-09': 'Día de la Independencia',
            '2023-08-21': 'Día Paso a la Inmortalidad del Gral. José de San Martín',
            '2023-10-13': 'Puente Turístico',
            '2023-10-16': 'Día del Respeto a la Diversidad Cultural',
            '2023-11-20': 'Día de la Soberanía Nacional',
            '2023-12-08': 'Inmaculada Concepción de María',
            '2023-12-25': 'Navidad',
        },
        'MX': {
            '2022-01-01': "Año Nuevo",
            '2022-02-07': 'Día de la Constitución',
            '2022-03-21': 'Natalicio de Benito Juárez',
            '2022-04-15': 'Viernes Santo',
            '2022-05-01': 'Día del Trabajo',
            '2022-09-16': 'Día de la Independencia',
            '2022-11-02': 'Día de Muertos',
            '2022-11-20': 'Revolution Day',
            '2022-12-12': 'Día de la Virgen de Guadalupe',
            '2022-12-25': 'Navidad'
        },
    }
    
    data = []
    for code, holidays in holidays.items():
        country_id = Country.query.filter_by(code_2=code).first().id
        data.extend(
            {
                'country_id': country_id,
                'date': date,
                'name': name,
            }
            for date, name in holidays.items()
        )
    insert(Holiday, data=data)


def populate_employer():
    employers = {
        'AR': ['Citibank', 'Practia'],
        'MX': ['Kavak'],
        'US': ['Outcome Health'],
    }

    data = []
    for code, employers in employers.items():
        country_id = Country.query.filter_by(code_2=code).first().id
        timezone_id = Timezone.query.filter_by(country_id=country_id).first().id
        
        data.extend(
            {
                'name': employer,
                'country_id': country_id,
                'timezone_id': timezone_id,
                'description': employer.lower(),
            }
            for employer in employers
        )
    insert(Employer, data=data)


def populate_salary_agreement():
    insert(SalaryAgreement, data=[
        {'employer_id': 1, 'description': 'citibank', 'started_at': '2010-01-15 00:00:00', 'ended_at': '2011-05-13 00:00:00', 'currency_id': 1, 'monthly_gross_amount': 25000},
        {'employer_id': 2, 'description': 'OLX', 'started_at': '2011-05-14', 'ended_at': '2012-02-10', 'currency_id': 1, 'monthly_gross_amount': 30000},
    ])


def populate_salary_earned():
    data = []
    for salary_agreement in SalaryAgreement.query.all():
        started_at = pendulum.parser.parse(str(salary_agreement.started_at))
        ended_at = pendulum.parser.parse(str(salary_agreement.ended_at)) if salary_agreement.ended_at else pendulum.now().add(months=6)
        
        period_start = pendulum.datetime( year=started_at.year, month=started_at.month, day=1 )
        period_end = pendulum.datetime( year=ended_at.year, month=ended_at.month, day=1 )
        
        period = period_start

        while period <= period_end:
            earned_at = period.add(months=1)
            period_year = period.year
            period_month = period.month
            
            print(f"Employer: {salary_agreement.employer.name} | {period_year}-{period_month:02d} | Earned at: {earned_at.to_date_string()}")
            
            data.append({
                'salary_agreement_id': salary_agreement.id,
                'earned_at': earned_at.to_datetime_string(),
                'period_year': period_year,
                'period_month': period_month,
                'description': None,
            })
            
            period = period.add(months=1)

    insert(SalaryEarned, data=data)


def populate_paycheck():
    paycheck_data = {
        'employer_id': 1,
        'cbu': '1234567890123456789012',
        'period_year': 2023,
        'period_month': 3,
        'payment_date': '2023-03-31',
        'currency_id': 1,
        'gross_amount': 450000,
    }
    
    paycheck = Paycheck(**paycheck_data)
    db.session.add(paycheck)
    db.session.flush()
    
    paycheck_items_data = [
        {
            'paycheck_id': paycheck.id,
            'code': '01100',
            'concept': 'SUELDO BASICO',
            'quantity': 30, 
            'is_remunerative': True,
            'is_discount': False,
            'amount': 450000,
        },
        {
            'paycheck_id': paycheck.id,
            'code': '01154',
            'concept': 'ACFA 2023',
            'quantity': 0, 
            'is_remunerative': True,
            'is_discount': False,
            'amount': 72000,
        },
        {
            'paycheck_id': paycheck.id,
            'code': '06005',
            'concept': 'JUBILACION',
            'quantity': 11, 
            'is_remunerative': False,
            'is_discount': True,
            'amount': 57420,
        },
        {
            'paycheck_id': paycheck.id,
            'code': '06010',
            'concept': 'INSSJP LEY 19032',
            'quantity': 3, 
            'is_remunerative': False,
            'is_discount': True,
            'amount': 15660,
        },
        {
            'paycheck_id': paycheck.id,
            'code': '06015',
            'concept': 'OBRA SOCIAL',
            'quantity': 3, 
            'is_remunerative': False,
            'is_discount': True,
            'amount': 15660,
        },
        {
            'paycheck_id': paycheck.id,
            'code': '09661',
            'concept': 'Acuerdo Prov. Home Office',
            'quantity': 0, 
            'is_remunerative': False,
            'is_discount': False,
            'amount': 15080,
        },
        {
            'paycheck_id': paycheck.id,
            'code': '13000',
            'concept': 'IMPUESTO A LAS GANANCIAS',
            'quantity': 0, 
            'is_remunerative': False,
            'is_discount': True,
            'amount': 57690.15,
        },
        {
            'paycheck_id': paycheck.id,
            'code': '15500',
            'concept': 'REDONDEO',
            'quantity': 0, 
            'is_remunerative': False,
            'is_discount': False,
            'amount': 0.15,
        },
    ]

    for items in paycheck_items_data:
        db.session.add(PaycheckItem(**items))
        
    db.session.commit()


def populate_first_time():
    populate_country()
    populate_timezone()
    populate_currency()
    populate_holiday()
    populate_employer()
    populate_salary_agreement()
    populate_paycheck()
    
