from flask import Flask, jsonify
from app.shared.exceptions.domain_exceptions import DomainException

def register_error_handlers(app):
    @app.errorhandler(DomainException)
    def handle_domain_exception(error: DomainException):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(_error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_server_error(_error):
        return jsonify({"error": "Internal server error"}), 500