import logging
from sqlalchemy import exc, asc, and_, or_
from ..domains.documents import Document
from ..domains.companies import Company
from ..domains.suppliers import Supplier
from ..repositories.companies_repository import CompaniesRepository
from ..repositories.suppliers_repository import SuppliersRepository
from ..repositories.db.database import DocumentDb, db

class DocumentsRepository:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.companies_repository = CompaniesRepository()
        self.suppliers_repository = SuppliersRepository()

    def get_all(self):
        data = []
        documents = DocumentDb.query.order_by(asc(DocumentDb.company_id), asc(DocumentDb.supplier_id), asc(DocumentDb.due_date)).all()
        if documents is not None:
            data = list(map(lambda theDocument: self.__get_domain_object(theDocument=theDocument), documents))
        return data

    def get_documents_by_supplier(self, supplier_id):
        data = []
        documents = DocumentDb.query.filter_by(supplier_id=supplier_id).order_by(asc(DocumentDb.company_id), asc(DocumentDb.due_date))
        if documents is not None:
            data = list(map(lambda theDocument: self.__get_domain_object(theDocument=theDocument), documents))
        return data

    def get_document_by_id(self, company_id, supplier_id, document_number):
        self.logger.debug(f'the key is: {company_id}, {supplier_id}, {document_number}')

        theDocument = DocumentDb.query.get((company_id, supplier_id, document_number))

        if theDocument is None:
            return None
        else:
            return self.__get_domain_object(theDocument=theDocument)

    def get_document_by_filters(self, company_id, supplier_id, document_number, from_date, to_date):
        self.logger.debug(f'the key is: {company_id}, {supplier_id}, {document_number}, {from_date}, {to_date}')

        data = []
        documents = DocumentDb.query.filter(
            and_(
                or_(DocumentDb.company_id==company_id, company_id==-1),
                or_(DocumentDb.supplier_id==supplier_id, supplier_id==-1),
                or_(DocumentDb.document_number==document_number, document_number=='-1'),
                and_(DocumentDb.due_date>=from_date,DocumentDb.due_date<=to_date)
                )
            ).order_by(asc(DocumentDb.company_id), asc(DocumentDb.supplier_id), asc(DocumentDb.due_date)).all()
        if documents is not None:
            data = list(map(lambda theDocument: self.__get_domain_object(theDocument=theDocument), documents))
        return data

    def create_document(self, company_id, supplier_id, document_number, issue_date, due_date, reference, previous_balance, total_debits, total_credits):
        self.logger.debug('create_document')

        try:
            theDocument = DocumentDb(company_id=company_id, supplier_id=supplier_id, document_number=document_number, issue_date=issue_date, due_date=due_date, reference=reference, previous_balance=previous_balance, total_debits=total_debits, total_credits=total_credits)
            db.session.add(theDocument)
            db.session.commit()

            return self.__get_domain_object(theDocument=theDocument)
        except exc.SQLAlchemyError as error:
            self.logger.error(error.__str__())
            return None

    def update_document(self, company_id, supplier_id, document_number, issue_date, due_date, reference, previous_balance, total_debits, total_credits):
        self.logger.debug('update_document')

        try:
            theDocument = DocumentDb.query.get(company_id, supplier_id, document_number)
            theDocument.issue_date = issue_date
            theDocument.due_date = due_date
            theDocument.reference = reference
            theDocument.previous_balance = previous_balance
            theDocument.total_debits = total_debits
            theDocument.total_credits = total_credits
            db.session.commit()

            return self.__get_domain_object(theDocument=theDocument)
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return None

    def __get_domain_object(self, theDocument):
            return Document(theDocument.company_id, theDocument.supplier_id, theDocument.document_number, theDocument.issue_date, theDocument.due_date, theDocument.reference, theDocument.previous_balance, theDocument.total_debits, theDocument.total_credits, self.companies_repository.get_company_by_id(theDocument.company_id), self.suppliers_repository.get_supplier_by_id(theDocument.supplier_id))
