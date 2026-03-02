from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from auth_app.permissions import IsOwner


class LoginView(APIView):

    permission_classes = []

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        print(username, password, request.data)

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        # кастомные claims
        refresh["userId"] = user.id
        refresh["accessLevel"] = user.level
        refresh["sub"] = user.username

        return Response({
            "token": str(refresh.access_token)
        })


class VerifyView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        return Response(status=200)
