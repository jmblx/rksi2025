import datetime
import secrets
import string
from io import BytesIO

from barcode import Code128
from barcode.writer import ImageWriter
import qrcode


SERVER_MSC_OFFSET = 3


def get_cur_msc_datetime():
    now = datetime.datetime.now()
    return now.astimezone(datetime.timezone(datetime.timedelta(hours=SERVER_MSC_OFFSET))).replace(tzinfo=None)


def generate_qr_code(data) -> bytes:
    qr = qrcode.QRCode(
        version=2,
        box_size=10,
        border=4,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def generate_barcode(data) -> bytes:
    data = str(data)

    barcode = Code128(data, writer=ImageWriter())

    buf = BytesIO()

    barcode.write(buf, options={
        "module_width": 0.2,
        "module_height": 25.0,
        "quiet_zone": 2.0,
        "write_text": False
    })

    return buf.getvalue()


def generate_short_token(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits  # base62
    return ''.join(secrets.choice(alphabet) for _ in range(length))
