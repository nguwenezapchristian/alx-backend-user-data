#!/usr/bin/env python3
""" Auth module
"""
from db import DB
from user import User
from bcrypt import gensalt, hashpw, checkpw
from sqlalchemy.orm.exc import NoResultFound


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
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            """ User not found, proceed with registration """
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False
