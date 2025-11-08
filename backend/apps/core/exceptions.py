"""
Custom exception handler for DRF to provide consistent error responses.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides RFC 7807 Problem Details format.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the error response format
        custom_response_data = {
            'error': {
                'status': response.status_code,
                'title': get_error_title(response.status_code),
                'detail': response.data.get('detail', str(exc)),
                'errors': response.data if isinstance(response.data, dict) else None,
            }
        }
        response.data = custom_response_data

    return response


def get_error_title(status_code):
    """Get human-readable error title from status code."""
    titles = {
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        409: 'Conflict',
        410: 'Gone',
        415: 'Unsupported Media Type',
        422: 'Unprocessable Entity',
        429: 'Too Many Requests',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
    }
    return titles.get(status_code, 'Error')
