#!/usr/bin/env python3
"""
a class BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth


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
        if authorization_header is not isinstance(str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]
