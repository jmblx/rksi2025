from dishka import Provider, Scope, provide

from application.auth.code_to_token_handler import CodeToTokenHandler
from application.auth.login_handler import LoginHandler
from application.documents.create_document_handler import CreateDocumentHandler


class HandlerProvider(Provider):
    get_login_handler = provide(LoginHandler, scope=Scope.REQUEST)
    code_to_token_handler = provide(CodeToTokenHandler, scope=Scope.REQUEST)
    create_document_handler = provide(CreateDocumentHandler, scope=Scope.REQUEST)
