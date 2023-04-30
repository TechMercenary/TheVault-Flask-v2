from models import db, Holiday, Country
from . import app
from flask import render_template, request, url_for, redirect
import pendulum

@app.route('/holiday/', methods=['GET', 'POST'])
def holiday_index():

    q_year = pendulum.now().year
    q_country_id = Country.query.filter_by(code_2='AR').first().id

    if request.method == 'POST':
        q_year = int(request.form['q_year'])
        q_country_id = int(request.form['q_country_id'])
                      
    holidays = Holiday.query.join(Country).filter(Country.is_enabled == True)
    years = {date.date.year for date in holidays}
    countries = Country.query.filter(Country.id.in_({holiday.country.id for holiday in holidays})).all()

    if q_year != 0:
        holidays = holidays.filter(Holiday.date >= f"{q_year}-01-01", Holiday.date <= f"{q_year}-12-31")
    
    if q_country_id != 0:
        holidays = holidays.filter(Country.id == q_country_id)

    holidays = holidays.order_by(Holiday.date, Country.name).all()

    return render_template(
        'holiday/holiday_index.html',
        holidays=holidays,
        years=years,
        q_year=q_year,
        q_country_id=q_country_id,
        countries=countries,
    )


@app.route('/holiday/create/', methods=['GET', 'POST'])
def holiday_create():
    if request.method == 'POST':
        
        code = request.form['code'].upper().strip()
        description = request.form['description'].strip() if request.form['description'] else None
        
        db.session.add(Holiday(
            code=code,
            description=description,
        ))
        db.session.commit()
        return redirect(url_for('holiday_index'))

    return render_template(
        'holiday/holiday_create.html',
    )


@app.route('/holiday/<int:holiday_id>/edit/', methods=['GET', 'POST'])
def holiday_edit(holiday_id):
    holiday = Holiday.query.get_or_404(holiday_id)

    if request.method == 'POST':
        holiday.code = request.form['code'].upper().strip()
        holiday.description = request.form['description'].strip() if request.form['description'] else None
        db.session.add(holiday)
        db.session.commit()
        return redirect(url_for('holiday_index'))
    return render_template(
        'holiday/holiday_edit.html',
        holiday=holiday,
    )


@app.route('/holiday/<int:holiday_id>/delete/', methods=['GET', 'POST'])
def holiday_delete(holiday_id):
    db.session.delete(Holiday.query.get_or_404(holiday_id))
    db.session.commit()
    
    return redirect(url_for('holiday_index'))
