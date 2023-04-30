from models import db, Currency, Country, Timezone
from . import app
from flask import render_template, request, url_for, redirect
from config import get_app_settings, set_app_settings
import os

@app.route('/app_settings/', methods=['GET', 'POST'])
def app_settings():
    
    if request.method == 'POST':

        fernet_key = request.form['fernet_key']
        country_id = request.form['country_id']
        currency_id = request.form['currency_id']
        timezone_id = request.form['timezone_id']

        os.environ['FERNET_KEY'] = fernet_key
        new_country = Country.query.get_or_404(country_id)
        new_currency = Currency.query.get_or_404(currency_id)
        new_timezone = Timezone.query.get_or_404(timezone_id)

        set_app_settings(settings={
            'DEFAULT_COUNTRY': new_country.code_2,
            'DEFAULT_CURRENCY': new_currency.code,
            'UI_TIMEZONE': new_timezone.code,
        })

        return redirect(url_for('app_settings'))

    app_settings = get_app_settings()

    countries = Country.query.order_by(Country.name).all()
    default_country = Country.query.filter_by(code_2=app_settings['DEFAULT_COUNTRY']).first()

    currencies = Currency.query.order_by(Currency.code).all()
    default_currency = Currency.query.filter_by(code=app_settings['DEFAULT_CURRENCY']).first()

    timezones = Timezone.query.order_by(Timezone.code).all()
    ui_timezone = Timezone.query.filter_by(code=app_settings['UI_TIMEZONE']).first()

    return render_template(
        'app_settings/app_settings.html',
        is_fernet_key_set=bool(os.environ.get('FERNET_KEY')),
        default_country=default_country,
        countries=countries,
        currencies=currencies,
        default_currency=default_currency,
        timezones=timezones,
        ui_timezone=ui_timezone,
    )

