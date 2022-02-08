import re
import decimal

class Movement:
    def __init__(self, movement_id, movement_date, company_id, supplier_id, document_number, rule_id, amount, issue_date, due_date, reference, user_id, company, supplier, rule, user):
        self.movement_id = movement_id
        self.movement_date = movement_date
        self.company_id = company_id
        self.supplier_id = supplier_id
        self.document_number = document_number
        self.rule_id = rule_id
        self.amount = self.__get_money_value(amount)
        self.issue_date = issue_date
        self.due_date = due_date
        self.reference = reference
        self.user_id = user_id
    
        self.company = company
        self.supplier = supplier
        self.rule = rule
        self.user = user

    def __str__(self):
        return '{"' \
        + 'company_id' + '": ' + str(self.company_id) + ',"' \
        + 'supplier_id' + '": "' + self.supplier_id + ',"}'  \
        + 'document_number' + '": "' + self.document_number + '"}'

    def jsonObject(self):
        return {
            'movement_id': self.movement_id,
            'movement_date': self.movement_date,
            #'company_id': self.company_id,
            #'supplier_id': self.supplier_id,
            'document_number': self.document_number,
            #'rule_id': self.rule_id,
            'amount': self.amount,
            'issue_date': self.issue_date,
            'due_date': self.due_date,
            'reference': self.reference,
            #'user_id': self.user_id,
            'company': self.company.jsonObject(),
            'supplier': self.supplier.jsonObject(),
            'rule': self.rule.jsonObject(),
            'user': self.user.jsonObject()
        }

    def __get_money_value(self, theValue):
        if theValue is None:
            return 0
        else:
            m = re.match(r"\$([\d.]+)", theValue)
            if m:
                theValue = decimal.Decimal(m.group(1))
        return theValue
