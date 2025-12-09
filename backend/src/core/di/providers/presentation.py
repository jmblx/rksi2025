from dishka import Provider, Scope, provide
from fastapi import Request

from application.common.idp import AccessToken, RefreshToken


class PresentationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AccessToken)
    def provide_access_token(self, request: Request) -> AccessToken:
        token = request.cookies.get("access_token")
        if token is None:
            return AccessToken("")
        return AccessToken(token)

    @provide(scope=Scope.REQUEST, provides=RefreshToken)
    def provide_refresh_token(self, request: Request) -> RefreshToken:
        token = request.cookies.get("refresh_token")
        if token is None:
            return RefreshToken("")
        return RefreshToken(token)

