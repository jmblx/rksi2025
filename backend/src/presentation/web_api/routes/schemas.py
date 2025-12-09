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
