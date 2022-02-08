import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import MONEY
db = SQLAlchemy()

class UserDb(db.Model):
    __tablename__ = 'users'
    user_id = db.Column('user_id',db.Integer, primary_key=True)
    user_name = db.Column('user_name',db.String(15), unique=True, nullable=False)
    user_email = db.Column('user_email',db.String(120), unique=True, nullable=False)
    user_pass =  db.Column('user_pass',db.Text(), nullable=False)

    def __repr__(self) -> str:
        return 'User>>>' + self.user_name

    def serialize(self):
        return {
        "id": self.id,
        "name": self.name
        }

class CompanyDb(db.Model):
    __tablename__ = 'companies'
    company_id = db.Column('company_id',db.Integer, primary_key=True)
    business_name = db.Column('business_name',db.String(50), unique=False, nullable=False)

    def __repr__(self) -> str:
        return 'Company>>>' + self.business_name

class SupplierDb(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column('supplier_id',db.Integer, primary_key=True)
    supplier_name = db.Column('supplier_name',db.String(50), unique=False, nullable=False)

    def __repr__(self) -> str:
        return 'Supplier>>> ' + self.supplier_name

class RuleDb(db.Model):
    __tablename__ = 'rules'
    rule_id = db.Column('rule_id',db.Integer, primary_key=True)
    rule_description = db.Column('rule_description',db.String(50), unique=False, nullable=False)
    action_over_document = db.Column('action_over_document',db.String(1), unique=False, nullable=False)
    movement_type = db.Column('movement_type',db.String(1), unique=False, nullable=False)
    update_issue_date = db.Column('update_issue_date',db.String(1), unique=False, nullable=False)
    update_due_date = db.Column('update_due_date',db.String(1), unique=False, nullable=False)
    update_reference = db.Column('update_reference',db.String(1), unique=False, nullable=False)

    def __repr__(self) -> str:
        return 'Rule>>> ' + self.rule_description

class DocumentDb(db.Model):
    __tablename__ = 'documents'
    company_id = db.Column('company_id',db.Integer(), primary_key=True, autoincrement=False)
    supplier_id = db.Column('supplier_id',db.Integer(), primary_key=True, autoincrement=False)
    document_number = db.Column('document_number',db.String(12), primary_key=True, autoincrement=False)
    issue_date = db.Column('issue_date',db.Date, unique=False, nullable=False)
    due_date = db.Column('due_date',db.Date, unique=False, nullable=False)
    reference = db.Column('reference',db.String(12), unique=False, nullable=True)
    previous_balance = db.Column('previous_balance', MONEY, default=0, unique=False, nullable=False)
    total_debits = db.Column('total_debits', MONEY, default=0, unique=False, nullable=False)
    total_credits = db.Column('total_credits', MONEY, default=0, unique=False, nullable=False)

    def __repr__(self) -> str:
        return 'Document>>> ' + str(self.company_id) + ', ' + str(self.supplier_id) + ', ' + self.document_number

class MovementDb(db.Model):
    __tablename__ = 'movements'
    movement_id = db.Column('movement_id', db.Integer, primary_key=True, autoincrement=True)
    movement_date = db.Column('movement_date',db.Date(), unique=False, nullable=False)
    company_id = db.Column('company_id',db.Integer(), db.ForeignKey('companies.company_id'))
    supplier_id = db.Column('supplier_id',db.Integer(), db.ForeignKey('suppliers.supplier_id'))
    document_number = db.Column('document_number',db.String(12), unique=False)
    rule_id = db.Column('rule_id',db.Integer(), db.ForeignKey('rules.rule_id'))
    amount = db.Column('amount', MONEY, default=0, unique=False, nullable=False)
    issue_date = db.Column('issue_date',db.Date(), unique=False, nullable=False)
    due_date = db.Column('due_date',db.Date(), unique=False, nullable=False)
    reference = db.Column('reference',db.String(12), unique=False, nullable=True)
    user_id = db.Column('user_id',db.Integer(), db.ForeignKey('users.user_id'))

    company = db.relationship("CompanyDb")
    supplier = db.relationship("SupplierDb")
    rule = db.relationship("RuleDb")
    user = db.relationship("UserDb")

    def __repr__(self) -> str:
        return 'Movement>>> ' + str(self.movement_id) + ', ' + str(self.company_id) + ', ' + str(self.supplier_id) + ', ' + self.document_number
