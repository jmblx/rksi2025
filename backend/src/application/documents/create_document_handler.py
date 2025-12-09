import base64
import datetime

from fastapi import File

from application.common.interfaces.uow import Uow
from application.documents.utils import generate_qr_code
from infrastructure.db.gateways.document_gateway import DocumentGateway
from infrastructure.db.models.document import Document
from infrastructure.document_processing import compute_hash_stream


class CreateDocumentHandler:
    def __init__(self, document_gateway: DocumentGateway, uow: Uow):
        self.document_gateway = document_gateway
        self.uow = uow

    async def handle(self, document_file: File, exp_date: datetime.datetime):
        file_hash = await compute_hash_stream(document_file)
        exp_date = exp_date.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        cur_data = datetime.datetime.now().astimezone(datetime.timezone.utc).replace(tzinfo=None)

        document = Document(hash=file_hash, created_at=cur_data, expiration_date=exp_date)

        await self.document_gateway.save(document)
        await self.uow.commit()

        doc_id = document.id

        qr_png_bytes = generate_qr_code(doc_id, file_hash)

        qr_base64 = base64.b64encode(qr_png_bytes).decode("utf-8")

        return {
            "id": doc_id,
            "hash": file_hash,
            "qr_png_base64": qr_base64,
        }
