class ApiException(Exception):
    def __init__(self, message, status_code):
        # super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['code'] = self.status_code
        rv['message'] = self.message
        return rv
    

class NotImplementedException(ApiException):
    def __init__(self, message):
        super().__init__(message, status_code=501)


class NotFoundException(ApiException):
    def __init__(self, message) -> None:
        super().__init__(message, status_code=404)


class BadRequestException(ApiException):
    def __init__(self, message) -> None:
        super().__init__(message, status_code=400)

class ConflictException(ApiException):
    def __init__(self, message) -> None:
        super().__init__(message, status_code=409)