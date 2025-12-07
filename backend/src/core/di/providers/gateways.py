from dishka import Provider, Scope, provide

from infrastructure.db.gateways.auth_gateway import AuthGateway


class GatewayProvider(Provider):
    get_auth_gateway = provide(AuthGateway, scope=Scope.REQUEST)
