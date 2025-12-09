from dataclasses import dataclass

from application.common.errors.base import ApplicationError


@dataclass(eq=False)
class EmailAlreadyRegistered(ApplicationError):
    @property
    def title(self) -> str:
        return "Email Already Registered"


@dataclass(eq=False)
class UserNotFound(ApplicationError):
    by: str

    @property
    def title(self) -> str:
        return f"User not found by {self.by}"


@dataclass(eq=False)
class CredMismatch(ApplicationError):
    @property
    def title(self) -> str:
        return "Credentials Mismatch"


@dataclass(eq=False)
class UnauthorizedError(ApplicationError):
    @property
    def title(self) -> str:
        return "Unauthorized"
