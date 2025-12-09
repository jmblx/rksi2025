from dishka import Provider, Scope, provide

from application.auth.login_handler import LoginHandler


class HandlerProvider(Provider):
    get_login_handler = provide(LoginHandler, scope=Scope.REQUEST)
