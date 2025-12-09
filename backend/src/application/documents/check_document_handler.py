import base64
import json

from application.auth.common.errors import InvalidDocumentError
from application.common.idp import IdentityProvider
from infrastructure.db.gateways.document_gateway import DocumentGateway
from infrastructure.db.gateways.user_gateway import UserGateway


class CheckDocumentHandler:
    def __init__(self, user_gateway: UserGateway, document_gateway: DocumentGateway, idp: IdentityProvider):
        self.user_gateway = user_gateway
        self.document_gateway = document_gateway
        self.idp = idp

    async def handle(self, base64_doc_data: str):
        decoded_bytes = base64.urlsafe_b64decode(base64_doc_data + "==")
        json_str = decoded_bytes.decode("utf-8")
        doc_data = json.loads(json_str)
        doc_id, doc_hash = doc_data["id"], doc_data["hash"]
        document = await self.document_gateway.get_by_id(doc_id)
        if not document or document.hash != doc_hash:
            raise InvalidDocumentError

        return await self.document_gateway.check_document(document, await self.idp.get_current_user_id())
