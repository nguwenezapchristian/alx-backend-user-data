#!/usr/bin/env python3
"""
Auth module
"""
from bcrypt import gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """Hash a password for storing."""
    return hashpw(password.encode(), gensalt())
