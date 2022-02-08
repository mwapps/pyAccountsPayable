import logging
from sqlalchemy import exc
from ..domains.users import User
from ..repositories.db.database import UserDb, db

class UsersRepository:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_user(self, user):
        self.logger.debug('create_user')

        try:
            newUser = UserDb(user_name=user.user_name, user_pass=user.user_pass, user_email=user.user_email)
            db.session.add(newUser)
            db.session.commit()

            return User(newUser.user_id, newUser.user_name, newUser.user_email, newUser.user_pass)
        except exc.SQLAlchemyError:
            return None

    def delete_user(self, user_id):
        self.logger.debug('delete_user')

        try:
            deleteUser = UserDb.query.get(user_id)
            db.session.delete(deleteUser)
            db.session.commit()
            return True
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return False

    def reset_password(self, user_id, new_password):
        self.logger.debug('delete_user')

        try:
            theUser = UserDb.query.get(user_id)
            theUser.user_pass = new_password
            db.session.commit()
            return True
        except exc.SQLAlchemyError as errorSQL:
            self.logger.error(errorSQL)
            return False

    def get_user_by_id(self, id):
        self.logger.debug(f'the id is: {id}')

        theUser = UserDb.query.get(id)

        if theUser is None:
            return None
        else:
            return User(theUser.user_id, theUser.user_name, theUser.user_email, theUser.user_pass)

    def get_user_by_email(self, email):
        self.logger.debug(f'the email is: {email}')

        theUser = UserDb.query.filter_by(user_email=email).first()

        if theUser is None:
            self.logger.debug(f'the user is None: {theUser}')
            return None
        else:
            return User(theUser.user_id, theUser.user_name, theUser.user_email, theUser.user_pass)

    def get_user_by_username(self, username):
        self.logger.debug(f'the username is: {username}')

        theUser = UserDb.query.filter_by(user_name=username).first()

        if theUser is None:
            return None
        else:
            return User(theUser.user_id, theUser.user_name, theUser.user_email, theUser.user_pass)
