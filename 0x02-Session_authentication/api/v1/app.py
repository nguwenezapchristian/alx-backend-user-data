#!/usr/bin/env python3
"""
Main application module
"""
from os import getenv
from flask import Flask, jsonify, request, abort
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()
elif getenv("AUTH_TYPE") == "basic_auth":
    auth = BasicAuth()
elif getenv("AUTH_TYPE") == "session_exp_auth":
    auth = SessionExpAuth()
elif getenv("AUTH_TYPE") == "session_db_auth":
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """Before request handler"""
    if auth is None:
        return
    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/']):
        return
    if auth.authorization_header(request) is None and \
       auth.session_cookie(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error):
    """404 handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
