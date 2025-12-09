from dataclasses import dataclass

from application.common.errors.base import ApplicationError


@dataclass(eq=False)
class UserNotFoundError(ApplicationError):
    by: str

    @property
    def title(self) -> str:
        return f"User not found by {self.by}"


@dataclass(eq=False)
class UnauthorizedError(ApplicationError):
    @property
    def title(self) -> str:
        return "Unauthorized"


@dataclass(eq=False)
class EmailCodeMismatchError(ApplicationError):
    @property
    def title(self) -> str:
        return "invalid email code"


@dataclass(eq=False)
class InvalidDocumentError(ApplicationError):
    @property
    def title(self) -> str:
        return "invalid document error"
