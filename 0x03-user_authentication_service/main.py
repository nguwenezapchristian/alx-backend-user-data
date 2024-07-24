#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Register a user."""
    url = "http://127.0.0.1:5000/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    assert response.json() == {
        "email": email, "message": "user created"}, \
        f"Unexpected response payload: {response.json()}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Register a user."""
    url = "http://127.0.0.1:5000/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 401, \
        f"Expected 401 but got {response.status_code}"


def log_in(email: str, password: str) -> str:
    """Register a user."""
    url = "http://127.0.0.1:5000/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    return response.json().get("session_id")


def profile_unlogged() -> None:
    """Register a user."""
    url = "http://127.0.0.1:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403, \
        f"Expected 403 but got {response.status_code}"


def profile_logged(session_id: str) -> None:
    """Register a user."""
    url = "http://127.0.0.1:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"


def log_out(session_id: str) -> None:
    """Register a user."""
    url = "http://127.0.0.1:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"


def reset_password_token(email: str) -> str:
    """Register a user."""
    url = "http://127.0.0.1:5000/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"
    return response.json().get("reset_token")


def update_password(
        email: str,
        reset_token: str,
        new_password: str) -> None:
    """Register a user."""
    url = "http://127.0.0.1:5000/reset_password"
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    response = requests.put(url, data=payload)
    assert response.status_code == 200, \
        f"Expected 200 but got {response.status_code}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    """Main function"""
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
