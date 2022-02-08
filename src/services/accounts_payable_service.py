import logging
import validators
from datetime import datetime
from ..domains.documents import Document
from ..domains.movements import Movement
from ..domains.companies import Company
from ..domains.suppliers import Supplier
from ..domains.rules import Rule
from ..domains.users import User

from ..repositories.accounts_payable_repository import AccountsPayableRepository
from ..repositories.companies_repository import CompaniesRepository
from ..repositories.documents_repository import DocumentsRepository
from ..repositories.movements_repository import MovementsRepository
from ..repositories.suppliers_repository import SuppliersRepository
from ..repositories.rules_repository import RulesRepository
from ..repositories.users_repository import UsersRepository

class AccountsPayableServiceException(Exception):
    def __init__(self, code="000", message="Error"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} -> {self.message}'

class AccountsPayableService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.accounts_payable_repository = AccountsPayableRepository()
        self.companies_repository = CompaniesRepository()
        self.documents_repository = DocumentsRepository()
        self.movements_repository = MovementsRepository()
        self.suppliers_repository = SuppliersRepository()
        self.rules_repository = RulesRepository()
        self.user_repository = UsersRepository()

    def make_transaction(self, movement_date, company_id, supplier_id, document_number, rule_id, amount, issue_date, due_date, reference, user_id):
        self.logger.debug("start make_transaction")
        self.logger.debug(f'movement_date : {movement_date}')
        self.logger.debug(f'company_id : {company_id}')
        self.logger.debug(f'supplier_id : {supplier_id}')
        self.logger.debug(f'document_number : {document_number}')
        self.logger.debug(f'rule_id : {rule_id}')
        self.logger.debug(f'amount : {amount}')
        self.logger.debug(f'issue_date : {issue_date}')
        self.logger.debug(f'due_date : {due_date}')
        self.logger.debug(f'reference : {reference}')
        self.logger.debug(f'user_id : {user_id}')

        try:
            theComp = self.companies_repository.get_company_by_id(company_id)
            theSupp = self.suppliers_repository.get_supplier_by_id(supplier_id)
            theRule = self.rules_repository.get_rule_by_id(rule_id)
            theUser = self.user_repository.get_user_by_id(user_id)
            document = self.documents_repository.get_document_by_id(company_id, supplier_id, document_number)

            self.__validate_data(theComp, theSupp, theRule, theUser, document, document_number, amount, issue_date, due_date, reference)


            self.logger.debug("finish make_transaction")
            return self.accounts_payable_repository.make_transaction(theComp, theSupp, theRule, theUser, document, movement_date, document_number, amount, issue_date, due_date, reference)
        except AccountsPayableServiceException as compSerExpto:
            raise AccountsPayableServiceException(code=compSerExpto.code, message=compSerExpto.message)


    def __validate_data(self, theComp, theSupp, theRule, theUser, document, document_number, amount, issue_date, due_date, reference):
        if theComp is None:
            self.logger.debug("Company not found")
            raise AccountsPayableServiceException(code="100", message="Company not found")

        if theSupp is None:
            self.logger.debug("Supplier not found")
            raise AccountsPayableServiceException(code="100", message="Supplier not found")

        if theRule is None:
            self.logger.debug("Rule not found")
            raise AccountsPayableServiceException(code="100", message="Rule not found")

        if theUser is None:
            self.logger.debug("User not found")
            raise AccountsPayableServiceException(code="100", message="User not found")

        if not validators.length(document_number, min=2, max=12):
            self.logger.debug("The document_number is invalid")
            raise AccountsPayableServiceException(code="100", message="The document_number is invalid")

        if not self.__is_numeric(val=amount):
            self.logger.debug("The amount is invalid")
            raise AccountsPayableServiceException(code="100", message="The amount must to be a numeric value like follow: 1.10")

        try:
            self.__date_validate(date_text=issue_date)
        except ValueError as errorValue:
            self.logger.debug("The issue_date is invalid")
            raise AccountsPayableServiceException(code="100", message="Incorrect issue_date format, should be YYYY-MM-DD")

        if due_date is not None:
            try:
                self.__date_validate(date_text=due_date)
            except ValueError as errorValue:
                self.logger.debug("The due_date is invalid")
                raise AccountsPayableServiceException(code="100", message="Incorrect due_date format, should be YYYY-MM-DD")

        if theRule.update_due_date is 'Y':
            try:
                self.__date_validate(date_text=due_date)
            except ValueError as errorValue:
                self.logger.debug("The due_date is invalid")
                raise AccountsPayableServiceException(code="100", message="Incorrect due_date format, should be YYYY-MM-DD")

        if theRule.update_reference is 'Y' and not validators.length(reference, min=2, max=12):
            self.logger.debug("The reference is invalid")
            raise AccountsPayableServiceException(code="100", message="The reference is invalid")

        if theRule.action_over_document is 'C' and document is not None:
            self.logger.debug("The document exist")
            raise AccountsPayableServiceException(code="100", message="The document exist, please provide new document_number")

        if theRule.action_over_document is 'U' and document is None:
            self.logger.debug("The document not exist")
            raise AccountsPayableServiceException(code="100", message="The document not exist, please provide a document_number that exist for the company_id and supplier_id")

        return True

    def __date_validate(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return True

    def __is_numeric(self, val):
        if str(val).isdigit():
            return True
        elif str(val).replace('.','',1).isdigit():
            return True
        else:
            return False
