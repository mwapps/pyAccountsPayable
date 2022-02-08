import logging
import validators
from werkzeug.security import check_password_hash, generate_password_hash
from ..domains.users import User
from ..repositories.users_repository import UsersRepository
from ..libraries.utilities import current_milli_time

class UsersServiceException(Exception):
    def __init__(self, code="000", message="Error"):
        self.code = code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.code} -> {self.message}'

class UsersService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_repository = UsersRepository()

    def create_user(self, username, email, password):
        self.logger.debug(f'the user is: {username}, {email}')

        if len(password) < 6:
            self.logger.debug("The password is too short")
            raise UsersServiceException(code="010", message="The password is too short")

        if len(username) < 3:
            self.logger.debug("The username is too short")
            raise UsersServiceException(code="010", message="The username is too short")

        if not username.isalnum() or " " in username:
            self.logger.debug("Username should be alphanumeric, also no spaces")
            raise UsersServiceException(code="010", message="Username should be alphanumeric, also no spaces")

        if not validators.email(email):
            self.logger.debug("The email is invalid")
            raise UsersServiceException(code="010", message="The email is invalid")

        if self.get_user_by_email(email=email) is not None:
            self.logger.debug("The email is taken")
            raise UsersServiceException(code="010", message="The email is taken")

        if self.get_user_by_username(username=username) is not None:
            self.logger.debug("The username is taken")
            raise UsersServiceException(code="010", message="The username is taken")

        return self.user_repository.create_user(User(None, username, email, generate_password_hash(password)))


    def login_user(self, email, password):
        self.logger.debug('start login_user')

        theUser = self.get_user_by_email(email=email)
        if theUser is None:
            self.logger.debug("Email does not exist")
            raise UsersServiceException(code="015", message="Email does not exist")

        is_pass_correct = check_password_hash(theUser.user_pass, password)
        if not is_pass_correct:
            self.logger.debug("The credentials are not valid")
            raise UsersServiceException(code="015", message="The credentials are not valid")

        self.logger.debug('finish login_user')
        return theUser

    def delete_user(self, email):
        self.logger.debug('start delete_user')

        theUser = self.get_user_by_email(email=email)
        if theUser is None:
            self.logger.debug("Email does not exist")
            raise UsersServiceException(code="015", message="Email does not exist")

        # TODO: Incluir una validación si el usuario tiene movimientos, si es así, no podrá ser eliminado

        if self.remove_user(user_id=theUser.user_id) is False:
            self.logger.debug("User not deleted")
            raise UsersServiceException(code="015", message="The user was not delete, please try again")

        self.logger.debug('finish delete_user')
        return True

    def reset_password(self, user_id, old_password, new_password):
        self.logger.debug('start reset_password')
        theUser = self.get_user_by_id(id=user_id)
        if theUser is None:
            self.logger.debug("The id user does not exist")
            raise UsersServiceException(code="015", message="The id user does not exist")

        if len(new_password) < 6:
            self.logger.debug("The new_password is too short")
            raise UsersServiceException(code="010", message="The new_password is too short")

        if not check_password_hash(theUser.user_pass, old_password):
            self.logger.debug("The old_password does not match")
            raise UsersServiceException(code="015", message="The old_password does not match")

        if not self.change_password(user_id=user_id, new_password=generate_password_hash(new_password)):
            self.logger.debug("The password was not changed")
            raise UsersServiceException(code="015", message="The password was not changed, please try again")

        self.logger.debug('finish reset_password')
        return True

    def get_user_by_id(self, id):
        self.logger.debug(f'the id is: {id}')
        return self.user_repository.get_user_by_id(id)

    def get_user_by_email(self, email):
        self.logger.debug(f'the email is: {email}')
        return self.user_repository.get_user_by_email(email)

    def get_user_by_username(self, username):
        self.logger.debug(f'the username is: {username}')
        return self.user_repository.get_user_by_username(username)

    def remove_user(self, user_id):
        self.logger.debug(f'the id is: {user_id}')
        return self.user_repository.delete_user(user_id)

    def change_password(self, user_id, new_password):
        self.logger.debug(f'the id is: {user_id}')
        return self.user_repository.reset_password(user_id=user_id, new_password=new_password)
