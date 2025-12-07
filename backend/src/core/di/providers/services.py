from dishka import Provider, Scope, provide

from application.common.idp import IdentityProvider


class ServicesProvider(Provider):
    identity_provider = provide(IdentityProvider, scope=Scope.REQUEST)
