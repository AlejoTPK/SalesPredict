class DomainException(Exception):
    """Base exception for all domain-level errors."""

    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail


class NotFoundError(DomainException):
    status_code = 404
    detail = "Resource not found"


class ConflictError(DomainException):
    status_code = 409
    detail = "Resource conflict"


class ValidationError(DomainException):
    status_code = 422
    detail = "Validation error"


class UnauthorizedError(DomainException):
    status_code = 401
    detail = "Authentication required"


class ForbiddenError(DomainException):
    status_code = 403
    detail = "Permission denied"


class PredictionError(DomainException):
    status_code = 422
    detail = "Prediction could not be completed"
