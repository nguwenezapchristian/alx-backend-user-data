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
        if path is None or excluded_paths is None:
            return True

        no_slash_path = path.rstrip('/')
        for excluded_path in excluded_paths:
            no_slash_excluded_path = excluded_path.rstrip('/')
            if no_slash_path == no_slash_excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ public method authorization header """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        else:
            return None

    def current_user(self, request=None) -> str:
        """ Public method to get current user """
        return None
