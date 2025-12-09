from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr


class LoginResponse(BaseModel):
    user_id: int
    session_token: str


class MeResponse(BaseModel):
    id: int
    email: EmailStr


class CodeToTokenCommand(BaseModel):
    code: str
    email: EmailStr


class DocumentStatus(str, Enum):
    green = "green"
    yellow = "yellow"
    red = "red"


class CodeType(str, Enum):
    qr = "qr"
    barcode = "barcode"


class CheckDocumentResponse(BaseModel):
    id: int
    status: DocumentStatus
    expiration_date: datetime
    created_at: datetime
    checked_at: datetime


class UserDocumentItem(BaseModel):
    document_id: int
    status: DocumentStatus
    expiration_date: datetime
    created_at: datetime
    checked_at: datetime


class UserDocumentListResponse(BaseModel):
    items: list[UserDocumentItem]
