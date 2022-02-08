import logging
import re
import decimal
from sqlalchemy import exc, asc
from ..domains.documents import Document
from ..domains.movements import Movement
from ..domains.companies import Company
from ..domains.suppliers import Supplier
from ..domains.rules import Rule
from ..domains.users import User
from ..repositories.db.database import MovementDb, DocumentDb, db

class AccountsPayableRepository:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def make_transaction(self, theComp, theSupp, theRule, theUser, document, movement_date, document_number, amount, issue_date, due_date, reference):
        self.logger.debug('make_transaction')

        try:
            if theRule.action_over_document == 'C':
                previous_balance = 0
                total_debits = 0
                total_credits = 0
                if theRule.movement_type == 'D':
                    total_debits = amount
                if theRule.movement_type == 'C':
                    total_credits = amount

                theDocument = DocumentDb(company_id=theComp.company_id, supplier_id=theSupp.supplier_id, document_number=document_number, issue_date=issue_date, due_date=due_date, reference=reference, previous_balance=previous_balance, total_debits=total_debits, total_credits=total_credits)
                db.session.add(theDocument)

            elif theRule.action_over_document == 'U':
                theDocument = DocumentDb.query.get((theComp.company_id, theSupp.supplier_id, document_number))

                self.logger.debug(self.__get_money_value(theDocument.total_debits)+self.__get_money_value('$'+str(amount)))

                if theRule.movement_type == 'D':
                    theDocument.total_debits = self.__get_money_value(theDocument.total_debits) + self.__get_money_value('$'+str(amount))
                if theRule.movement_type == 'C':
                    theDocument.total_credits = self.__get_money_value(theDocument.total_credits) + self.__get_money_value('$'+str(amount))

                if theRule.update_issue_date == 'Y':
                    theDocument.issue_date = issue_date
                if theRule.update_due_date == 'Y':
                    theDocument.due_date = due_date
                if theRule.update_reference == 'Y':
                    theDocument.reference = reference
            else:
                theDocument = DocumentDb.query.get((theComp.company_id, theSupp.supplier_id, document_number))
                if theDocument == None:
                    theDocument = DocumentDb(company_id=theComp.company_id, supplier_id=theSupp.supplier_id, document_number=document_number, issue_date=issue_date, due_date=due_date, reference=reference, previous_balance=previous_balance, total_debits=total_debits, total_credits=total_credits)

                if theRule.movement_type == 'D':
                    theDocument.total_debits = self.__get_money_value(theDocument.total_debits) + self.__get_money_value('$'+str(amount))
                if theRule.movement_type == 'C':
                    theDocument.total_credits = self.__get_money_value(theDocument.total_credits) + self.__get_money_value('$'+str(amount))

                if theRule.update_issue_date == 'Y':
                    theDocument.issue_date = issue_date
                if theRule.update_due_date == 'Y':
                    theDocument.due_date = due_date
                if theRule.update_reference == 'Y':
                    theDocument.reference = reference

            theMovement = MovementDb(movement_date=movement_date, company_id=theComp.company_id, supplier_id=theSupp.supplier_id, document_number=document_number, rule_id=theRule.rule_id, amount=amount, issue_date=issue_date, due_date=due_date, reference=reference, user_id=theUser.user_id)
            db.session.add(theMovement)

            db.session.commit()
            return self.__get_domain_object(theMovement=theMovement)

        except exc.SQLAlchemyError as error:
            self.logger.error(error.__str__())
            db.session.rollback()
            return None

    def __get_domain_object(self, theMovement):
            return Movement(theMovement.movement_id, theMovement.movement_date, theMovement.company_id, theMovement.supplier_id, theMovement.document_number, theMovement.rule_id, theMovement.amount, theMovement.issue_date, theMovement.due_date, theMovement.reference, theMovement.user_id, Company(theMovement.company.company_id, theMovement.company.business_name), Supplier(theMovement.supplier.supplier_id, theMovement.supplier.supplier_name), Rule(theMovement.rule.rule_id, theMovement.rule.rule_description, theMovement.rule.action_over_document, theMovement.rule.movement_type, theMovement.rule.update_issue_date, theMovement.rule.update_due_date, theMovement.rule.update_reference), User(theMovement.user.user_id, theMovement.user.user_name, theMovement.user.user_email, None))

    def __get_money_value(self, theValue):
        if theValue is None:
            return 0
        else:
            m = re.match(r"\$([\d.]+)", theValue)
            if m:
                theValue = decimal.Decimal(m.group(1))
        return theValue
