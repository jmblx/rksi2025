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
        return "User not found by %s".format(self.by)


@dataclass(eq=False)
class PwdMismatch(ApplicationError):
    @property
    def title(self) -> str:
        return "Login password mismatch"
