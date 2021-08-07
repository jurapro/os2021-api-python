from rest_framework.exceptions import APIException
from rest_framework.response import Response


class CafeAPIException(APIException):

    def __init__(self, message=None, code=None):
        self.status_code = code
        response = {
            'error': {
                'code': code,
                'message': message
            }
        }
        self.detail = response


class CafeValidationAPIException(APIException):

    def __init__(self, message=None, code=None, errors=None):
        self.status_code = code
        response = {
            'error': {
                'code': code,
                'message': message,
                'errors': errors
            }
        }
        self.detail = response
