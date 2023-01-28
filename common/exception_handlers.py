"""
Common project exception handlers.
"""
from http import HTTPStatus

from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler.
    """
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            response.data = {"status": HTTPStatus.BAD_REQUEST, "message": response.data}
        else:
            error_payload = {
                "error": {
                    "status_code": response.status_code,
                    "message": response.data["detail"],
                }
            }
            response.data = error_payload
    return response
