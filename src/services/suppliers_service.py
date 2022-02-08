import logging
import validators
from ..repositories.suppliers_repository import SuppliersRepository

class SuppliersServiceException(Exception):
    def __init__(self, code="000", message="Error"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} -> {self.message}'

class SuppliersService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.suppliers_repository = SuppliersRepository()

    def get_all(self):
        return self.suppliers_repository.get_all()

    def create_supplier(self, supplier_name):
        self.logger.debug(f'supplier_name: {supplier_name}')

        if not validators.length(supplier_name, min=2, max=50):
            self.logger.debug("The supplier_name is invalid")
            raise SuppliersServiceException(code="010", message="The supplier_name is invalid")

        return self.suppliers_repository.create_supplier(supplier_name=supplier_name)

    def update_supplier(self, id, supplier_name):
        self.logger.debug(f'data: {id}, {supplier_name}')

        if self.get_supplier_by_id(id=id) is None:
            self.logger.debug("Supplier not found")
            raise SuppliersServiceException(code="020", message="Supplier not found")

        if not validators.length(supplier_name, min=2, max=50):
            self.logger.debug("The supplier_name is invalid")
            raise SuppliersServiceException(code="020", message="The supplier_name is invalid")

        return self.suppliers_repository.update_supplier(id=id, supplier_name=supplier_name)

    def delete_supplier(self, id):
        self.logger.debug(f'data: {id}')

        if self.get_supplier_by_id(id=id) is None:
            self.logger.debug("Supplier not found")
            raise SuppliersServiceException(code="020", message="Supplier not found")

        return self.suppliers_repository.delete_supplier(id=id)

    def get_supplier_by_id(self, id):
        self.logger.debug(f'id: {id}')
        return self.suppliers_repository.get_supplier_by_id(id)
