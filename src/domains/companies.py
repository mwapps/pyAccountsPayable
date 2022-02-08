
class Company:
    def __init__(self, company_id, business_name):
        self.company_id = company_id
        self.business_name = business_name
    
    def __str__(self):
        return '{"' \
        + 'company_id' + '": ' + str(self.company_id) + ',"' \
        + 'business_name' + '": "' + self.business_name + '"}'

    def jsonObject(self):
        return {
            'company_id': self.company_id,
            'business_name': self.business_name
        }
