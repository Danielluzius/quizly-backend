from django.conf import settings


def set_auth_cookies(response, access_token, refresh_token):
    """Set access and refresh tokens as HttpOnly cookies on the response."""
    jwt = settings.SIMPLE_JWT
    response.set_cookie(
        key=jwt.get('AUTH_COOKIE', 'access_token'),
        value=str(access_token),
        max_age=int(jwt['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        httponly=jwt.get('AUTH_COOKIE_HTTP_ONLY', True),
        samesite=jwt.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        secure=jwt.get('AUTH_COOKIE_SECURE', False),
    )
    response.set_cookie(
        key=jwt.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
        value=str(refresh_token),
        max_age=int(jwt['REFRESH_TOKEN_LIFETIME'].total_seconds()),
        httponly=jwt.get('AUTH_COOKIE_HTTP_ONLY', True),
        samesite=jwt.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        secure=jwt.get('AUTH_COOKIE_SECURE', False),
    )


def delete_auth_cookies(response):
    """Delete access and refresh token cookies from the response."""
    jwt = settings.SIMPLE_JWT
    response.delete_cookie(jwt.get('AUTH_COOKIE', 'access_token'))
    response.delete_cookie(jwt.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
