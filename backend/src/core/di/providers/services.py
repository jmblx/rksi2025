from dishka import Provider, Scope, provide

from application.common.idp import IdentityProvider
from infrastructure.email_notification import EmailCodeService
from infrastructure.notification.smtp_service import SmtpService


class ServicesProvider(Provider):
    identity_provider = provide(IdentityProvider, scope=Scope.REQUEST)
    smtp_service = provide(SmtpService, scope=Scope.REQUEST)
    email_code_service = provide(EmailCodeService, scope=Scope.REQUEST)
