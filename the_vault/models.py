from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import TypeDecorator, Integer
from config import CONFIG
import pendulum
import datetime


db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = ({"schema": CONFIG['DB_SCHEMA']},)


class Country(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code_2 = db.Column(db.Text, unique=True, nullable=False)
    code_3 = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    is_enabled = db.Column(db.Boolean, nullable=False, default=True)
    

class Timezone(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.country.id"), nullable=False)
    code = db.Column(db.Text, unique=True, nullable=False)
    is_enabled = db.Column(db.Boolean, nullable=False, default=True)

    country = db.relationship("Country", backref="timezones")


class Currency(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    

class Holiday(BaseModel):
    __table_args__ = (
        UniqueConstraint('country_id', 'date', name='unique_country_date'),
    ) + BaseModel.__table_args__
    
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.country.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.Text, nullable=False)
    
    country = db.relationship("Country")
    

class Employer(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.country.id"), nullable=False)
    timezone_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.timezone.id"), nullable=False)
    cuit = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    country = db.relationship("Country", backref="employers")
    timezone = db.relationship("Timezone")


class JobContract(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.employer.id"), nullable=False)
    personnel_number = db.Column(db.Text, nullable=True)


# What is paid is what is earned actually
class Paycheck(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.employer.id"), nullable=False)
    cbu = db.Column(db.Text, nullable=True)
    period_year = db.Column(db.Integer, nullable=False)
    period_month = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.currency.id"), nullable=False)
    gross_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    employer = db.relationship("Employer", backref="paychecks")
    currency = db.relationship("Currency")

class PaycheckItem(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    paycheck_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.paycheck.id"), nullable=False)
    code = db.Column(db.Text, nullable=False)
    concept = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    is_remunerative = db.Column(db.Boolean, nullable=False, default=True)
    is_discount = db.Column(db.Boolean, nullable=False, default=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    paycheck = db.relationship("Paycheck", backref="items")
    
    @property
    def total_remunerative(self):
        return sum(item.amount for item in self.paycheck.items if item.is_remunerative)

    @property
    def total_non_remunerative(self):
        return sum(item.amount for item in self.paycheck.items if not item.is_remunerative and not item.is_discount)
    
    @property
    def total_discount(self):
        return sum(item.amount for item in self.paycheck.items if item.is_discount)
    
    @property
    def total_net(self):
        return self.total_remunerative + self.total_non_remunerative - self.total_discount


# Expenctancy vs actual (for report and forecast)
class SalaryAgreement(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.employer.id"), nullable=False)
    description = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime(timezone=True), nullable=False)
    ended_at = db.Column(db.DateTime(timezone=True), nullable=True)
    currency_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.currency.id"), nullable=False)
    monthly_gross_amount = db.Column(db.Numeric(10, 2), nullable=False)

    employer = db.relationship('Employer', foreign_keys=[employer_id], backref=db.backref('salary_agreements', lazy=True))
    currency = db.relationship('Currency', foreign_keys=[currency_id])

# The intention is to control the employer's debt, for accrual basis
class SalaryEarned(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    salary_agreement_id = db.Column(db.Integer, db.ForeignKey(f"{CONFIG['DB_SCHEMA']}.salary_agreement.id"), nullable=False)
    earned_at = db.Column(db.DateTime(timezone=True), nullable=False)
    period_year = db.Column(db.Integer, nullable=False)
    period_month = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    salary_agreement = db.relationship('SalaryAgreement', foreign_keys=[salary_agreement_id], backref=db.backref('salary_earneds', lazy=True))

    # @property
    # def current_earned(self):
    #     return self.salary_agreement.monthly_gross_amount


