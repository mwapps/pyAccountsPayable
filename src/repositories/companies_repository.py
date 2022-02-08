import logging
from sqlalchemy import exc, asc
from ..domains.companies import Company
from ..repositories.db.database import CompanyDb, db

class CompaniesRepository:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        data = []
        companies = CompanyDb.query.order_by(asc(CompanyDb.business_name)).all()
        if companies is not None:
            data = list(map(lambda company: Company(company.company_id, company.business_name), companies))
        return data

    def get_company_by_id(self, id):
        self.logger.debug(f'the id is: {id}')

        theCompany = CompanyDb.query.get(id)

        if theCompany is None:
            return None
        else:
            return Company(theCompany.company_id, theCompany.business_name)

    def create_company(self, business_name):
        self.logger.debug('create_company')

        try:
            newCompany = CompanyDb(business_name=business_name)
            db.session.add(newCompany)
            db.session.commit()

            return Company(newCompany.company_id, newCompany.business_name)
        except exc.SQLAlchemyError:
            return None

    def update_company(self, id, business_name):
        self.logger.debug('update_company')

        try:
            theCompany = CompanyDb.query.get(id)
            theCompany.business_name = business_name
            db.session.commit()
            return Company(theCompany.company_id, theCompany.business_name)
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return None

    def delete_company(self, id):
        self.logger.debug('delete_company')

        try:
            deleteComp = CompanyDb.query.get(id)
            db.session.delete(deleteComp)
            db.session.commit()
            return True
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return False
