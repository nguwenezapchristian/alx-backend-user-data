from db import DB
from user import User
from bcrypt import gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """Hash a password for storing."""
    return hashpw(password.encode(), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user."""
        if self._db.find_user_by(email=email) is not None:
            raise ValueError(f"User {email} already exists")

        return self._db.add_user(email, _hash_password(self, password))
