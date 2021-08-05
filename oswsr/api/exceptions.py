from rest_framework.exceptions import APIException


class CafeAPIException(APIException):

    def __init__(self, message=None, code=None):
        self.status_code = code
        response = {
            'error': {
                'code': code,
                'message': message
            }
        }
        super().__init__(response, code)


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
        super().__init__(response, code)