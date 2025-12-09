from fastapi.responses import ORJSONResponse

from infrastructure.token_service import ACCESS_TTL_MINUTES, REFRESH_TTL_DAYS

base_refresh_token_settings = {
    "httponly": True,
    "secure": False,
    "max_age": REFRESH_TTL_DAYS * 60 * 60 * 24,
    "expires": REFRESH_TTL_DAYS * 60 * 60 * 24,
    "samesite": "lax",
}

base_access_token_settings = {
    "httponly": True,
    "secure": False,
    "max_age": ACCESS_TTL_MINUTES * 60,
    "expires": ACCESS_TTL_MINUTES * 60,
    "samesite": "strict",
}


def set_tokens(response: ORJSONResponse, refresh_token: str, access_token: str):
    response.set_cookie(
        **base_refresh_token_settings,
        key="refresh_token",
        value=refresh_token,
    )
    response.set_cookie(
        **base_access_token_settings,
        key="access_token",
        value=access_token,
    )
