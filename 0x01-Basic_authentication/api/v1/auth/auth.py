#!/usr/bin/env python3
"""
Module to manage the API authentication.
"""
from typing import List
from flask import request


class Auth():
    """ A class to manage the API authentication """

    def __init__(self) -> None:
        """ init method """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ public method require authentification """
        return False

    def authorization_header(self, request=None) -> str:
        """ public method authorization header """
        return None

    def current_user(self, request=None) -> str:
        """ Public method to get current user """
        return None
