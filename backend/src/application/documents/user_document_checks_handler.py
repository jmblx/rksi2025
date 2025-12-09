from application.common.idp import IdentityProvider
from infrastructure.db.gateways.document_gateway import DocumentGateway


class ListUserDocumentChecksHandler:
    def __init__(self, document_gateway: DocumentGateway, idp: IdentityProvider):
        self.document_gateway = document_gateway
        self.idp = idp

    async def handle(self):
        user_id = await self.idp.get_current_user_id()
        return await self.document_gateway.list_doc_user(user_id)
