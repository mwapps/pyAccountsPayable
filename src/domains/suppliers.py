
class Supplier:
    def __init__(self, supplier_id, supplier_name):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
    
    def __str__(self):
        return '{"' \
        + 'supplier_id' + '": ' + str(self.supplier_id) + ',"' \
        + 'supplier_name' + '": "' + self.supplier_name + '"}'

    def jsonObject(self):
        return {
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name
        }
