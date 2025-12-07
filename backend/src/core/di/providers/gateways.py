from dishka import Provider, Scope, provide

from infrastructure.db.gateways.session_gateway import SessionGateway
from infrastructure.db.gateways.user_gateway import UserGateway


class GatewayProvider(Provider):
    user_gateway = provide(UserGateway, scope=Scope.REQUEST)
    session_gateway = provide(SessionGateway, scope=Scope.REQUEST)
