from datetime import datetime

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter, File, Form, UploadFile
from starlette import status

from application.documents.check_document_handler import CheckDocumentHandler
from application.documents.create_document_handler import CreateDocumentHandler
from application.documents.user_document_checks_handler import ListUserDocumentChecksHandler
from presentation.web_api.routes.schemas import CheckDocumentResponse, UserDocumentListResponse, CodeType

document_router = APIRouter(prefix="/document", tags=["documents"], route_class=DishkaRoute)


@document_router.post("", responses={
    status.HTTP_201_CREATED: {"description": "Document uploaded. Returning base64 qr string"},
})
async def upload_document(
    handler: FromDishka[CreateDocumentHandler],
    file: UploadFile = File(...),
    exp_date: datetime = Form(...),
    code_type: CodeType = Form(...),
) -> str:
    return await handler.handle(file, exp_date, code_type)


@document_router.get(
    "/check/{doc_search_data}",
    response_model=CheckDocumentResponse,
    responses={404: {"description": "Document not found or invalid"}}
)
async def check_document(
    doc_search_data: str,
    handler: FromDishka[CheckDocumentHandler],
) -> CheckDocumentResponse:
    return await handler.handle(doc_search_data)


@document_router.get(
    "",
    response_model=UserDocumentListResponse,
    responses={status.HTTP_200_OK: {"description": "Users documents list"}},
)
async def list_documents(
    handler: FromDishka[ListUserDocumentChecksHandler],
):
    items = await handler.handle()
    return UserDocumentListResponse(items=items)
