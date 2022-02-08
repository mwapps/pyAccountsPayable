import logging
import validators
#from datetime import datetime
import datetime
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

class ReportsServiceException(Exception):
    def __init__(self, code="000", message="Error"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} -> {self.message}'

class ReportsService:
    YEARS = 100
    DAYS_PER_YEAR = 365.24

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.accounts_payable_repository = AccountsPayableRepository()
        self.companies_repository = CompaniesRepository()
        self.documents_repository = DocumentsRepository()
        self.movements_repository = MovementsRepository()
        self.suppliers_repository = SuppliersRepository()
        self.rules_repository = RulesRepository()
        self.user_repository = UsersRepository()

    def process_documents_reports(self, company_id, supplier_id, document_number, from_date, to_date):
        self.logger.debug("start process_documents_reports")

        today = datetime.datetime.now()
        hundred_years_before = today - datetime.timedelta(days=(self.YEARS*self.DAYS_PER_YEAR))
        hundred_years_later  = today + datetime.timedelta(days=(self.YEARS*self.DAYS_PER_YEAR))
        self.logger.debug(f'hundred_years_before : {hundred_years_before}')
        self.logger.debug(f'hundred_years_later : {hundred_years_later}')

        if not from_date:
            from_date_r = hundred_years_before.strftime('%Y-%m-%d')
        else:
            try:
                from_date_r = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            except ValueError as errorValue:
                self.logger.debug("The from_date is invalid")
                raise ReportsServiceException(code="100", message="Incorrect from_date format, should be YYYY-MM-DD")

        if not to_date:
            to_date_r = hundred_years_later.strftime('%Y-%m-%d')
        else:
            try:
                to_date_r = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            except ValueError as errorValue:
                self.logger.debug("The to_date is invalid")
                raise ReportsServiceException(code="100", message="Incorrect to_date format, should be YYYY-MM-DD")

        company_id_r = -1
        if self.__is_integer(company_id):
            company_id_r = int(company_id)
        supplier_id_r = -1
        if self.__is_integer(supplier_id):
            supplier_id_r = int(supplier_id)
        document_number_r = "-1"
        if document_number:
            document_number_r = document_number

        self.logger.debug(f'from_date_r : {from_date_r}')
        self.logger.debug(f'to_date_r   : {to_date_r}')

        self.logger.debug("finish process_documents_reports")
        return self.documents_repository.get_document_by_filters(company_id=company_id_r, supplier_id=supplier_id_r, document_number=document_number_r, from_date=from_date_r, to_date=to_date_r)

    def process_movements_reports(self, company_id, supplier_id, document_number, rule_id, from_date, to_date):
        self.logger.debug("start process_movements_reports")

        today = datetime.datetime.now()
        hundred_years_before = today - datetime.timedelta(days=(self.YEARS*self.DAYS_PER_YEAR))
        hundred_years_later  = today + datetime.timedelta(days=(self.YEARS*self.DAYS_PER_YEAR))
        self.logger.debug(f'hundred_years_before : {hundred_years_before}')
        self.logger.debug(f'hundred_years_later : {hundred_years_later}')

        if not from_date:
            from_date_r = hundred_years_before.strftime('%Y-%m-%d')
        else:
            try:
                from_date_r = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            except ValueError as errorValue:
                self.logger.debug("The from_date is invalid")
                raise ReportsServiceException(code="100", message="Incorrect from_date format, should be YYYY-MM-DD")

        if not to_date:
            to_date_r = hundred_years_later.strftime('%Y-%m-%d')
        else:
            try:
                to_date_r = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            except ValueError as errorValue:
                self.logger.debug("The to_date is invalid")
                raise ReportsServiceException(code="100", message="Incorrect to_date format, should be YYYY-MM-DD")

        company_id_r = -1
        if self.__is_integer(company_id):
            company_id_r = int(company_id)
        supplier_id_r = -1
        if self.__is_integer(supplier_id):
            supplier_id_r = int(supplier_id)
        rule_id_r = -1
        if self.__is_integer(rule_id):
            rule_id_r = int(rule_id)
        document_number_r = "-1"
        if document_number:
            document_number_r = document_number

        self.logger.debug(f'from_date_r : {from_date_r}')
        self.logger.debug(f'to_date_r   : {to_date_r}')

        self.logger.debug("finish process_movements_reports")
        return self.movements_repository.get_movements_by_filters(company_id=company_id_r, supplier_id=supplier_id_r, document_number=document_number_r, rule_id=rule_id_r, from_date=from_date_r, to_date=to_date_r)

    def __is_integer(self, val):
        if str(val).isdigit():
            return True
        else:
            return False
