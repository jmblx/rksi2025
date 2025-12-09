from dishka import Provider, Scope, provide
from fastapi import Request

from application.common.idp import AccessToken


class PresentationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AccessToken)
    def provide_session(self, request: Request) -> AccessToken:
        token = request.headers.get("authorization")
        if token is None:
            return AccessToken("")
        return AccessToken(token)
