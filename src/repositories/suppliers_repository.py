import logging
from sqlalchemy import exc, asc
from ..domains.suppliers import Supplier
from ..repositories.db.database import SupplierDb, db

class SuppliersRepository:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        data = []
        suppliers = SupplierDb.query.order_by(asc(SupplierDb.supplier_name)).all()
        if suppliers is not None:
            for supplier in suppliers:
                data.append(Supplier(supplier.supplier_id, supplier.supplier_name))
        return data

    def get_supplier_by_id(self, id):
        self.logger.debug(f'the id is: {id}')

        theSupplier = SupplierDb.query.get(id)

        if theSupplier is None:
            return None
        else:
            return Supplier(theSupplier.supplier_id, theSupplier.supplier_name)

    def create_supplier(self, supplier_name):
        self.logger.debug('create_Supplier')

        try:
            newSupplier = SupplierDb(supplier_name=supplier_name)
            db.session.add(newSupplier)
            db.session.commit()

            return Supplier(newSupplier.supplier_id, newSupplier.supplier_name)
        except exc.SQLAlchemyError:
            return None

    def update_supplier(self, id, supplier_name):
        self.logger.debug('update_Supplier')

        try:
            theSupplier = SupplierDb.query.get(id)
            theSupplier.supplier_name = supplier_name
            db.session.commit()
            return Supplier(theSupplier.supplier_id, theSupplier.supplier_name)
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return None

    def delete_supplier(self, id):
        self.logger.debug('delete_Supplier')

        try:
            deleteComp = SupplierDb.query.get(id)
            db.session.delete(deleteComp)
            db.session.commit()
            return True
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return False
