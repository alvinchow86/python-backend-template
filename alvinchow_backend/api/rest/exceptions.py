from alvinchow.lib.exceptions import BaseException


class APIException(BaseException):
    status_code = 400

    def __init__(self, *args, status_code=None, error_code=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        obj = dict(message=self.message, code=self.error_code)
        if self.data:
            obj.update(self.data)
        return obj


class BadRequestError(APIException):
    status_code = 400


class ResourceNotFound(APIException):
    status_code = 404


class UnauthorizedError(APIException):
    status_code = 401


class ServerError(APIException):
    status_code = 500


class CSRFValidationError(APIException):
    status_code = 403
