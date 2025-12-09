from dishka import Provider, Scope, provide

from application.auth.code_to_token_handler import CodeToTokenHandler
from application.auth.login_handler import LoginHandler
from application.auth.logout_handler import InvalidateTokensHandler
from application.auth.refresh_tokens_handler import RefreshTokensHandler
from application.documents.check_document_handler import CheckDocumentHandler
from application.documents.create_document_handler import CreateDocumentHandler
from application.documents.user_document_checks_handler import ListUserDocumentChecksHandler


class HandlerProvider(Provider):
    get_login_handler = provide(LoginHandler, scope=Scope.REQUEST)
    code_to_token_handler = provide(CodeToTokenHandler, scope=Scope.REQUEST)
    create_document_handler = provide(CreateDocumentHandler, scope=Scope.REQUEST)
    check_document_handler = provide(CheckDocumentHandler, scope=Scope.REQUEST)
    list_user_document_checks_handler = provide(ListUserDocumentChecksHandler, scope=Scope.REQUEST)
    refresh_tokens_handler = provide(RefreshTokensHandler, scope=Scope.REQUEST)
    invalidate_tokens_handler = provide(InvalidateTokensHandler, scope=Scope.REQUEST)
