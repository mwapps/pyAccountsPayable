import logging
from sqlalchemy import exc, asc
from ..domains.rules import Rule
from ..repositories.db.database import RuleDb, db

class RulesRepository:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        data = []
        rules = RuleDb.query.order_by(asc(RuleDb.rule_description)).all()
        if rules is not None:
            for theRule in rules:
                data.append(Rule(theRule.rule_id, theRule.rule_description, theRule.action_over_document, theRule.movement_type, theRule.update_issue_date, theRule.update_due_date, theRule.update_reference))
        return data

    def get_rule_by_id(self, id):
        self.logger.debug(f'the id is: {id}')

        theRule = RuleDb.query.get(id)

        if theRule is None:
            return None
        else:
            return Rule(theRule.rule_id, theRule.rule_description, theRule.action_over_document, theRule.movement_type, theRule.update_issue_date, theRule.update_due_date, theRule.update_reference)

    def create_rule(self, rule_description, action_over_document, movement_type, update_issue_date, update_due_date, update_reference):
        self.logger.debug('create_Rule')

        try:
            newRule = RuleDb(rule_description=rule_description, action_over_document=action_over_document, movement_type=movement_type, update_issue_date=update_issue_date, update_due_date=update_due_date, update_reference=update_reference)
            db.session.add(newRule)
            db.session.commit()

            return Rule(newRule.rule_id, newRule.rule_description, newRule.action_over_document, newRule.movement_type, newRule.update_issue_date, newRule.update_due_date, newRule.update_reference)
        except exc.SQLAlchemyError as error:
            self.logger.error(error)
            return None

    def update_rule(self, id, rule_description, action_over_document, movement_type, update_issue_date, update_due_date, update_reference):
        self.logger.debug('update_rule')

        try:
            theRule = RuleDb.query.get(id)
            theRule.rule_description = rule_description
            theRule.action_over_document = action_over_document
            theRule.movement_type = movement_type
            theRule.update_issue_date = update_issue_date
            theRule.update_due_date = update_due_date
            theRule.update_reference = update_reference
            db.session.commit()
            return Rule(theRule.rule_id, theRule.rule_description, theRule.action_over_document, theRule.movement_type, theRule.update_issue_date, theRule.update_due_date, theRule.update_reference)
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return None

    def delete_rule(self, id):
        self.logger.debug('delete_rule')

        try:
            deleteComp = RuleDb.query.get(id)
            db.session.delete(deleteComp)
            db.session.commit()
            return True
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return False
