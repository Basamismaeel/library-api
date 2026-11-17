"""Central error handling: one place that builds every error response."""
from flask import jsonify


class ApiError(Exception):
    """Raised anywhere in the app to produce an HTTP error response."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def error_response(message, status_code):
    """Build a JSON error response with a custom message and HTTP status code."""
    return jsonify({"error": message}), status_code


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(err):
        return error_response(err.message, err.status_code)
