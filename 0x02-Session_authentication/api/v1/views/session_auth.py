#!/usr/bin/env python3
""" Module of Session Authentication views """
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth
import os

auth = SessionAuth()


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Login session"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout session"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
