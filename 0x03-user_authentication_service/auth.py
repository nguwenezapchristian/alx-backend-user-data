from db import DB
from user import User
from bcrypt import gensalt, hashpw
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password for storing."""
        return hashpw(password.encode(), gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Register a user."""
        try:
            if self._db.find_user_by(email=email) is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            """No user found, proceed to register """
            pass

        hashed_password = self._hash_password(password)
        return self._db.add_user(email, hashed_password)
