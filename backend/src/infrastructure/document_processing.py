import hashlib

from fastapi import UploadFile


async def compute_hash_stream(file: UploadFile) -> str:
    h = hashlib.sha256()
    chunk_size = 65536  # 64 KB

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)

    return h.hexdigest()
