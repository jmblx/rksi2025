from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from core.di.providers.db import DBProvider
from core.di.providers.handlers import HandlerProvider
from core.di.providers.redis_provider import RedisProvider
from core.di.providers.gateways import GatewayProvider
from core.di.providers.settings import SettingsProvider
from core.di.providers.uow import UowProvider


prod_provders = [
    DBProvider(),
    RedisProvider(),
    GatewayProvider(),
    SettingsProvider(),
    # UseCaseProvider(),
    FastapiProvider(),
    HandlerProvider(),
    UowProvider(),
]

container = make_async_container(*prod_provders)
