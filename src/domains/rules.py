
class Rule:
    def __init__(self, rule_id, rule_description, action_over_document, movement_type, update_issue_date, update_due_date, update_reference):
        self.rule_id = rule_id
        self.rule_description=rule_description
        self.action_over_document=action_over_document
        self.movement_type=movement_type
        self.update_issue_date=update_issue_date
        self.update_due_date=update_due_date
        self.update_reference=update_reference

    def __str__(self):
        return '{"' \
        + 'rule_id' + '": ' + str(self.rule_id) + ',"' \
        + 'rule_description' + '": "' + self.rule_description + '"}'

    def jsonObject(self):
        return {
            'rule_id': self.rule_id,
            'rule_description': self.rule_description,
            'action_over_document': self.action_over_document,
            'movement_type': self.movement_type,
            'update_issue_date': self.update_issue_date,
            'update_due_date': self.update_due_date,
            'update_reference': self.update_reference,
        }

