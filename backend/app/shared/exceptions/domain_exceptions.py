class DomainException(Exception):
    status_code: int = 400

    def __init__(self,  message: str):
        super().__init__(message)
        self.message = message


class NotFound(DomainException):
    status_code = 404


class Conflict(DomainException):
    status_code = 409


class Unauthorized(DomainException):
    status_code = 401


class InvalidDataException(DomainException):
    status_code = 422


class ExternalServiceException(DomainException):
    status_code = 503

