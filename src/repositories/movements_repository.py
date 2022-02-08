import logging
from sqlalchemy import exc, asc, and_, or_
from ..domains.movements import Movement
from ..domains.companies import Company
from ..domains.suppliers import Supplier
from ..domains.rules import Rule
from ..domains.users import User
from ..repositories.db.database import MovementDb, db

class MovementsRepository:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all_by_date(self):
        self.logger.debug("get_all_by_date")
        data = []
        movements = MovementDb.query.order_by(asc(MovementDb.movement_date)).all()
        if movements is not None:
            for theMovement in movements:
                data.append(self.__get_domain_object(theMovement=theMovement))
        return data

    def get_all_by_company_supplier(self):
        self.logger.debug("get_all_by_company_supplier")
        data = []
        movements = MovementDb.query.order_by(asc(MovementDb.company_id), asc(MovementDb.supplier_id), asc(MovementDb.movement_date)).all()
        if movements is not None:
            for theMovement in movements:
                data.append(self.__get_domain_object(theMovement=theMovement))
        return data

    def get_movement_by_id(self, movement_id):
        self.logger.debug(f'the key is: {movement_id}')

        theMovement = MovementDb.query.get(movement_id)

        if theMovement is None:
            return None
        else:
            return self.__get_domain_object(theMovement=theMovement)

    def get_movements_by_filters(self, company_id, supplier_id, document_number, rule_id, from_date, to_date):
        self.logger.debug(f'the key is: {company_id}, {supplier_id}, {document_number}, {rule_id}, {from_date}, {to_date}')

        data = []
        movements = MovementDb.query.filter(
            and_(
                or_(MovementDb.company_id==company_id, company_id==-1),
                or_(MovementDb.supplier_id==supplier_id, supplier_id==-1),
                or_(MovementDb.rule_id==rule_id, rule_id==-1),
                or_(MovementDb.document_number==document_number, document_number=='-1'),
                and_(MovementDb.movement_date>=from_date,MovementDb.movement_date<=to_date)
                )
            ).order_by(asc(MovementDb.movement_date), asc(MovementDb.company_id), asc(MovementDb.supplier_id)).all()
        if movements is not None:
            data = list(map(lambda theMovement: self.__get_domain_object(theMovement=theMovement), movements))
        return data

    def create_movement(self, movement_date, company_id, supplier_id, document_number, rule_id, amount, issue_date, due_date, reference, user_id):
        self.logger.debug('create_movement')

        try:
            theMovement = MovementDb(movement_date=movement_date, company_id=company_id, supplier_id=supplier_id, document_number=document_number, rule_id=rule_id, amount=amount, issue_date=issue_date, due_date=due_date, reference=reference, user_id=user_id)
            db.session.add(theMovement)
            db.session.commit()
            return self.__get_domain_object(theMovement=theMovement)

        except exc.SQLAlchemyError as error:
            self.logger.error(error.__str__())
            return None

    def __get_domain_object(self, theMovement):
            return Movement(theMovement.movement_id, theMovement.movement_date, theMovement.company_id, theMovement.supplier_id, theMovement.document_number, theMovement.rule_id, theMovement.amount, theMovement.issue_date, theMovement.due_date, theMovement.reference, theMovement.user_id, Company(theMovement.company.company_id, theMovement.company.business_name), Supplier(theMovement.supplier.supplier_id, theMovement.supplier.supplier_name), Rule(theMovement.rule.rule_id, theMovement.rule.rule_description, theMovement.rule.action_over_document, theMovement.rule.movement_type, theMovement.rule.update_issue_date, theMovement.rule.update_due_date, theMovement.rule.update_reference), User(theMovement.user.user_id, theMovement.user.user_name, theMovement.user.user_email, None))
