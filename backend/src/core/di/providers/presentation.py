from dishka import Provider, Scope, provide
from fastapi import Request

from application.common.idp import SessionHash


class PresentationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=SessionHash)
    def provide_session(self, request: Request) -> SessionHash:
        token = request.headers.get("authorization")
        if token is None:
            return SessionHash("")
        return SessionHash(token)
