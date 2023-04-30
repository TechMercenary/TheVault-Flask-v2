from models import db, SalaryAgreement, Currency, Employer
from . import app
from flask import render_template, request, url_for, redirect
import pendulum

@app.route('/salary_agreement/')
def salary_agreement_index():
    salary_agreements = SalaryAgreement.query.order_by(SalaryAgreement.started_at.desc()).all()
    return render_template(
        'salary_agreement/salary_agreement_index.html',
        salary_agreements=salary_agreements,
    )


@app.route('/salary_agreement/create/', methods=['GET', 'POST'])
def salary_agreement_create():
    
    employers = Employer.query.order_by(Employer.name).all()
    currencies = Currency.query.order_by(Currency.code).all()
    
    if request.method == 'POST':
        
        employer_id = request.form['employer_id']
        description = request.form['description'].strip() if request.form['description'] else None
        started_at = pendulum.datetime(
            year=int(request.form['started_at_year']),
            month=int(request.form['started_at_month']),
            day=int(request.form['started_at_day']),
            hour=int(request.form['started_at_hour']),
            minute=int(request.form['started_at_minute']),
            tz='America/Argentina/Buenos_Aires',
        )
        currency_id = request.form['currency_id']
        monthly_gross_amount = request.form['monthly_gross_amount']
        
        db.session.add(SalaryAgreement(
            employer_id=employer_id,
            description=description,
            started_at=started_at.to_datetime_string(),
            ended_at=None,
            currency_id=currency_id,
            monthly_gross_amount=monthly_gross_amount,
        ))
        db.session.commit()
        return redirect(url_for('salary_agreement_index'))

    return render_template(
        'salary_agreement/salary_agreement_create.html',
        employers=employers,
        currencies=currencies,
        pendulum_now=pendulum.now(),
    )


@app.route('/salary_agreement/<int:salary_agreement_id>/edit/', methods=['GET', 'POST'])
def salary_agreement_edit(salary_agreement_id):
    salary_agreement = SalaryAgreement.query.get_or_404(salary_agreement_id)

    if request.method == 'POST':

        employer_id = request.form['employer_id']
        description = request.form['description'].strip() if request.form['description'] else None
        started_at = pendulum.datetime(
            year=int(request.form['started_at_year']),
            month=int(request.form['started_at_month']),
            day=int(request.form['started_at_day']),
            hour=int(request.form['started_at_hour']),
            minute=int(request.form['started_at_minute']),
            tz='America/Argentina/Buenos_Aires',
        )
        ended_at = pendulum.datetime(
            year=int(request.form['ended_at_year']),
            month=int(request.form['ended_at_month']),
            day=int(request.form['ended_at_day']),
            hour=int(request.form['ended_at_hour']),
            minute=int(request.form['ended_at_minute']),
            tz='America/Argentina/Buenos_Aires',
        )
        currency_id = request.form['currency_id']
        monthly_gross_amount = request.form['monthly_gross_amount']
        
        salary_agreement.employer_id = employer_id
        salary_agreement.description = description
        salary_agreement.started_at = started_at.to_datetime_string()
        salary_agreement.ended_at = ended_at.to_datetime_string()
        salary_agreement.currency_id = currency_id
        salary_agreement.monthly_gross_amount = monthly_gross_amount
        
        db.session.add(salary_agreement)
        db.session.commit()
        return redirect(url_for('salary_agreement_index'))
    
    employers = Employer.query.order_by(Employer.name).all()
    currencies = Currency.query.order_by(Currency.code).all()
    return render_template(
        'salary_agreement/salary_agreement_edit.html',
        salary_agreement=salary_agreement,
        employers=employers,
        currencies=currencies,
    )


@app.route('/salary_agreement/<int:salary_agreement_id>/delete/', methods=['GET', 'POST'])
def salary_agreement_delete(salary_agreement_id):
    db.session.delete(SalaryAgreement.query.get_or_404(salary_agreement_id))
    db.session.commit()
    
    return redirect(url_for('salary_agreement_index'))
