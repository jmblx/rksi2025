import base64
import datetime
import json

from fastapi import File

from application.common.interfaces.uow import Uow
from application.documents.utils import generate_qr_code, get_cur_msc_datetime, generate_barcode
from infrastructure.db.gateways.document_gateway import DocumentGateway
from infrastructure.db.models.document import Document
from infrastructure.document_processing import compute_hash_stream


class CreateDocumentHandler:
    def __init__(self, document_gateway: DocumentGateway, uow: Uow):
        self.document_gateway = document_gateway
        self.uow = uow

    async def handle(self, document_file: File, exp_date: datetime.datetime, code_type: str = "qr"):
        file_hash = await compute_hash_stream(document_file)
        exp_date = exp_date.astimezone(datetime.UTC).replace(tzinfo=None)
        cur_data = get_cur_msc_datetime()

        document = Document(hash=file_hash, created_at=cur_data, expiration_date=exp_date)

        await self.document_gateway.save(document)
        await self.uow.commit()

        doc_id = document.id

        payload = {"id": doc_id, "hash": file_hash}

        json_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        data = base64.urlsafe_b64encode(json_bytes).rstrip(b"=").decode("utf-8")

        if code_type == "qr":
            image_bytes = generate_qr_code(data)
        elif code_type == "barcode":
            image_bytes = generate_barcode(data)
        else:
            raise ValueError("Invalid code_type. Expected 'qr' or 'barcode'.")

        # Отдаём base64 PNG
        return base64.b64encode(image_bytes).decode("utf-8")

