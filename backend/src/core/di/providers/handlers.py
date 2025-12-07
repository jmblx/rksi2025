from dishka import Provider, Scope, provide

from application.auth.login_handler import LoginHandler
from application.auth.register_handler import RegisterHandler


class HandlerProvider(Provider):
    get_register_handler = provide(RegisterHandler, scope=Scope.REQUEST)
    get_login_handler = provide(LoginHandler, scope=Scope.REQUEST)
