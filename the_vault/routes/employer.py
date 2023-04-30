from models import db, Employer
from . import app
from flask import render_template, request, url_for, redirect


@app.route('/employer/')
def employer_index():
    employers = Employer.query.order_by(Employer.name).all()
    return render_template(
        'employer/employer_index.html',
        employers=employers,
    )


@app.route('/employer/create/', methods=['GET', 'POST'])
def employer_create():
    if request.method == 'POST':
        
        name = request.form['name'].upper().strip()
        description = request.form['description'].strip() if request.form['description'] else None
        
        db.session.add(Employer(
            name=name,
            description=description,
        ))
        db.session.commit()
        return redirect(url_for('employer_index'))

    return render_template(
        'employer/employer_create.html',
    )


@app.route('/employer/<int:employer_id>/edit/', methods=['GET', 'POST'])
def employer_edit(employer_id):
    employer = Employer.query.get_or_404(employer_id)

    if request.method == 'POST':
        employer.name = request.form['name'].upper().strip()
        employer.description = request.form['description'].strip() if request.form['description'] else None
        db.session.add(employer)
        db.session.commit()
        return redirect(url_for('employer_index'))
    return render_template(
        'employer/employer_edit.html',
        employer=employer,
    )
    


@app.route('/employer/<int:employer_id>/delete/', methods=['GET', 'POST'])
def employer_delete(employer_id):
    db.session.delete(Employer.query.get_or_404(employer_id))
    db.session.commit()
    
    return redirect(url_for('employer_index'))
