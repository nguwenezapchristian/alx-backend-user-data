#!/usr/bin/env python3
"""
a class BasicAuth that inherits from Auth
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """ a class BasicAuth that inherits from Auth """

    def __init__(self) -> None:
        """ Initializaion Method """
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 encoded part from a Basic Authorization header.

        Args:
            authorization_header (str): The Authorization header value.

        Returns:
            str: The Base64 encoded part of the header (excluding "Basic "),
            or None if the format is invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ A method that returns the decoded value of a Base64 string """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_auth = base64.b64decode(base64_authorization_header)
            return decoded_auth.decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ A method that returns the user email and password from
        the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(":")
        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ A method that returns the User instance
        based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.all()
        if not users:
            return None
        user = User.search({"email": user_email})
        if not user:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the authenticated user from a request.

        Args:
            request (object, optional): The request object (default: None).

        Returns:
            TypeVar('User'): The User instance if authenticated,
            otherwise None.
        """

        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')
        base64_auth = self.extract_base64_authorization_header(
            authorization_header)

        if not base64_auth:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)

        if not decoded_auth:
            return None

        email, password = self.extract_user_credentials(decoded_auth)

        if not email or not password:
            return None

        return self.user_object_from_credentials(email, password)
