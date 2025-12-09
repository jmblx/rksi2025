from datetime import datetime

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response

from application.documents.create_document_handler import CreateDocumentHandler
from infrastructure.document_processing import compute_hash_stream

document_router = APIRouter(prefix="/document", tags=["documents"], route_class=DishkaRoute)


@document_router.post("", responses={
    status.HTTP_201_CREATED: {"description": "Document uploaded"},
})
async def upload_document(
    handler: FromDishka[CreateDocumentHandler],
    file: UploadFile = File(...),
    exp_date: datetime = Form(...)
):
    return await handler.handle(file, exp_date)
