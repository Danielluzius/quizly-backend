from django.conf import settings


def _set_single_cookie(response, key, value, lifetime, jwt):
    """Set a single HttpOnly cookie on the response."""
    response.set_cookie(
        key=key,
        value=str(value),
        max_age=int(lifetime.total_seconds()),
        httponly=jwt.get('AUTH_COOKIE_HTTP_ONLY', True),
        samesite=jwt.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        secure=jwt.get('AUTH_COOKIE_SECURE', False),
    )


def set_auth_cookies(response, access_token, refresh_token):
    """Set access and refresh tokens as HttpOnly cookies on the response."""
    jwt = settings.SIMPLE_JWT
    _set_single_cookie(
        response, jwt.get('AUTH_COOKIE', 'access_token'),
        access_token, jwt['ACCESS_TOKEN_LIFETIME'], jwt,
    )
    _set_single_cookie(
        response, jwt.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
        refresh_token, jwt['REFRESH_TOKEN_LIFETIME'], jwt,
    )


def delete_auth_cookies(response):
    """Delete access and refresh token cookies from the response."""
    jwt = settings.SIMPLE_JWT
    response.delete_cookie(jwt.get('AUTH_COOKIE', 'access_token'))
    response.delete_cookie(jwt.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
