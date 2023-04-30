from models import db, SalaryEarned
from . import app
from flask import render_template, request, url_for, redirect


@app.route('/salary_earned/')
def salary_earned_index():
    salaries_earned = SalaryEarned.query.order_by(SalaryEarned.earned_at.desc()).all()
    return render_template(
        'salary_earned/salary_earned_index.html',
        salaries_earned=salaries_earned,
    )


@app.route('/salary_earned/create/', methods=['GET', 'POST'])
def salary_earned_create():
    if request.method == 'POST':
        
        code = request.form['code'].upper().strip()
        description = request.form['description'].strip() if request.form['description'] else None
        
        db.session.add(SalaryEarned(
            code=code,
            description=description,
        ))
        db.session.commit()
        return redirect(url_for('salary_earned_index'))

    return render_template(
        'salary_earned/salary_earned_create.html',
    )


@app.route('/salary_earned/<int:salary_earned_id>/edit/', methods=['GET', 'POST'])
def salary_earned_edit(salary_earned_id):
    salary_earned = SalaryEarned.query.get_or_404(salary_earned_id)

    if request.method == 'POST':
        salary_earned.code = request.form['code'].upper().strip()
        salary_earned.description = request.form['description'].strip() if request.form['description'] else None
        db.session.add(salary_earned)
        db.session.commit()
        return redirect(url_for('salary_earned_index'))
    return render_template(
        'salary_earned/salary_earned_edit.html',
        salary_earned=salary_earned,
    )


@app.route('/salary_earned/<int:salary_earned_id>/delete/', methods=['GET', 'POST'])
def salary_earned_delete(salary_earned_id):
    db.session.delete(SalaryEarned.query.get_or_404(salary_earned_id))
    db.session.commit()
    
    return redirect(url_for('salary_earned_index'))
