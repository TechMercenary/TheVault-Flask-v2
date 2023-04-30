from models import db, Paycheck, Employer, Currency
from . import app
from flask import render_template, request, url_for, redirect
from config import get_app_settings
import pendulum

@app.route('/paycheck/')
def paycheck_index():
    
    paychecks = Paycheck.query.order_by(Paycheck.payment_date.desc()) .all()
    
    return render_template(
        'paycheck/paycheck_index.html',
        paychecks=paychecks,
    )


@app.route('/paycheck/create/', methods=['GET', 'POST'])
def paycheck_create():
    
    app_settings = get_app_settings()
    
    if request.method == 'POST':
        employer_id = request.form.get('employer_id')
        cbu = request.form.get('cbu')
        period_year = request.form.get('period_year')
        period_month = request.form.get('period_month')
        payment_date = pendulum.parser.parse(request.form.get('payment_date'), tz=app_settings['UI_TIMEZONE'])
        currency_id = request.form.get('currency_id')
        gross_amount = request.form.get('gross_amount')

        db.session.add(Paycheck(
            employer_id=employer_id,
            cbu=cbu,
            period_year=period_year,
            period_month=period_month,
            payment_date=payment_date,
            currency_id=currency_id,
            gross_amount=gross_amount,
        ))

        db.session.commit()

        return redirect(url_for('paycheck_index'))

    employers = sorted(Employer.query.order_by(Employer.name).all(), key=lambda e: e.name.upper())
    currencies = Currency.query.order_by(Currency.code).all()
    pendulum_now = pendulum.now(tz=app_settings['UI_TIMEZONE'])
    
    return render_template(
        'paycheck/paycheck_create.html',
        employers=employers,
        currencies=currencies,
        pendulum_now=pendulum_now,
    )


@app.route('/paycheck/<int:paycheck_id>/edit/', methods=['GET', 'POST'])
def paycheck_edit(paycheck_id):
    pass


@app.route('/paycheck/<int:paycheck_id>/delete/', methods=['GET', 'POST'])
def paycheck_delete(paycheck_id):
    paycheck = Paycheck.query.get_or_404(paycheck_id)
    
    for paycheck_item in paycheck.items:
        db.session.delete(paycheck_item)
    
    db.session.flush()
    db.session.delete(Paycheck.query.get_or_404(paycheck_id))
    db.session.commit()
    
    return redirect(url_for('paycheck_index'))
