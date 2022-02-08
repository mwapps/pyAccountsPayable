import logging
import validators
from ..repositories.companies_repository import CompaniesRepository

class CompaniesServiceException(Exception):
    def __init__(self, code="000", message="Error"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} -> {self.message}'

class CompaniesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.companies_repository = CompaniesRepository()

    def get_all(self):
        return self.companies_repository.get_all()

    def create_company(self, business_name):
        self.logger.debug(f'business_name: {business_name}')

        if not validators.length(business_name, min=2, max=50):
            self.logger.debug("The business_name is invalid")
            raise CompaniesServiceException(code="010", message="The business_name is invalid")

        return self.companies_repository.create_company(business_name=business_name)

    def update_company(self, id, business_name):
        self.logger.debug(f'data: {id}, {business_name}')

        if self.get_company_by_id(id=id) is None:
            self.logger.debug("Company not found")
            raise CompaniesServiceException(code="020", message="Company not found")

        if not validators.length(business_name, min=2, max=50):
            self.logger.debug("The business_name is invalid")
            raise CompaniesServiceException(code="020", message="The business_name is invalid")

        return self.companies_repository.update_company(id=id, business_name=business_name)

    def delete_company(self, id):
        self.logger.debug(f'data: {id}')

        if self.get_company_by_id(id=id) is None:
            self.logger.debug("Company not found")
            raise CompaniesServiceException(code="020", message="Company not found")

        return self.companies_repository.delete_company(id=id)

    def get_company_by_id(self, id):
        self.logger.debug(f'id: {id}')
        return self.companies_repository.get_company_by_id(id)
