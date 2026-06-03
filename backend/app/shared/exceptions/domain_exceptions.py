class DomainException(Exception):
    status_code: int = 400

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundException(DomainException):
    status_code = 404


class ConflictException(DomainException):
    status_code = 409


class UnauthorizedException(DomainException):
    status_code = 401


class InvalidDataException(DomainException):
    status_code = 422


class ExternalServiceException(DomainException):
    status_code = 503