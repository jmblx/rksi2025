import base64
import json
from io import BytesIO

import qrcode


def generate_qr_code(document_id: int, file_hash: str) -> bytes:
    # 1. Формируем JSON
    payload = {"id": document_id, "hash": file_hash}

    # 2. Кодируем as base64url без padding
    json_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    encoded = base64.urlsafe_b64encode(json_bytes).rstrip(b"=")

    # 3. Генерируем QR
    qr = qrcode.QRCode(
        version=2,
        box_size=10,
        border=4,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(encoded.decode("utf-8"))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # 4. Возвращаем PNG bytes
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
