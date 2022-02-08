import logging
import validators
from ..repositories.rules_repository import RulesRepository

class RulesServiceException(Exception):
    def __init__(self, code="000", message="Error"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} -> {self.message}'

class RulesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rules_repository = RulesRepository()

    def get_all(self):
        return self.rules_repository.get_all()

    def create_rule(self, rule_description, action_over_document, movement_type, update_issue_date, update_due_date, update_reference):
        self.logger.debug(f'rule_description: {rule_description}')

        if not validators.length(rule_description, min=2, max=50):
            self.logger.debug("The rule_description is invalid")
            raise RulesServiceException(code="010", message="The rule_description is invalid")

        if action_over_document not in ('C', 'U', 'A'):
            self.logger.debug("The action_over_document is invalid")
            raise RulesServiceException(code="010", message="The action_over_document only can be 'C', 'U', 'A'")

        if movement_type not in ('D', 'C', 'N'):
            self.logger.debug("The movement_type is invalid")
            raise RulesServiceException(code="010", message="The movement_type only can be 'D', 'C', 'N'")

        if update_issue_date not in ('Y', 'N'):
            self.logger.debug("The update_issue_date is invalid")
            raise RulesServiceException(code="010", message="The update_issue_date only can be 'Y', 'N'")

        if update_due_date not in ('Y', 'N'):
            self.logger.debug("The update_due_date is invalid")
            raise RulesServiceException(code="010", message="The update_due_date only can be 'Y', 'N'")

        if update_reference not in ('Y', 'N'):
            self.logger.debug("The update_reference is invalid")
            raise RulesServiceException(code="010", message="The update_reference only can be 'Y', 'N'")

        return self.rules_repository.create_rule(rule_description=rule_description, action_over_document=action_over_document, movement_type=movement_type, update_issue_date=update_issue_date, update_due_date=update_due_date, update_reference=update_reference)

    def update_rule(self, id, rule_description, action_over_document, movement_type, update_issue_date, update_due_date, update_reference):
        self.logger.debug(f'data: {id}, {rule_description}')

        if self.get_rule_by_id(id=id) is None:
            self.logger.debug("Rule not found")
            raise RulesServiceException(code="020", message="Rule not found")

        if not validators.length(rule_description, min=2, max=50):
            self.logger.debug("The rule_description is invalid")
            raise RulesServiceException(code="010", message="The rule_description is invalid")

        if action_over_document not in ('C', 'U', 'A'):
            self.logger.debug("The action_over_document is invalid")
            raise RulesServiceException(code="010", message="The action_over_document only can be 'C', 'U', 'A'")

        if movement_type not in ('D', 'C', 'N'):
            self.logger.debug("The movement_type is invalid")
            raise RulesServiceException(code="010", message="The movement_type only can be 'D', 'C', 'N'")

        if update_issue_date not in ('Y', 'N'):
            self.logger.debug("The update_issue_date is invalid")
            raise RulesServiceException(code="010", message="The update_issue_date only can be 'Y', 'N'")

        if update_due_date not in ('Y', 'N'):
            self.logger.debug("The update_due_date is invalid")
            raise RulesServiceException(code="010", message="The update_due_date only can be 'Y', 'N'")

        if update_reference not in ('Y', 'N'):
            self.logger.debug("The update_reference is invalid")
            raise RulesServiceException(code="010", message="The update_reference only can be 'Y', 'N'")

        return self.rules_repository.update_rule(id=id, rule_description=rule_description, action_over_document=action_over_document, movement_type=movement_type, update_issue_date=update_issue_date, update_due_date=update_due_date, update_reference=update_reference)

    def delete_rule(self, id):
        self.logger.debug(f'data: {id}')

        if self.get_rule_by_id(id=id) is None:
            self.logger.debug("Rule not found")
            raise RulesServiceException(code="020", message="Rule not found")

        return self.rules_repository.delete_rule(id=id)

    def get_rule_by_id(self, id):
        self.logger.debug(f'id: {id}')
        return self.rules_repository.get_rule_by_id(id)
