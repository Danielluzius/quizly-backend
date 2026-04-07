from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer
from auth_app.utils import set_auth_cookies, delete_auth_cookies
from django.conf import settings


class RegisterView(APIView):
    """Register a new user account."""

    def post(self, request):
        """Validate input and create a new user account."""
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'detail': 'User created successfully!'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Authenticate a user and set JWT cookies."""

    def post(self, request):
        """Authenticate user credentials and set JWT cookies."""
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        response = Response({
            'detail': 'Login successfully!',
            'user': {'id': user.id, 'username': user.username, 'email': user.email},
        })
        set_auth_cookies(response, refresh.access_token, refresh)
        return response


class LogoutView(APIView):
    """Blacklist the refresh token and clear auth cookies."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Blacklist the refresh token and delete auth cookies."""
        refresh_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token')
        raw_refresh = request.COOKIES.get(refresh_cookie)
        try:
            RefreshToken(raw_refresh).blacklist()
        except Exception:
            pass
        detail = 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'
        response = Response({'detail': detail})
        delete_auth_cookies(response)
        return response


class TokenRefreshView(APIView):
    """Issue a new access token using the refresh token cookie."""

    def post(self, request):
        """Issue a new access token from the refresh token cookie."""
        refresh_cookie = settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token')
        raw_refresh = request.COOKIES.get(refresh_cookie)
        if not raw_refresh:
            return Response({'detail': 'Refresh token missing.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(raw_refresh)
            response = Response({'detail': 'Token refreshed'})
            set_auth_cookies(response, refresh.access_token, refresh)
            return response
        except TokenError:
            return Response({'detail': 'Invalid or expired refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)
