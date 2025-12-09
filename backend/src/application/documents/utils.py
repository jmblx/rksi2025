import base64
import datetime
import json
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
        "module_height": 25.0,
        "module_width": 0.4,
        "quiet_zone": 6.5,
        "font_size": 12,
        "text_distance": 1.0,
        "background": "white",
        "foreground": "black",
        "write_text": True,
    })

    return buf.getvalue()
