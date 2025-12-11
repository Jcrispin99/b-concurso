from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.contrib.auth.models import User


class LoginView(APIView):
    """
    Vista de login con formulario HTML en la Browsable API.
    Envía email y password para obtener el token.
    """

    serializer_class = LoginSerializer

    def get(self, request):
        return Response({"message": "Send POST with email and password"})

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate with username (Django's default auth uses username)
        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )


class RegisterView(APIView):
    """
    Vista de registro con formulario HTML en la Browsable API.
    Selecciona 'HTML form' en el dropdown de Media type para ver el formulario.
    """

    serializer_class = UserSerializer

    def get(self, request):
        return Response({"message": "Send POST with username, email, and password"})

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(username=request.data["username"])
            user.set_password(request.data["password"])
            user.save()

            token = Token.objects.create(user=user)

            return Response(
                {"token": token.key, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Vista de perfil protegida por token.
    Requiere header: Authorization: Token <tu_token>
    """

    from rest_framework.authentication import TokenAuthentication
    from rest_framework.permissions import IsAuthenticated

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": user.date_joined,
            }
        )
