import re
import decimal

class Document:
    def __init__(self, company_id, supplier_id, document_number, issue_date, due_date, reference, previous_balance, total_debits, total_credits, company, supplier):
        self.company_id = company_id
        self.supplier_id = supplier_id
        self.document_number = document_number
        self.issue_date = issue_date
        self.due_date = due_date
        self.reference = reference
        self.previous_balance = self.__get_money_value(previous_balance)
        self.total_debits = self.__get_money_value(total_debits)
        self.total_credits = self.__get_money_value(total_credits)

        self.company = company
        self.supplier = supplier
    
    def __str__(self):
        return '{"' \
        + 'company_id' + '": ' + str(self.company_id) + ',"' \
        + 'supplier_id' + '": "' + self.supplier_id + ',"}'  \
        + 'document_number' + '": "' + self.document_number + '"}'

    def jsonObject(self):
        return {
            #'company_id': self.company_id,
            #'supplier_id': self.supplier_id,
            'document_number': self.document_number,
            'issue_date': self.issue_date,
            'due_date': self.due_date,
            'reference': self.reference,
            'previous_balance': self.previous_balance,
            'total_debits': self.total_debits,
            'total_credits': self.total_credits,
            'company': self.company.jsonObject(),
            'supplier': self.supplier.jsonObject(),
            'balance': self.previous_balance + self.total_debits - self.total_credits
        }

    def __get_money_value(self, theValue):
        if theValue is None:
            return 0
        else:
            m = re.match(r"\$([\d.]+)", theValue)
            if m:
                theValue = decimal.Decimal(m.group(1))
        return theValue
