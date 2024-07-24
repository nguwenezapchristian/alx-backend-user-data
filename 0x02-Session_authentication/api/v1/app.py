#!/usr/bin/env python3
""" API routes
"""
from flask import Flask, jsonify, request, abort
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.user_auth import UserAuth

app = Flask(__name__)
app.register_blueprint(app_views)

auth = None
auth_type = getenv("AUTH_TYPE")
if auth_type == "auth":
    auth = Auth()
elif auth_type == "session_auth":
    auth = SessionAuth()
elif auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "user_auth":
    auth = UserAuth()


@app.before_request
def before_request():
    """ Before request handler
    """
    if auth:
        excluded_paths = ['/api/v1/status/',
                          '/api/v1/unauthorized/',
                          '/api/v1/forbidden/',
                          '/api/v1/auth_session/login/']
        if auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None and \
               auth.session_cookie(request) is None:
                abort(401)


@app.errorhandler(404)
def not_found(error):
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
